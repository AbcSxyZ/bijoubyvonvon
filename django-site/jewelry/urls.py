from django.urls import path
from django.conf.urls.static import static

from . import views
from django.conf import settings

app_name = "jewelry"

urlpatterns = [
        path("", views.home, name="home"),
        path("jewels/", views.jewel_loader, name="jewels-load"),
        path("contact/", views.contact, name="contact-mail"),
        ]
