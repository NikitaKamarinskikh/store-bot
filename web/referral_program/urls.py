from django.urls import path
from web.referral_program import views

urlpatterns = [
    path('', views.get_referral_program_settings),
    path('update/', views.update_referral_program_settings, name='update-referral-program-settings')
]



