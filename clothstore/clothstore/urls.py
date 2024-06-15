from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import get_resolver
from pprint import pprint
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")), 
    path("auth/", include("userauth.urls")),
    path("cart/", include("cart.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    resolver = get_resolver()
    pprint(list(resolver.reverse_dict.keys()))