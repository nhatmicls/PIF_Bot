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
