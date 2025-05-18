import gettext
import os
import contextvars



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES_PATH = os.path.join(BASE_DIR, "locales")


current_translation = contextvars.ContextVar(
    "current_translation", default=gettext.NullTranslations()
)

def set_language(language_code: str = "en"):
    """
    Устанавливает текущий язык для конкретного пользователя.
    Если перевод не найден, используется NullTranslations.
    """
    try:

        translation = gettext.translation(
            "messages",
            localedir=LOCALES_PATH,
            languages=[language_code],
            fallback=True
        )
    except Exception as e:
        print(f"Ошибка при установке языка (set_language): {e}")
        translation = gettext.NullTranslations()


    current_translation.set(translation)


def _(s: str) -> str:
    """
    Возвращает переведённую строку для текущего пользователя.
    Если перевод недоступен, возвращается исходная строка.
    """
    translation = current_translation.get()
    return translation.gettext(s)








