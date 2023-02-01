from db_api import clients
from referral_program.referral_program import load_referral_program_settings_from_json_file
from .notifications import notify_client_about_first_order_of_his_referral, notify_client_about_new_order_of_his_referral


def check_client_referrer(client_telegram_id: int, order_amount: int) -> None:
    client = clients.get_by_telegram_id_or_none(client_telegram_id)
    if client.referrer is not None:
        referral_program_settings = load_referral_program_settings_from_json_file()
        if referral_program_settings.referral_order_reward_status:
            referrer = client.referrer
            if client.orders_quantity == 1:
                clients.add_coins(referrer, 100)
                notify_client_about_first_order_of_his_referral(referrer.telegram_id, 100)
            else:
                percent = referral_program_settings.referral_order_reward_in_percentages
                bonus = (order_amount * percent) // 100
                clients.add_coins(referrer, bonus)
                notify_client_about_new_order_of_his_referral(referrer.telegram_id, bonus)




