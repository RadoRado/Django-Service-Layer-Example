from django.core.exceptions import ImproperlyConfigured


class ServiceFactoryMixin:
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        get_service = getattr(cls, 'get_service', None)

        if get_service is None:
            raise ImproperlyConfigured(
                'Provide get_service classmethod in factory.'
            )

        service = cls.get_service()

        if service is None:
            raise ImproperlyConfigured(
                'get_service returned None. Should return service intead.'
            )

        return service(**kwargs)
