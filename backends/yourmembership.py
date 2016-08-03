import six

from social.p3 import urlencode, unquote
from social.utils import url_add_parameters, parse_qs, handle_http_errors
from social.exceptions import AuthFailed, AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter, AuthStateMissing, \
                              AuthStateForbidden, AuthTokenError
from social.backends.base import BaseAuth

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom.minidom import parseString
from xml.etree import ElementTree

from requests import request

import uuid

class YourMembershipAuth(BaseAuth):
    name = "yourmembership"
    REQUIRES_EMAIL_VALIDATION = False
    ID_KEY = "WebsiteID"
    EXTRA_DATA = [
        ('user_id', 'user_id'),
        ('session_id', 'SessionID')
    ]
    YMAPI_SERVLET_URI = "https://api.yourmembership.com/"
    YMAPI_VERSION = "2.03"

    def generate_request_xml(self, _call_method, _session_id="", _call_args={}):
        API_KEY, PRIVATE_KEY = self.get_key_and_secret()
        top = Element('YourMembership')

        version = SubElement(top, 'Version')
        version.text = self.YMAPI_VERSION

        apikey = SubElement(top, 'ApiKey')
        apikey.text = API_KEY
        
        callid = SubElement(top, 'CallID')
        callid.text = str(uuid.uuid4())[0:23]
        
        if _session_id:
            sessionid = SubElement(top, 'SessionID')
            sessionid.text = _session_id

        call = SubElement(top, "Call", {"Method": _call_method})

        if len(_call_args):
            for key, value in _call_args.items():
                call_arg = SubElement(call, key)
                call_arg.text = value
        
        return parseString(ElementTree.tostring(top)).toprettyxml()

    def call_api(self, _call_method, _session_id="", _call_args={}):
        data = self.generate_request_xml(_call_method, _session_id=_session_id, _call_args=_call_args)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'} 
    
        response = request("POST", self.YMAPI_SERVLET_URI, headers=headers, data=data)
        self.procees_error(response)
        parse = self.xml_parse(response)
        ym_response = parse.findall("./" + _call_method)[0]
        return_dict = {"call_method": _call_method}
        for node in ym_response:
            return_dict[node.tag] = node.text
        return return_dict

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        """Return access_token and extra defined names to store in
        extra_data field"""
        data = super(YourMembershipAuth, self).extra_data(user, uid, response, details,
                                                 *args, **kwargs)
        data['access_token'] = response.get('access_token', '') or \
                               kwargs.get('access_token')
        return data

    def procees_error(self, response):
        xmldoc = self.xml_parse(response)
        errcode = int(xmldoc.findall("./ErrCode")[0].text)
        ExtendedErrorInfo = xmldoc.findall("./ExtendedErrorInfo")
        errdesc = xmldoc.findall("./ErrDesc")
        if errcode == 0:
            return
        elif errcode == 999:
            raise AuthUnknownError(self, errdesc[0].text)
        elif errcode in [101, 102, 103, 201, 301, 404]:
            raise AuthMissingParameter(self, errdesc[0].text)
        elif errcode in [405]:
            raise AuthStateForbidden(self, errdesc[0].text)
        else:
            raise AuthUnknownError(self, errdesc[0].text)

    def create_session(self):
        return self.call_api("Session.Create")["SessionID"]

    def auth_url(self):
        """Return redirect url"""
        sessionID = self.create_session()
        self.strategy.session_set("ymsessionID", sessionID)
        data = self.call_api("Auth.CreateToken", sessionID, _call_args={"RetUrl": self.get_redirect_uri()})
        return data["GoToUrl"]

    @staticmethod
    def xml_parse(response):
        return ElementTree.fromstring(response.text)

    def get_redirect_uri(self):
        """Build redirect with redirect_state parameter."""
        uri = self.redirect_uri
        return uri


    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        sessionID = self.strategy.session_get("ymsessionID")
        if not sessionID:
            raise AuthStateMissing(self, "Missing Session ID.")

        response = self.call_api("Member.Profile.Get", sessionID)
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)


    def get_user_details(self, response):
        """Return user details
        """

        return {
            'username': response['Username'],
            'email': response["EmailAddr"],
            'fullname': response['LastName'] + response['FirstName'],
            'first_name': response['FirstName'],
            'last_name': response['LastName']
        }

    def get_user_id(self, details, response):
        """Return a unique ID for the current user, by default from server
        response."""
        return response["WebsiteID"]