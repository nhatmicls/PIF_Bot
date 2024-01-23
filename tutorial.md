# PIF BOT TUTORIAL

Writen by: Micls

## User command

Command can use by every member

### Member manager

- `sign_up`: Use for sign up data to server

### Infrastructure manager

- `infra_borrow`: Use for sign up borrow item
- `infra_list`: Use for show list item is currently borrow
- `infra_extend`: Use for for extend deadline return item
- `infra_return`: Use for sign up return item

Note:
- When borrow some item, the system will return to you a borrow ID, it will use for identify your borrow section in system to return or extend your deadline return, ....

## Admin command

Command can only use by admin/managerment team

### Member manager

- `change_data`: Use for change user data

### Infrastructure manager

- `infra_admin_borrow`: Use for sign up borrow item for someone.
- `infra_admin_list`: Use for show list borrow item from who.
- `infra_admin_extend`: Use for extend deadline return item for someone.
- `infra_borrow_admin_affirm`: Use for confirm borrow item when it need to verify.
- `infra_borrow_admin_deny`: Use for deny borrow item when it to verify.
- `infra_return_admin_affirm`: Use for confirm item had been returned to LAB.
- `infra_return_admin_fail`: Use for NOT confirm item had been returned to LAB, it will change state to `LOST`.
- `infra_review_admin_list`: Use for show list borrow item need to be review.
- `infra_borrow_admin_list`: Use for show list borrow item.
- `infra_return_admin_list`: Use for show list returned item need to be review.
- `infra_late_admin_list`: Use for show list late return item need to be review.
- `infra_lost_admin_list`: Use for show list lost item need to be review.