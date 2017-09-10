from rest_framework.response import Response
from rest_framework import status

from common.apis import GenericServiceApi

from users.services import create_user
from users.serializers import CreateUserSerializer


class CreateUserApi(GenericServiceApi):
    serializer_class = CreateUserSerializer

    def get_service(self):
        return create_user

    def get_response(self, service_result):
        return Response(status=status.HTTP_202_ACCEPTED)
