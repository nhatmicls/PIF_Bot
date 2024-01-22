from utils import *
from typing import *


class botInfrastructureManagementResponseDefault:
    deny_expect_time_response = (
        "You unable to borrow.\n"
        "Your expected return date EXCEEDED the maximum item borrowing duration.\n"
        "Please contact DIRECT to authority for borrow this item."
    )
    deny_out_of_quota_response = (
        "You unable to borrow.\n"
        "Your borrow item quota is reach.\n"
        "Please contact DIRECT to authority for borrow any more item."
    )

    review_for_long_time_borrow_response = (
        "You able to borrow.\n"
        "Your expected return date EXCEEDED the maximum item borrowing duration without need permission.\n"
        "But it will notice to our authority."
    )

    deny_extend_expected_return_day_response = (
        "You unable to extend expected return time.\n"
        "You already extended it the pass.\n"
        "Please contact DIRECT to authority for extend return day this item."
    )

    deny_extend_long_expected_return_day_response = (
        "You unable to extend expected return time.\n"
        "Your expected return date EXCEEDED the maximum item borrowing duration.\n"
        "Please contact DIRECT to authority for extend return day this item."
    )

    deny_extend_borrow_not_confirm_response = (
        "You unable to extend expected return time.\n"
        "This return is not confirm please contact to authority confirm and extend it later.\n"
        "Thanks."
    )

    extend_expected_return_day_response = (
        "Your expected return date has been extended.\n"
        "You can not extend anymore please notice that.\n"
        "Thanks."
    )

    borrow_response = "Your borrow ID is: <ID>\n" "Your remaining days is: <days> ."

    return_response = (
        "Your returned the item.\n"
        "Thanks for return it ontime.\n"
        "If you need to borrow any item next time, please register with this system. Thanks"
    )

    no_borrow_item_response = "You are not borrowing any item from PIF LAB."

    borrow_id_not_found_response = "ID not found, please try again."

    confirm_return_response = "This item confirm is returned."


class botInfrastructureManagementAdminResponseDefault:
    borrow_admin_affirm_response = (
        "You are just affirm the borrow ID: <ID>.\n"
        "I will send notice to the borrower\n"
        "You are using admin tool, please use in the right way\n"
        "Thanks."
    )

    borrow_admin_deny_response = (
        "You are just deny the borrow ID: <ID>.\n"
        "I will send notice to the borrower\n"
        "You are using admin tool, please use in the right way\n"
        "Thanks."
    )

    return_admin_affirm_response = (
        "You are just affirm the return of borrow ID: <ID>.\n"
        "I will send notice to the borrower\n"
        "You are using admin tool, please use in the right way\n"
        "Thanks."
    )

    return_admin_not_found_response = (
        "You are just not found the return of borrow ID: <ID>.\n"
        "I will send notice to the borrower to return/find again or it will change state to lost\n"
        "You are using admin tool, please use in the right way\n"
        "Thanks."
    )

    no_borrow_found_response = (
        "No one borrow anything in lab please check it later.\n"
        "Note: This system depend on human innocent please check it manually\n"
        "Thanks."
    )

    no_return_queue_response = (
        "No one return item in queue please check it later.\n" "Thanks."
    )

    no_late_return_item_found_response = (
        "No one late return item found in system please check it later.\n" "Thanks."
    )

    no_lost_item_found_response = (
        "No one lost item found in system please check it later.\n" "Thanks."
    )

    borrow_need_review_queue_add_response = (
        "**<Name>** just borrow **`<Item_name>`** but longer than expect (<ETA_of_days_to_return> days), ID borrow: <ID>.\n"
        "Please check it manually and confirm it\n"
        "Thanks."
    )

    return_queue_add_response = (
        "**<Name>** just returned **`<Item_name>`**, ID borrow: <ID>.\n"
        "Please check it manually and confirm it\n"
        "Thanks."
    )
