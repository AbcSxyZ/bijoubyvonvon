from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import sys, os, getpass
import traceback
import datetime

class ExceptionMiddleware(MiddlewareMixin):
    """
    Handle exception and print them into a logfile,
    given by LOG_FILE settings variable.
    """
    def process_exception(self, request, exception):
        with open(settings.LOG_FILE, "a") as log_file:
            print(datetime.datetime.now(), ":", file=log_file)
            traceback.print_exc(file=log_file)
        return None
