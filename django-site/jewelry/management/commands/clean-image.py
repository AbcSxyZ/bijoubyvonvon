from jewelry.models import Jewel, ManufacturingTechnique
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

def retrieve_stored_image(directory):
    """
    Retrieve recursively all images stored in the VPS for the website,
    stocked in MEDIA_ROOT
    """
    list_images = []
    for filename in os.listdir(directory):
        filename = os.path.join(directory, filename)
        if os.path.isfile(filename):
            list_images.append(filename)
        elif os.path.isdir(filename):
            list_images.extend(retrieve_stored_image(filename))
    return set(list_images)



def retrieve_site_images():
    """
    Retrieve all absolute path of Jewel's and ManufacturingTechnique's
    images.
    """
    site_images = []
    for class_item in (Jewel, ManufacturingTechnique):
        list_instance = class_item.objects.all()
        item_imgs = [instance.image.path for instance in list_instance]
        site_images.extend(item_imgs)
    return set(site_images)


class Command(BaseCommand):
    help = "Remove unused image in MEDIA_ROOT folder"

    def handle(self, *args, **kwargs):
        """
        Delete stored file which are unused by the website.
        """
        stored_img = retrieve_stored_image(settings.MEDIA_ROOT)
        #Retrieve a set of unused files.
        diff_img = stored_img - retrieve_site_images()
        for to_delete_img in diff_img:
            os.unlink(to_delete_img)

