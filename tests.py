import json
from config import ReferralProgramSettings, REFERRAL_PROGRAM_SETTINGS_FILE_NAME


def load_referral_program_settings_from_json_file() -> ReferralProgramSettings:
    with open(REFERRAL_PROGRAM_SETTINGS_FILE_NAME, 'r') as settings_file:
        data = json.load(settings_file)
        referral_program_settings = ReferralProgramSettings(
            data['user_acquisition_reward'],
            data['referral_reward'],
            data['referral_order_reward'],
            data['make_order_reward'],
            data['user_acquisition_reward_satus'],
            data['make_order_reward_status'],
            data['referral_order_reward_status']
        )
        return referral_program_settings


def save_referral_program_setting_to_json_file(settings: ReferralProgramSettings) -> None:
    with open(REFERRAL_PROGRAM_SETTINGS_FILE_NAME, 'w') as settings_file:
        json.dump(settings.as_dict(), settings_file)


if __name__ == '__main__':
    settings = load_referral_program_settings_from_json_file()
    settings.make_order_reward = 100
    settings.referral_order_reward_status = False
    settings.referral_order_reward = 100
    settings.referral_reward= 33
    save_referral_program_setting_to_json_file(settings)


datadata