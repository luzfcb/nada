from django.conf.urls import include, url

from . import documento_views

urlpatterns = [
    url(r'^list/$',
        documento_views.DocumentoListView.as_view(),
        name='documento_list'
        ),
    url(r'^create/$',
        documento_views.DocumentoCreateView.as_view(),
        name='documento_create'
        ),
    url(r'^update/(?P<pk>\d+)/$',
        documento_views.DocumentoUpdateView.as_view(),
        name='documento_update'
        ),
    url(r'^versions/(?P<pk>\d+)/$',
        documento_views.DocumentoVersionsView.as_view(),
        name='documento_versions'
        ),
]
