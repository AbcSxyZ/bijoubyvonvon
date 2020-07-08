from django.conf import settings
from core.custom_media import CustomMedia

def save_description(request):
    """
    Update the description file with the new content.
    """
    with open(settings.DESCRIPTION_FILE, 'w', encoding="utf8") as description_file:
        description_file.write(request.POST["description"])

def save_files(request):
    """
    Change images of the description from new POSTed files.

    Change : - profil
             - Banner
    """
    file_to_change = [
            (CustomMedia.get(settings.HEADER_IMAGE), "image_banner"),
            (CustomMedia.get(settings.PROFIL_IMAGE), "image_profil"),
            ]

    #Copy uploaded file to the server through the CustomMedia model
    for custom_media_inst, form_value in file_to_change:
        if request.FILES.get(form_value, None):
            new_upload = request.FILES[form_value]
            custom_media_inst.copy(new_upload)

