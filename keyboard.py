from aiogram import types

adminMenu = types.InlineKeyboardMarkup(row_width=1)
adminMenu.add (
    types.InlineKeyboardButton(text = 'Создать лот', callback_data= 'createLot'),
    types.InlineKeyboardButton(text = 'Добавить админа', callback_data= 'addAdminInBd')
)

lootAction = types.InlineKeyboardMarkup(row_width=1)
lootAction.add(
    types.InlineKeyboardButton('Увеличить цену на 3 000', callback_data= 'addMoneyCar'),
    types.InlineKeyboardButton('Увеличить цену на 5 000', callback_data= 'addMoneyCar5000'),
    types.InlineKeyboardButton('Увеличить цену на 10 000', callback_data= 'addMoneyCar10000')
)

cancel = types.InlineKeyboardMarkup(row_width=1)
cancel.add(
    types.InlineKeyboardButton('Отмена', callback_data= 'cancel')
)
def checkRules():
    choiseUser = types.InlineKeyboardMarkup()
    choiseUser.add(
        types.InlineKeyboardButton('Принять', callback_data= 'accept'),
        types.InlineKeyboardButton('Отклонить', callback_data= 'decline')
    )
    return choiseUser
