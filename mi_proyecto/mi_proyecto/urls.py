from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),  # Incluir las URLs de la aplicación polls
    path('admin/', admin.site.urls),
]
