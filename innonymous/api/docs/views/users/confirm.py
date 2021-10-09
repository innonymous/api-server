from fastapi import status

from innonymous.api.docs.exceptions import (
    invalid_or_expired_token
)
from innonymous.api.schemas import HTTPExceptionSchema

description = 'Returns a user by uuid.'
responses = {
    status.HTTP_403_FORBIDDEN: {
        'description': 'If create_token is expired or invalid.',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    **invalid_or_expired_token
                }
            }
        }
    },
    status.HTTP_400_BAD_REQUEST: {
        'description': 'If the captcha is invalid or user already exists '
                       '(token was already used).',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    'Invalid captcha.': {
                        'value': {
                            'detail': 'Invalid captcha.'
                        }
                    },
                    'User already exists.': {
                        'value': {
                            'detail': 'User already exists.'
                        }
                    }
                }
            }
        }
    }
}
