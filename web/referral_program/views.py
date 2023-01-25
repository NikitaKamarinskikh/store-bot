from django.shortcuts import render


def index(request):
    return render(
        request,
        'referral_program/referral_program_settings.html'
    )

