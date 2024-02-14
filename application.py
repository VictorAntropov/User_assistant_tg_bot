from telegram.ext import Application

from core.settings import settings
from handlers import register_all_handlers


def main() -> None:  # noqa
    '''Запуск бота.'''

    application = Application.builder().token(settings.token).build()

    register_all_handlers(application)

    application.run_polling()


if __name__ == '__main__':
    main()
