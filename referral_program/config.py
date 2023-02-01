from dataclasses import dataclass

REFERRAL_PROGRAM_SETTINGS_FILE_NAME = 'referral_program_settings.json'

@dataclass
class ReferralProgramSettings:
    user_acquisition_reward: int = 0 # Вознаграждение за привлечение пользователя.
    referral_reward: int = 0  # Вознаграждение привлеченному пользователю.
    referral_order_reward_in_percentages: int = 0 # Вознаграждение в % за заказ привлеченным пользователем.
    make_order_reward_in_percentages: int =  0 # Вознаграждение себе в % за свой заказ
    user_acquisition_reward_satus: bool = False # вознаграждение, за приглашение, пока преферал не сделал заказ.
    make_order_reward_status: bool = False # вознаграждение за собственный заказ.
    referral_order_reward_status: bool = False # вознаграждение за заказ рефералов

    def as_dict(self) -> dict:
        return {
            "user_acquisition_reward": self.user_acquisition_reward,
            "referral_reward": self.referral_reward,
            "referral_order_reward_in_percentages": self.referral_order_reward_in_percentages,
            "make_order_reward_in_percentages": self.make_order_reward_in_percentages,
            "user_acquisition_reward_satus": self.user_acquisition_reward_satus,
            "make_order_reward_status": self.make_order_reward_status,
            "referral_order_reward_status": self.referral_order_reward_status
        }
