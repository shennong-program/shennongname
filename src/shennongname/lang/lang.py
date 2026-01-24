import os
import gettext


localedir = os.path.join(os.path.dirname(__file__), 'locale')


def get_translation(lang):
    return gettext.translation('messages', localedir, languages=[lang], fallback=True).gettext
