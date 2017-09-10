from django.test import TestCase, RequestFactory

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


from common.apis import GenericServiceApi


class GenericServiceApiExceptionHandlingTests(TestCase):
    def setUp(self):
        factory = RequestFactory()

        self.request = factory.post('/')

        class DummySerializer(serializers.Serializer):
            pass

        self.DummySerializer = DummySerializer

    def test_django_validation_error_from_service_is_transformed(self):
        serializer = self.DummySerializer
        error_message = 'error'

        def service_that_raises_django_validation_error():
            raise DjangoValidationError(message=error_message)

        class ApiUnderTest(GenericServiceApi):
            serializer_class = serializer

            def get_service(self):
                return service_that_raises_django_validation_error

            def get_response(self, service_result):
                return Response(status=status.HTTP_202_ACCEPTED)

        response = ApiUnderTest.as_view()(self.request)

        self.assertEqual(400, response.status_code)
        self.assertEqual(error_message, response.data[0])

    def test_permission_error_from_service_is_transformed(self):
        serializer = self.DummySerializer
        error_message = 'error'

        def service_that_raises_permission_denied():
            raise PermissionError(error_message)

        class ApiUnderTest(GenericServiceApi):
            serializer_class = serializer

            def get_service(self):
                return service_that_raises_permission_denied

            def get_response(self, service_result):
                return Response(status=status.HTTP_202_ACCEPTED)

        response = ApiUnderTest.as_view()(self.request)

        self.assertEqual(403, response.status_code)
        self.assertEqual(error_message, response.data['detail'])

    def test_value_error_from_service_is_transformed(self):
        serializer = self.DummySerializer
        error_message = 'error'

        def service_that_raises_value_error():
            raise ValueError(error_message)

        class ApiUnderTest(GenericServiceApi):
            serializer_class = serializer

            def get_service(self):
                return service_that_raises_value_error

            def get_response(self, service_result):
                return Response(status=status.HTTP_202_ACCEPTED)

        response = ApiUnderTest.as_view()(self.request)

        self.assertEqual(400, response.status_code)
        self.assertEqual(error_message, response.data[0])
