from django.shortcuts import render,redirect
from web.referral_program import services


def get_referral_program_settings(request):
    settings = services.get_referral_program_settings()
    context = {
        'settings': settings,
    }
    return render(
        request,
        'referral_program/referral_program_settings.html',
        context=context
    )


def update_referral_program_settings(request):
    if request.method == 'POST':
        services.update_referral_program_settings(request.POST)
        return redirect('/referral_program')

