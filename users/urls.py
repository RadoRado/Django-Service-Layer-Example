from django.conf.urls import url

from .apis import CreateUserApi

urlpatterns = [
    url(
        regex=r'^create/$',
        name='create',
        view=CreateUserApi.as_view()
    )
]
