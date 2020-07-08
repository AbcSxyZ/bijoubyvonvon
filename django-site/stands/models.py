from django.db import models
import datetime

class Stand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    latitude = models.FloatField(help_text="exemple de site: https://www.coordonnees-gps.fr/")
    longitude = models.FloatField()
    day = models.DateField(blank=False, verbose_name="Date")
    number_of_days = models.PositiveSmallIntegerField(default=1, blank=False,
            verbose_name="Nombre de jours")
    description = models.TextField(default='')
    weekly = models.BooleanField(default=False,
            verbose_name="Hebdomadaire")
    canceled = models.BooleanField(default=False,
            verbose_name="Annulé")

    DATE_FORMAT = "%-d/%-m/%Y"

    def __str__(self):
        return self.name

    def description_html(self):
        return self.description.replace("\n", "</br>")

    def date_render(self):
        """
        Render the string for the date range, according to the
        given day and the duration (in days) of the stand.

        Get format like :
            - "{self.DATE_FORMAT}"
            - "{self.DATE_FORMAT} au {self.DATE_FORMAT}"
        Depending if the stands is on mutliple days.

        """
        start_date = self.day.strftime(self.DATE_FORMAT)
        #Return only the day if it's only single day stand
        if self.is_single_day():
            return start_date

        #Return range date if it's on multiple days
        end_date_str = self.end_date.strftime(self.DATE_FORMAT)
        return "{} au {}".format(start_date, end_date_str)
    date_render.short_description = "Date"

    def is_single_day(self):
        """
        True if the stand durate only one day, False otherwise.
        """
        return self.number_of_days in [0, 1]

    @property
    def end_date(self):
        """
        Return a datetime corresponding to the end of the stand.
        """
        if self.is_single_day():
            return self.day
        duration = datetime.timedelta(days=self.number_of_days - 1)
        return self.day + duration


    def date_display(self):
        """
        Render the string whenever the stand date will be displayed.

        """
        event_format = self.date_render()
        if self.canceled:
            deleted_format = "<span class='deleted-event'>{}</span> (Annulé)"
            event_format = deleted_format.format(event_format)
        return event_format

    def is_stand_finish(self):
        """
        Check if the stand date is over
        """
        today = datetime.date.today()
        return today > self.end_date

    def get_next_date(self):
        """
        In case of a weekly event, calculate the next date.
        """
        return self.day + datetime.timedelta(days=7)

    @classmethod
    def manage_stand(cls):
        """
        Clear and/or update a stand if they are over.
        Re-create a new stand in case of weekly stand.
        """
        for stand in cls.objects.all():
            #Skip unfinished event
            if stand.is_stand_finish() is False:
                continue

            #Remove finished event if it's not repeated
            if stand.weekly == False:
                stand.delete()
            #Update event for the next time if it's weekly event
            else:
                stand.delete()
                stand.pk = None
                stand.canceled = False
                stand.day = stand.get_next_date()
                stand.save()
