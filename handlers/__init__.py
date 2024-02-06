from telegram.ext import Application

from . import main_application


def register_all_handlers(application: Application):
    main_application.register_handlers(application)
