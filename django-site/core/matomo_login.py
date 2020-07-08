import sys
from http.client import HTTPSConnection, CannotSendRequest
import re
from http.cookies import SimpleCookie
from html.parser import HTMLParser
import urllib.parse as urllib
import ssl

class MatomoUserException(Exception):
    """Common exception raise for all error with MatomoUser"""
    pass

class NonceExtractor(HTMLParser):
    """
    Retrieve the input hidden field for the form Nonce for Matomo Login
    """
    def handle_starttag(self, tag, attr):
        attr = {key:value for key, value in attr}
        self.nonce = {attr['name'] : attr["value"]}

class MatomoUser:
    """
    Utils for trying an automatic connection to matomo
    whenver a admin is loggin into django's admin interface.

    Matomo and django admin sharing the same username/password
    to perform this.
    """
    SITE = "matomo"
    def __init__(self, username, password):
        self.nonce = None
        self.user = username
        self.password = password
        self._cookie = SimpleCookie()

        #SECURITY ISSUE:
        # - certificate not checked, can lead to man in the middle attack
        self.connection = HTTPSConnection(self.SITE,
                context=ssl.SSLContext())
        self._retrieve_session_cookie()
        self.login()

    def request(self, method, url, body=None, headers={}, read=False):
        """
        Hook to perform request with http.client.
        """
        #Try to add session cookie if already available.
        try:
            headers['Cookie'] = self.matomo_session
        except KeyError:
            pass

        #Format post data.
        if type(body) is dict:
            body = urllib.urlencode(body)

        #Add website root if needed
        if url[0] != "/":
            url = "/" + url

        #Send the request to website
        self.connection.request(method, url, \
                body=body, headers=headers)

        #Return the request response
        response = self.connection.getresponse()
        if read:
            response.read()
        return response

    def _retrieve_session_cookie(self):
        """
        Use to retrieve default data to login.
        Retrieve the MATOMO_SESSID cookie and the
        hidden form input login_form_nonce.
        """
        response = self.request("GET", "/")
        html_page = response.read().decode()

        if response.status != 200:
            raise MatomoUserException("Unable to connect to matomo site")
        #Retrieve <form> nonce of matomo
        pattern = "<input .*login_form_nonce.*?>"
        input_tag = re.search(pattern, html_page)
        if input_tag is None:
            raise MatomoUserException("login_form_nonce not found.")
        #Retrieve form nonce value
        parser = NonceExtractor()
        parser.feed(input_tag.group(0))
        self.nonce = parser.nonce
        self._cookie.load(response.headers['Set-Cookie'])

    def login(self):
        """
        Login user to matomo.
        """
        post_data = {
                "form_login" : self.user,
                "form_password" : self.password,
                **self.nonce,
                }
        headers = {
                "Content-Type" : "application/x-www-form-urlencoded",
                }
        response = self.request("POST", "/?module=Login", \
                post_data, headers, read=True)
        self._cookie.load(response.headers['Set-Cookie'])

    @property
    def matomo_session(self):
        """
        Get current MATOMO_SESSID cookie formated for http
        request
        """
        return "MATOMO_SESSID={}".format(self.cookie)

    @property
    def cookie(self):
        return self._cookie['MATOMO_SESSID'].value
