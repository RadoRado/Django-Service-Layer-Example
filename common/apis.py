from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView

from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework.exceptions import PermissionDenied as DrfPermissionDenied


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


class GenericServiceApi(GenericAPIView):
    expected_exceptions = {
        # Python errors here:
        ValueError: DrfValidationError,
        # Django errors here:
        ValidationError: DrfValidationError,
        PermissionError: DrfPermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)

    def get_service(self):
        raise NotImplemented()

    def get_response(self):
        raise NotImplemented()

    def transform_serializer_data(self, serializer):
        return serializer.validated_data

    def call_service(self, **service_data):
        service = self.get_service()

        return service(**service_data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_data = self.transform_serializer_data(serializer)
        service_call_result = self.call_service(**service_data)

        response = self.get_response(service_call_result)

        return response
