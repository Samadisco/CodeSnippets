from django.db import models

# Create your models here.

class PxData(models.Model):
    px_id = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    sessions = models.CharField(max_length=500, null=True, blank=True)


class TestData(models.Model):
    pretest_rec = models.FileField(upload_to='recordings/', null=True, blank = True)
    pretest_time = models.CharField(max_length=50, null=True, blank=True)
    pretest_standard = models.CharField(max_length=500, null=True, blank=True)
    pretest_raw = models.CharField(max_length=500, null=True, blank=True)
    pretest_score = models.CharField(max_length=50, null=True, blank=True)

    test_a_rec = models.FileField(upload_to='recordings/', null=True, blank = True)
    test_a_time = models.CharField(max_length=50, null=True, blank=True)
    test_a_standard = models.CharField(max_length=500, null=True, blank=True)
    test_a_raw = models.CharField(max_length=500, null=True, blank=True)
    test_a_omissions = models.CharField(max_length=50, null=True, blank=True)
    test_a_additions = models.CharField(max_length=50, null=True, blank=True)

    test_b_rec = models.FileField(upload_to='recordings/', null=True, blank = True)
    test_b_time = models.CharField(max_length=50, null=True, blank=True)
    test_b_standard = models.CharField(max_length=500, null=True, blank=True)
    test_b_raw = models.CharField(max_length=500, null=True, blank=True)
    test_b_omissions = models.CharField(max_length=50, null=True, blank=True)
    test_b_additions = models.CharField(max_length=50, null=True, blank=True)

    test_c_rec = models.FileField(upload_to='recordings/', null=True, blank = True)
    test_c_time = models.CharField(max_length=50, null=True, blank=True)
    test_c_standard = models.CharField(max_length=500, null=True, blank=True)
    test_c_raw = models.CharField(max_length=500, null=True, blank=True)
    test_c_omissions = models.CharField(max_length=50, null=True, blank=True)
    test_c_additions = models.CharField(max_length=50, null=True, blank=True)

    session_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"TestData {self.id}"

