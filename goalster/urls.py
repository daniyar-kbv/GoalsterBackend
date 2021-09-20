from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/users/', include('users.urls')),
    url(r'^api/main/', include('main.urls')),
    url(r'^api/knowledge/', include('knowledge.urls')),
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.DOCUMENTS_URL, document_root=settings.DOCUMENTS_ROOT)

admin.site.index_title = ''
admin.site.site_header = _('24Goals admin panel')
admin.site.site_title = ''
