from django.conf import settings
import os
import glob
from django.db import models
from django.core.files.storage import FileSystemStorage
from core import image

class CustomMediaPatternError(Exception):
    """Raise when the custom media pattern give an invalid match."""
    pass

class CustomMediaManager(models.Manager):
    def get_or_create(self, pattern=None):
        """
        Override Manager.get_or_create method. On model
        creation, retrieve the associated filename and
        save it into the database.
        """
        retrieved, created = super().get_or_create(pattern=pattern)
        if created:
            filename = retrieved.__class__._retrieve_filename(pattern)
            retrieved.filename.name = filename
            retrieved.save()
        return retrieved
        
class CustomMediaStorage(FileSystemStorage):
    """
    FileSystemStorage for the CustomMedia model.
    """
    def __init__(self, *args, **kwargs):
        """
        Use CUSTOM_MEDIA_(ROOT|URL) settings to configure
        the storage by default.
        """
        if not kwargs.get("location", None):
            kwargs["location"] = settings.CUSTOM_MEDIA_ROOT
        if not kwargs.get("base_url", None):
            kwargs["base_url"] = settings.CUSTOM_MEDIA_URL
        super().__init__(*args, **kwargs)

    @image.save_resized(*settings.CUSTOM_STORAGE_IMAGE_SIZE)
    def _save(self, name, content):
        """ Change image dimension on when saving a file. """
        self.delete(name)
        return super()._save(name, content)

class CustomMedia(models.Model):
    """
    Represent an editable file from the server.
    Manage a separate directory for this kind of file.
    """
    #Custom settings
    STORAGE = CustomMediaStorage()
    objects = CustomMediaManager()

    #Model Fields
    filename = models.FileField(null=True, storage=STORAGE)
    pattern = models.CharField(max_length=255, null=False, unique=True)

    @classmethod
    def _retrieve_filename(cls, pattern):
        """Retrieve the absolute path of the custom file"""
        absolute_pattern = os.path.join(cls.STORAGE.location, pattern)
        list_match = glob.glob(absolute_pattern)

        #Make sure we have only a single file in the match.
        if len(list_match) != 1:
            msg = "Invalid match for pattern '{}' : {}."
            raise CustomMediaPatternError(msg.format(pattern, list_match))
        #Format the filename, make it relative to the storage,
        #and remove leading slash if necessary
        filename = list_match[0].replace(cls.STORAGE.location, "")
        if filename[0] == "/":
            filename = filename[1:]
        return filename

    @classmethod
    def get_filename(cls, pattern):
        """Retrieve absolute filename from pattern."""
        return cls.get(pattern).filename.path

    @classmethod
    def get_url(cls, pattern):
        """Retrieve url from pattern."""
        return cls.get(pattern).filename.url

    @classmethod
    def get(cls, pattern):
        """ Create or retrieve a CustomMedia from a given pattern """
        obj =  cls.objects.get_or_create(pattern)
        return obj

    def copy(self, new_file):
        """
        Copy a given django File object to replace the content
        of a CustomMedia file.
        """
        old_basename = self.filename.name.split(".")[:-1]
        old_basename = ".".join(old_basename)
        new_extension = new_file.name.split(".")[-1]
        new_filename = old_basename + "." + new_extension
        self.filename.delete()
        self.filename.save(new_filename, new_file)
