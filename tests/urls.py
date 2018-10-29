from django.conf.urls import include, url

from wagtail.admin import urls as admin_urls
from wagtail.core import urls as core_urls


urlpatterns = [
    url(r'^admin/', include(admin_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(core_urls)),
]
