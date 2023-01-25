from django.http import QueryDict
from referral_program.config import ReferralProgramSettings
from referral_program import referral_program

def get_referral_program_settings() -> ReferralProgramSettings:
    return referral_program.load_referral_program_settings_from_json_file()


def update_referral_program_settings(data: QueryDict) -> None:
    settings = _convert_post_data_to_referral_program_settings(data)
    referral_program.save_referral_program_setting_to_json_file(settings)


def _convert_post_data_to_referral_program_settings(data: QueryDict) -> ReferralProgramSettings:
    settings = ReferralProgramSettings(
        int(data.get('user_acquisition_reward')),
        int(data.get('referral_reward')),
        int(data.get('referral_order_reward')),
        int(data.get('make_order_reward'))
    )
    if 'user_acquisition_reward_satus' in data:
        settings.user_acquisition_reward_satus = True
    if 'make_order_reward_status' in data:
        settings.make_order_reward_status = True
    if 'referral_order_reward_status' in data:
        settings.referral_order_reward_status = True
    return settings


