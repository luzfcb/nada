from django.conf.urls import include, url


from .views import ArtigoUpdateView, ArtigoCreateView, ArtigoListView, RevisionView

urlpatterns = [
    url(r'^list/$', ArtigoListView.as_view(), name='artigo_list'),
    url(r'^create/$', ArtigoCreateView.as_view(), name='artigo_create'),
    url(r'^update/(?P<pk>\d+)/$', ArtigoUpdateView.as_view(), name='artigo_update'),
    url(r'^revision/(?P<pk>\d+)/$', RevisionView.as_view(), name='artigo_revison')


]
