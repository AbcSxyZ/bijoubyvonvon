from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.db import models
from django.conf import settings
from .models import Jewel, Type, ManufacturingTechnique
from .forms import DescriptionForm
from .filter_jewels import control_search, retrieve_searched_jewel
from .utils import description_loader, mailing
from .description import save_description, save_files
from stands.models import Stand
from core.custom_media import CustomMedia
from django.contrib import messages
import json

def admin_description(request):
    """
    Edit the description of the website through the administration
    panel.
    """
    # Save edited file/content on POST
    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            save_description(request)
            save_files(request)
        messages.success(request, "Modifications prises en compte.")

    # Prepare display of default value for description.
    with open(settings.DESCRIPTION_FILE, 'r', encoding='utf-8') as description_file:
        description = description_file.read()
    header = CustomMedia.get(settings.HEADER_IMAGE).filename
    profil = CustomMedia.get(settings.PROFIL_IMAGE).filename
    initial_data_form = {
            "description": description,
            "image_banner": header,
            "image_profil": profil,
            "image_profil": profil,
            }

    # Setup form with initial data prepared above for the context
    context= {"form": DescriptionForm(initial=initial_data_form)}
    return TemplateResponse(request, "admin/description.html", context)

def jewel_loader(request):
    """
    Retrieve jewels, according the specified filters.
    Display jewels in JSON format.
    """
    json_jewels = []
    request.GET = request.GET.copy()
    if control_search(request.GET) is False:
        raise Http404("Invalid filters")
    for jewel in retrieve_searched_jewel(request.GET):
        json_jewels.append(jewel.to_json())
    response = HttpResponse(json.dumps(json_jewels))
    response.content_type = "text/plain; charset=utf-8"
    return response

def home(request):
    description = description_loader()
    context = {
        "stands" : Stand.objects.all().order_by("day"),
        "techniques" : ManufacturingTechnique.objects.all(),
        "columns_techniques": ManufacturingTechnique.menu_columnize(),
        "types" : Type.objects.all(),
        "description": description_loader(),
        "hero_img" : CustomMedia.get_url(settings.HEADER_IMAGE),
        "about_img" : CustomMedia.get_url(settings.PROFIL_IMAGE),
            }
    return render(request, "jewelry/home.html", context)

def contact(request):
    """
    Send an email from data with contact form.
    """
    if request.method == "POST":
        mailing(request.POST)
        return HttpResponse("mail sended");
    raise Http404("Invalid request")
