from fastapi import status

from innonymous.api.docs.exceptions import (
    invalid_or_expired_token,
    too_many_requests,
    room_not_found
)
from innonymous.api.schemas import HTTPExceptionSchema

description = 'Create a new message.'
responses = {
    status.HTTP_403_FORBIDDEN: {
        'description': 'If access_token is expired or invalid.',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    **invalid_or_expired_token
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        'description': 'Room with the given uuid not found.',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    **room_not_found
                }
            }
        }
    },
    status.HTTP_429_TOO_MANY_REQUESTS: {
        'description': 'If user sends too many requests.',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    **too_many_requests
                }
            }
        }
    }
}
