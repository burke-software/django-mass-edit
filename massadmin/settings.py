from django.conf import settings


_default_settings = {
    'ADD_ACTION_GLOBALLY': True,
    'SESSION_BASED_URL_THRESHOLD': 500,
}

_settings = getattr(settings, 'MASSEDIT', _default_settings)

ADD_ACTION_GLOBALLY = _settings.get(
    'ADD_ACTION_GLOBALLY', _default_settings['ADD_ACTION_GLOBALLY'])


SESSION_BASED_URL_THRESHOLD = _settings.get(
    'SESSION_BASED_URL_THRESHOLD', _default_settings['SESSION_BASED_URL_THRESHOLD'])
