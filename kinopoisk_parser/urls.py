import re
from django.conf import settings
from django.urls.conf import include, re_path
from django.contrib import admin
from django.urls import path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
]

kwargs = {"document_root": settings.STATIC_ROOT}

urlpatterns.append(re_path(r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")), serve, kwargs=kwargs))
