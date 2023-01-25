from dataclasses import dataclass

REFERRAL_PROGRAM_SETTINGS_FILE_NAME = 'referral_program_settings.json'

@dataclass
class ReferralProgramSettings:
    user_acquisition_reward: int
    referral_reward: int
    referral_order_reward: int
    make_order_reward: int
    user_acquisition_reward_satus: bool = False
    make_order_reward_status: bool = False
    referral_order_reward_status: bool = False

    def as_dict(self) -> dict:
        return {
            "user_acquisition_reward": self.user_acquisition_reward,
            "referral_reward": self.referral_reward,
            "referral_order_reward": self.referral_order_reward,
            "make_order_reward": self.make_order_reward,
            "user_acquisition_reward_satus": self.user_acquisition_reward_satus,
            "make_order_reward_status": self.make_order_reward_status,
            "referral_order_reward_status": self.referral_order_reward_status
        }
