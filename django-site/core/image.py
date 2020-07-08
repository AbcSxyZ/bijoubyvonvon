from PIL import Image
import os

def save_resized(height, width, quality=90):
    """
    Decore a Storage._save function to resize
    all saved image.
    """
    def save_and_resize(function):
        def _save_wrapper(self, *args, **kwargs):
            filename = function(self, *args, **kwargs)
            abs_filename = os.path.join(self.location, filename)
            # WARNING : can have concurrence issue with apache
            # reading file.
            img = Image.open(abs_filename)
            img.thumbnail((height, width))
            img.save(abs_filename, quality=90)
            return filename
        return _save_wrapper
    return save_and_resize
