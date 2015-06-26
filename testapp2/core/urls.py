from django.conf.urls import include, url


from .views import ArtigoUpdateView, ArtigoCreateView, ArtigoListView, RevisionView, RevisionView2, \
    ArtigoVersionListView

urlpatterns = [
    url(r'^list/$', ArtigoListView.as_view(), name='artigo_list'),
    url(r'^create/$', ArtigoCreateView.as_view(), name='artigo_create'),
    url(r'^update/(?P<pk>\d+)/$', ArtigoUpdateView.as_view(), name='artigo_update'),
    url(r'^revision/(?P<pk>\d+)/$', RevisionView.as_view(), name='artigo_revison'),
    url(r'^revision2/(?P<pk>\d+)/$', RevisionView2.as_view(), name='artigo_revison3'),
    url(r'^revision3/(?P<pk>\d+)/$', ArtigoVersionListView.as_view(), name='artigo_revison2')


]
