from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index , name='index'),
    path('pre-test/<str:px_id>/<str:session_id>', views.pre_test, name='pre-test'),
    path('px-details/', views.px_details,  name='px-details'),
    path('px-instructions/<str:px_id>', views.px_instructions,  name='px-instructions'),
    path('test-a/<str:px_id>/<str:session_id>', views.test_a, name='test-a'),
    path('test-b/<str:px_id>/<str:session_id>', views.test_b, name='test-b'),
    path('test-c/<str:px_id>/<str:session_id>', views.test_c, name='test-c'),
    path('finish/<str:px_id>/<str:session_id>', views.finish, name='finish'),


    path('recording/', views.recording, name='recording'),


    path('api/', views.api, name='api')
]
