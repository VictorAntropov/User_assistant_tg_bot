from telegram import BotCommandScopeChat, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)

from constants.information import (USER, HELP, ONE,
                                   PROJECT_CORRECT_EMAIL, PROJECT_EMAIL,
                                   PROJECT_EXAMPLE, PROJECT_MESSAGE,
                                   PROJECT_MISTAKE, PROJECT_NO, PROJECT_STOP,
                                   PROJECT_USER_INFO, PROJECT_USER_QUESTION,
                                   PROJECT_USER_TEXT, PROJECT_WORK_PLACE,
                                   PROJECT_YES, START, STOP, THREE, TWO)
from core.settings import settings
from keyboard.menu_keyboard import reply_markup
from utils.create_user import create_user_in_db
from utils.send_email import send_message_qr_kod_and_email
from utils.validators import (check_user_email, getting_user_address_company,
                              getting_user_info)

user_info = {}


async def greeting_callback(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Приветствие /start.'''
    await context.bot.set_my_commands(
        [START, STOP, HELP],
        scope=BotCommandScopeChat(update.effective_chat.id),
    )
    await update.message.reply_text(PROJECT_MESSAGE,
                                    reply_markup=reply_markup)
    return ONE


async def help_callback(update: Update,
                        context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Связаться с разработчиком /help.'''
    await update.message.reply_text(PROJECT_USER_QUESTION)
    return ONE


async def stop_callback(update: Update,
                        context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Остановить работу бота /stop.'''
    await update.message.reply_text(PROJECT_STOP,
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def commands(update: Update,
                   context: ContextTypes.DEFAULT_TYPE, command: str) -> None:
    '''Команда - действия.'''

    commands_handlers = {
        'help': help_callback,
        'stop': stop_callback,
    }
    if command in commands_handlers:
        await commands_handlers[command](update, context)


async def get_user_question_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Обработка вопроса от пользователя и отправка разработчику'''
    if update.message.text.startswith('/'):
        command = update.message.text[1:]
        await commands(update, context, command)
        return ConversationHandler.END

    user_text = update.message.text
    await context.bot.send_message(chat_id=settings.tg_id, text=user_text)
    await update.message.reply_text(PROJECT_USER_TEXT)


async def handle_process_yes(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Нажатие кнопки "Да"'''
    await update.callback_query.message.reply_text(PROJECT_YES)
    return ONE


async def handle_process_no(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Нажатие кнопки "Нет"'''
    await update.callback_query.message.reply_text(PROJECT_NO)


async def first_info_about_user(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Персональная информация от пользователя(фамилия, имя, номер)'''
    full_name = update.message.text

    if update.message.text.startswith('/'):
        command = update.message.text[1:]
        await commands(update, context, command)
        return ConversationHandler.END

    try:
        first_name, second_name, number = getting_user_info(full_name)
        chat_id = update.message.chat.id
        user_info.update({'chat_id': chat_id, 'first_name': first_name,
                         'second_name': second_name, 'number': number})
        await update.message.reply_text(PROJECT_WORK_PLACE)
        return TWO
    except Exception as e:
        await update.message.reply_text(f'{PROJECT_MISTAKE}: {str(e)}')


async def second_info_about_user(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    '''Персональная информация от пользователя(работа, город)'''
    info_user = update.message.text

    if update.message.text.startswith('/'):
        command = update.message.text[1:]
        await commands(update, context, command)
        return ConversationHandler.END

    company, address = getting_user_address_company(info_user)
    user_info.update({'company': company, 'address': address})
    await update.message.reply_text(PROJECT_EMAIL)
    return THREE


async def last_info_about_user(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    '''Персональная информация от пользователя(электронная почта)'''
    email = update.message.text

    if update.message.text.startswith('/'):
        command = update.message.text[1:]
        await commands(update, context, command)
        return ConversationHandler.END

    if email == PROJECT_EXAMPLE:
        await update.message.reply_text(PROJECT_CORRECT_EMAIL)
        return
    try:
        correct_email = check_user_email(email)
        user_info.update({'email': correct_email})
        await update.message.reply_text(PROJECT_USER_INFO)
        await create_user_in_db(user_info)
        qr_kod = send_message_qr_kod_and_email(user_info)
        await update.message.reply_photo(qr_kod)
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f'{PROJECT_MISTAKE}: {str(e)}')


conv_callback = ConversationHandler(
    entry_points=[CommandHandler('start', greeting_callback)],
    states={
        ONE: [
            MessageHandler(filters.TEXT, first_info_about_user),
        ],
        TWO: [
            MessageHandler(filters.TEXT, second_info_about_user),
        ],
        THREE: [
            MessageHandler(filters.TEXT, last_info_about_user),
        ],

    },
    fallbacks=[CommandHandler('stop', stop_callback)],
)

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help_callback)],
        states={
            ONE: [
                MessageHandler(filters.ALL, get_user_question_callback)
            ],
        },
        fallbacks=[CommandHandler('stop', stop_callback)],
    )


def register_handlers(application: Application) -> None:
    '''Регистрация обработчиков.'''

    application.add_handler(conv_callback)
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(
        handle_process_no,
        pattern=f'{USER}no'))
    application.add_handler(CallbackQueryHandler(
        handle_process_yes,
        pattern=f'{USER}yes',
        ))
