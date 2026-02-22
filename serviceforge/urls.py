from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobcards.urls')),
    path('clients/', include('clients.urls')),
    path('users/', include('users.urls')),
]
