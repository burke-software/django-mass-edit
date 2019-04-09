from django.conf import settings


_default_settings = {
    'ADD_ACTION_GLOBALLY': True,
}

_settings = getattr(settings, 'MASSEDIT', _default_settings)

ADD_ACTION_GLOBALLY = _settings.get(
    'ADD_ACTION_GLOBALLY', _default_settings['ADD_ACTION_GLOBALLY'])
