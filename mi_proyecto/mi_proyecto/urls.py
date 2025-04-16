from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),  # Para las rutas de la aplicación polls
    path('', include('polls.urls')),  # Esto redirige la raíz '/' a las rutas de polls
]
