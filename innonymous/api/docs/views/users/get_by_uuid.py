from fastapi import status

from innonymous.api.docs.exceptions import user_not_found
from innonymous.api.schemas import HTTPExceptionSchema

description = 'Returns a user by uuid.'
responses = {
    status.HTTP_404_NOT_FOUND: {
        'description': 'User with the given uuid not found.',
        'model': HTTPExceptionSchema,
        'content': {
            'application/json': {
                'examples': {
                    **user_not_found
                }
            }
        }
    }
}
