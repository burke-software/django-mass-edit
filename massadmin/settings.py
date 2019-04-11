from django.conf import settings


_default_settings = {
    'ADD_ACTION_GLOBALLY': True,
    'SESSION_BASED_URL_THRESHOLD': 500,
}

_settings = getattr(settings, 'MASSEDIT', _default_settings)


def _get_value(name):
    return _settings.get(name, _default_settings[name])


ADD_ACTION_GLOBALLY = _get_value('ADD_ACTION_GLOBALLY')
SESSION_BASED_URL_THRESHOLD = _get_value('SESSION_BASED_URL_THRESHOLD')
