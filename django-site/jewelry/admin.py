from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib.auth import authenticate
from django.contrib import messages
from core import admin
from .models import Jewel, Type, ManufacturingTechnique
from .views import admin_description
from core.matomo_login import MatomoUser, MatomoUserException

class JewelAdmin(ModelAdmin):
    list_display = ("type", "technique", "image", "price", \
            "reference")
    search_fields = ["reference"]

#Add Custom models
admin.site.register(Type)
admin.site.register(Jewel, JewelAdmin)
admin.site.register(ManufacturingTechnique)

# Change website verbose
admin.site.site_header = "Bijou Bijou by Vonvon | Administration"
admin.site.site_title = "Bijou Bijou by Vonvon"

# Add view to admin website
admin.site.add_view("edit", admin_description, "description",
        "Description")

matomo_url = "https://{}/".format(settings.MATOMO_DOMAIN_PATH)
admin.site.add_view(matomo_url, None, \
        verbose="Matomo")

def custom_login(request, *args, **kwargs):
    """
    Override admin login view, try to connect
    logged admin in django to matomo server.

    Matomo and django share same username/password,
    to avoid mutliple password.
    """
    user = None
    #Try to connect to Matomo on POST request.
    if request.method == "POST":
        user_credential = {
                'username' : request.POST["username"],
                'password' : request.POST["password"],
        }
        #Verify if the admin user exists before trying
        #to log into matomo.
        if authenticate(**user_credential):
            try:
                user = MatomoUser(**user_credential)
            #Log can fail, and user have to login into
            #matomo with his credential.
            except MatomoUserException:
                msg = "Echec de la connexion automatique " + \
                      "à Matomo, veuillez vous connecter manuellement."
                messages.error(request, msg)

    response = super(type(admin.site), admin.site).\
            login(request, *args, **kwargs)
    if user is not None:
        response.set_cookie("MATOMO_SESSID", user.cookie)
    return response

admin.site.login = custom_login
