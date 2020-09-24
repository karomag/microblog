# -*- coding:utf-8 -*-

"""Text translation function."""

import json

import requests
from flask_babel import _

from flask import current_app


def translate(text, source_language, dest_language):
    key_not_found = (
        'MS_TRANSLATOR_KEY' not in current_app.config
        or not current_app.config['MS_TRANSLATOR_KEY']
    )
    if key_not_found:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get(
        '{0}/Translate?text={1}&from={2}&to={3}'.format(
            'https://api.microsofttranslator.com/v2/Ajax.svc',
            text,
            source_language,
            dest_language,
        ),
        headers=auth,
    )
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))
