from django.conf.urls import url, include
from django.contrib import admin
from .app.qa import views,urls as qaurls
from .app.cluster import urls as clusterurls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^qasystem/', include(qaurls)),
    url(r'^cluster/', include(clusterurls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

