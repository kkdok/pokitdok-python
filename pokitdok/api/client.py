from __future__ import absolute_import
import json

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


class PokitDokClient(object):
    """
        PokitDok Platform API Client
        This class provides a wrapper around requests and requests-oauth
        to handle common API operations
    """
    def __init__(self, client_id, client_secret, base="https://platform.pokitdok.com", version="v3"):
        """
            Initialize a new PokitDok API Client

            :param client_id: The client id for your PokitDok Platform Application
            :param client_secret: The client secret for your PokitDok Platform Application
            :param base: The base URL to use for API requests.  Defaults to https://platform.pokitdok.com
        """
        self.headers = {
            'Content-type': 'application/json',
            'Content-type': 'application/json'
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_access_token = None
        self.url_base = "{0}/api/{1}".format(base, version)
        self.token_url = "{0}/oauth2/token".format(base)
        self.api_client = OAuth2Session(self.client_id, client=BackendApplicationClient(self.client_id))
        self.fetch_access_token()

    def fetch_access_token(self):
        """
            Retrieves an OAuth2 access token based on the supplied client_id and client_secret
            :returns: the client application's access token
        """
        return self.api_client.fetch_token(self.token_url, client_id=self.client_id, client_secret=self.client_secret)

    def activities(self, activity_id=None):
        """
            Fetch platform activity information
        """
        activities_url = "{0}/activities/{1}".format(self.url_base, activity_id if activity_id else '')
        return self.api_client.get(activities_url).json()

    def cash_prices(self):
        """
            Fetch cash price information
        """
        #TODO: support all query string possibilities
        cash_prices_url = "{0}/prices/cash/".format(self.url_base)
        return self.api_client.get(cash_prices_url).json()

    def claims(self, claims_request):
        """
            Submit a claims request

            :param claims_request: dictionary representing a claims request
        """
        claims_url = "{0}/claims/".format(self.url_base)
        return self.api_client.post(claims_url, data=json.dumps(claims_request), headers=self.headers).json()

    def claims_status(self, claims_status_request):
        """
            Submit a claims status request

            :param claims_status_request: dictionary representing a claims status request
        """
        claims_status_url = "{0}/claims/status/".format(self.url_base)
        return self.api_client.post(claims_status_url, data=json.dumps(claims_status_request),
                                    headers=self.headers).json()

    def eligibility(self, eligibility_request):
        """
            Submit an eligibility request

            :param eligibility_request: dictionary representing an eligibility request
        """
        eligibility_url = "{0}/eligibility/".format(self.url_base)
        return self.api_client.post(eligibility_url, data=json.dumps(eligibility_request), headers=self.headers).json()

    def enrollment(self, enrollment_request):
        """
            Submit a benefits enrollment/maintenance request

            :param enrollment_request: dictionary representing an enrollment request
        """
        enrollment_url = "{0}/enrollment/".format(self.url_base)
        return self.api_client.post(enrollment_url, data=json.dumps(enrollment_request), headers=self.headers).json()

    def files(self, trading_partner_id, x12_file):
        """
            Submit a raw X12 file to the platform for processing

            :param trading_partner_id: the trading partner that should receive the X12 file information
            :param x12_file: the path to a X12 file to be submitted to the platform for processing
        """
        files_url = "{0}/files/".format(self.url_base)
        return self.api_client.post(files_url,
                                    data={'trading_partner_id': trading_partner_id},
                                    files={'file': open(x12_file, 'rb')}).json()

    def providers(self, provider_id=None):
        """
            Fetch health care provider information
        """
        #TODO: support all query string parameters
        providers_url = "{0}/providers/{1}".format(self.url_base, provider_id if provider_id else '')
        return self.api_client.get(providers_url).json()