from django.db import models

class Jewel(models.Model):
    """
    Representation of a jewel. Used for the gallery.

    name: Jewel custom name.
    description: Short text for jewel details
    type: like "bague" | "collier".
    technique: Technique of jewel creation.
    image: Single image of the jewel.
    """
    type = models.ForeignKey("Type", null=True,
            on_delete=models.SET_NULL, verbose_name="Type")
    technique = models.ForeignKey("ManufacturingTechnique", null=True,
            on_delete=models.SET_NULL, blank=False,
            verbose_name="Technique de fabrication")
    description = models.TextField(blank=False, default="")
    image = models.ImageField(upload_to="img/", null=True)
    price = models.IntegerField(null=True, blank=True,
            verbose_name="Prix")
    reference = models.CharField(unique=True, blank=False, null=True, 
            max_length=10)
    
    class Meta:
        verbose_name = "Bijou"
        verbose_name_plural = "Bijoux"

    def to_json(self):
        """
        Transform the entire Jewel object in a dictionnary.
        """
        jewel_data = {
                "type" : self.type.name,
                "description" : self.description,
                "image" : self.image.url,
                "technique" : self.technique.name,
                "price" : self.price,
                "reference" : self.reference,
                }
        return jewel_data

    def __str__(self):
        if self.reference:
            return self.reference
        return "{} {}".format(self.__class__._meta.verbose_name, self.id)

# Specific fields attached to a single Jewel

class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom")

    class Meta:
        verbose_name = "Type"

    def __str__(self):
        return self.name

def pop_slice(lst, start=0, stop=None):
    """
    list.pop like function, but used with a slice.
    """
    if stop is None:
        stop = len(lst)
    sliced_list = lst[start:stop]
    del lst[start:stop]
    return sliced_list

class ManufacturingTechnique(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom")
    image = models.ImageField(upload_to="img/", null=True)

    class Meta:
        verbose_name = "Technique de fabrication"
        verbose_name_plural = "Techniques de fabrication"

    @classmethod
    def menu_columnize(cls, list_technique=None):
        """
        Group ManufacturingTechnique instance as a list of columns
        to facilitate their rendering in template.

        Balance them to be "intelligently" displayed, avoiding
        having a single technique in a bulma columns.

        Ex:
            with 6 technique, get:
                [
                    [0, 1, 2],
                    [3, 4, 5]
                ]

            with 7 technique:
                [
                    [0, 1, 2],
                    [3, 4],
                    [5, 6]
                ]
        """
        if list_technique is None:
            list_technique = list(cls.objects.all())
        final_display = []
        nbr_technique = len(list_technique)
        if nbr_technique == 0:
            return None
        if nbr_technique % 3 == 0 or nbr_technique >= 5:
            final_display.append(pop_slice(list_technique, 0, 3))
        else:
            final_display.append(pop_slice(list_technique, 0, 2))
        if len(list_technique) > 0:
            final_display.extend(cls.menu_columnize(list_technique))
        return final_display


    def __str__(self):
        return self.name
