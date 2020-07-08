from django.core.files.storage import FileSystemStorage
from django.conf import settings
from core import image

class JewelryFileStorage(FileSystemStorage):
    """
    Default FileSystemStorage for the website,
    configured with MEDIA_(URL|ROOT) variables.

    Resize all saved image.
    """
    @image.save_resized(*settings.DEFAULT_STORAGE_IMAGE_SIZE)
    def _save(self, name, content):
        return super()._save(name, content)
