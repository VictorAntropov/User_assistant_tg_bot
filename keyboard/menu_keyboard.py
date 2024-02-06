from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants.information import USER

CALLBACKS = {
    'yes': f'{USER}yes',
    'no': f'{USER}no',
}

menu_keyboard = [
        [
            InlineKeyboardButton('Да',
                                 callback_data=CALLBACKS.get('yes')),
            InlineKeyboardButton('Нет',
                                 callback_data=CALLBACKS.get('no')),
        ],
    ]

reply_markup = InlineKeyboardMarkup(menu_keyboard)
