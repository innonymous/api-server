from fastapi import status

from innonymous.api.docs.exceptions import room_not_found
from innonymous.api.schemas import HTTPExceptionSchema

description = 'Returns a room by uuid.'
responses = {
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
    }
}
