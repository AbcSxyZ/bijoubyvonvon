from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminException(Exception):
    """Base exception for all error on the CustomAdmin site."""
    pass

class CustomAdminView:
    """
    Represent a single view with all of his data.
    Wrapper when a view is added to the CustomAdmin
    """
    def __init__(self, url, view, name, verbose):
        self.url = url
        self.view = view
        self.name = name
        self.verbose = verbose

    def as_path(self):
        return path(self.url, self.view, name=self.name)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value


class CustomAdmin(admin.AdminSite):
    """
    AdminSite with a custom list of view created
    by the user.
    
    Those view are useful to manipulate some information
    such as file, a view non-related to a model/app.
    """
    index_template = "admin/index_custom.html"
    app_label = "custom-admin"
    custom_app_name = "Admin"
    custom_views = []

    class Meta:
        app_label = "custom-admin"
        object_name = "None"

    def get_urls(self):
        """
        Extend admin urls with the list of available custom view.
        """
        urlspattern = super().get_urls()
        for view in self.custom_views:
            urlspattern.append(view.as_path())
        return urlspattern

    def add_view_context(self, view, verbose=None):
        """
        Wrapper for view to add an admin context.
        This configuration must be set mainly to fit
        contrib.admin templates.
        """
        def view_wrapper(request, *args, **kwargs):
            """
            Run the view, and add extra context to a TemplateResponse.

            The view must return a 
            django.template.response.TemplateResponse.
            """
            response = view(request, *args, **kwargs)
            admin_context = {
                    **self.each_context(request),
                    "opts":self.Meta,
                    'add':False,
                    'change': True,
                    'is_popup': False,
                    'save_as': False,
                    'has_delete_permission': False,
                    'has_add_permission': False,
                    'has_change_permission': True,
                    'has_view_permission': False,
                    'has_editable_inline_admin_formsets':False,
                    'title': verbose,
                    }

            # Make sure the view return a TemplateResponse to allow
            # extension of the context with the AdminSite
            if isinstance(response, TemplateResponse):
                view_context = response.context_data or {}
                admin_context = {**admin_context, **view_context}
                response.context_data = admin_context
                return response
            err_msg = "View must return a TemplateResponse. Get {}"
            raise CustomAdminException(err_msg.format(type(response)))
        return view_wrapper

    def add_view(self, url, view, name=None, verbose=None):
        """
        Interface to add a custom view the admin site.
        """
        if verbose == None:
            err_msg = "A new view must have verbose argument."
            raise CustomAdminException(err_msg)

        #Decorate the view, to add custom context, 
        #and to perform default admin checks
        view = self.add_view_context(view, verbose)
        view = self.admin_view(view)
        view = CustomAdminView(url, view, name, verbose)

        self.custom_views.append(view)
    
    def index(self, *args, **kwargs):
        """
        View called for the admin index. Extend context
        with all view's urls.
        """
        context = {
                "custom_views" : self.custom_views,
                "custom_app_name" : self.custom_app_name,
                }

        #Use extra_context kwargs of the AdminSite.index view
        #to send extra context. Save default extra context
        #in the current new one.
        if kwargs.get("extra_context"):
            context = {**kwargs["extra_context"], **context}
        kwargs["extra_context"] = context

        return super().index(*args, **kwargs)

site = CustomAdmin()
