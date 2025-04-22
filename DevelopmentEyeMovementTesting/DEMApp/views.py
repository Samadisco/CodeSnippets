from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
import json
from .models import *
import random
import base64
from django.core.files.base import ContentFile
import os

PRETEST_STANDARD = [5287493162]
TEST_A_STANDARD = [3759825746147637939245217537487465292364]
TEST_B_STANDARD = [7125484735256471923689573647523686412937]
TEST_C_STANDARD = [87593657423476129398752148374524657132964236924657837457521429397347616874287593]

# def find_differences(standard, response):
#     omission = False
#     addition = False
#     if len(standard) > len(response):
#         omission = True
#     elif len(standard) < len(response):        
#         addition = True  
#     else:
#         omission = False
#         addition = False   


def find_differences(standard, response):
    standard_digits = [int(digit) for digit in str(standard[0])]
    response_digits = [int(digit) for digit in str(response[0])]
    missing_digits = []
    added_digits = []   
    i, j = 0, 0
    while i < len(standard_digits) and j < len(response_digits):
        if standard_digits[i] == response_digits[j]:
            i += 1
            j += 1
        elif standard_digits[i] not in response_digits[j:]:
            missing_digits.append(standard_digits[i])
            i += 1
        else:
            added_digits.append(response_digits[j])
            j += 1
    missing_digits.extend(standard_digits[i:]) 
    added_digits.extend(response_digits[j:])
    return missing_digits, added_digits

# TEST_A_STANDARD = [122045]
# m, a = find_differences(TEST_A_STANDARD, [10220458])
# print(m,a)


def index(request):
    return render(request, 'index.html')
    
def px_details(request):
    if request.method == 'POST':
        px_id=request.POST.get('px_id')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        school=request.POST.get('school')
        a = PxData(px_id=px_id, age=age, sex=gender,school=school)
        a.save()
        return redirect(px_instructions, px_id)
    return render(request, 'px-details.html')

def px_instructions(request, px_id):
    # print(getattr(request, 'px_id'))
    return render(request, 'px-instructions.html', {'px_id':px_id})

def pre_test(request, px_id, session_id):
    return render(request, 'pre-test.html', {'px_id':px_id, 'session_id':session_id})    

def test_a(request,px_id, session_id):
    return render(request, 'test-a.html',{'px_id':px_id, 'session_id':session_id})  

def test_b(request, px_id, session_id):
    return render(request, 'test-b.html', {'px_id':px_id, 'session_id':session_id})  

def test_c(request, px_id, session_id):
    return render(request, 'test-c.html', {'px_id':px_id, 'session_id':session_id}) 


def finish(request, px_id, session_id):
    return render(request, 'finish.html', {'px_id':px_id, 'session_id':session_id})


def recording(request):
    return render(request, 'recording.html')


def api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        audio = data.get('audio_data')
        session_id = data.get('session_id')
        test = data.get('test')
        a = None

        if test == 'time_submissions':
            a = TestData.objects.get(session_id=session_id)
            a.pretest_time = data.get('pretest_time')
            a.test_a_time = data.get('test_a_time')
            a.test_b_time = data.get('test_b_time')
            a.test_c_time = data.get('test_c_time')
            a.save()
        else:
            # Decode Base64 and save as a file
            audio_file = ContentFile(base64.b64decode(audio), name=f"{session_id}.wav")

            if TestData.objects.filter(session_id=session_id).exists():
                data = TestData.objects.get(session_id=session_id)
                # data.
                if test == 'pretest': 
                    data.pretest_rec = audio_file
                elif test == 'test_a':   
                    data.test_a_rec = audio_file
                elif test == 'test_b':   
                    data.test_b_rec = audio_file
                elif test == 'test_c':   
                    data.test_c_rec = audio_file
                data.save()
                attribute_name = test  # e.g., "posttest_rec", "midtest_rec", etc.
                input_file_path = getattr(data, f'{attribute_name}_rec').path
                output_file_path = os.path.join(os.path.dirname(input_file_path), f"converted_audio.wav")
            else:
                if test == 'pretest': 
                    audio_instance = TestData(pretest_rec=audio_file, session_id=session_id)
                elif test == 'test_a':   
                    audio_instance = TestData(test_a_rec=audio_file, session_id=session_id)
                elif test == 'test_b':   
                    audio_instance = TestData(test_b_rec=audio_file, session_id=session_id)
                elif test == 'test_c':   
                    audio_instance = TestData(test_c_rec=audio_file, session_id=session_id)
                audio_instance.save()  

                a = TestData.objects.get(session_id=session_id)

                attribute_name = test
                input_file_path = getattr(a, f'{attribute_name}_rec').path
                output_file_path = os.path.join(os.path.dirname(input_file_path), f"converted_audio.wav")


            import subprocess
            subprocess.run([
                    "ffmpeg", "-i", input_file_path,
                    "-acodec", "pcm_s16le", "-ar", "16000", output_file_path,
                    "-y"
                ], check=True)

            response = recognize_speech_from_file(output_file_path)
            if a in locals():
                attribute = getattr(a, f'{test}_raw')
                print(f'{test.upper()}_STANDARD')
                missing, added = find_differences(globals().get(f'{test.upper()}_STANDARD'), response.replace(' ',''))
                setattr(a, f'{test}_additions', added)
                setattr(a, f'{test}_omissions', missing)
                standard_value = globals().get(f'{test.upper()}_STANDARD')
                setattr(data, f'{test}_standard', standard_value)
                attribute = response.replace(' ','')
                attribute.save()
            else:
                data = TestData.objects.get(session_id=session_id)
                setattr(data, f'{test}_raw', response.replace(' ',''))  # Set the attribute properly
                missing, added = find_differences(globals().get(f'{test.upper()}_STANDARD'), response.replace(' ',''))
                setattr(data, f'{test}_additions', added)
                setattr(data, f'{test}_omissions', missing)
                standard_value = globals().get(f'{test.upper()}_STANDARD')
                setattr(data, f'{test}_standard', standard_value) 
                data.save()   
 
    return JsonResponse({'data':'Working'})




import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to process an existing audio file
def recognize_speech_from_file(audio_path):
    try:
        # Load the recorded audio file
        with sr.AudioFile(audio_path) as source:
            print("Processing audio file... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for background noise
            audio = recognizer.record(source)  # Read the entire file

        # Recognize the speech using Google Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")

        # Validate if the recognized text is a number
        if text.replace(" ", "").isdigit():  # Remove spaces & check if it's numeric
            print(f"Valid number: {text}")
            return text
        else:
            print("Sorry, the audio did not contain a valid number.")
            return None

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Network error. Check your internet connection.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Provide the path to your recorded audio file
audio_file_path = "recordings/recording.wav"  # Update with your actual file path

# Process the audio file
recognized_number = recognize_speech_from_file(audio_file_path)

if recognized_number:
    print(f"Number successfully recognized: {recognized_number}")
else:
    print("No valid number recognized.")
