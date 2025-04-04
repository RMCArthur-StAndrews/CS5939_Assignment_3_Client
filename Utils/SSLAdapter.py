import requests
import ssl
import logging

class SSLAdapter(requests.adapters.HTTPAdapter):
    """
    Class handles the SSL/TLS settings for all requests to external cloud services.
    """
    def init_poolmanager(self, *args, **kwargs):
        """
        Initialize the pool manager with custom SSL settings.
        :param args: the arguments to pass to the parent class
        :param kwargs: the keyword arguments to pass to the parent class
        :return: instance of the pool manager
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Adjust SSL/TLS versions as needed
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

def make_request(method, url, **kwargs):
    """
    Wrapper function for making HTTP requests with custom SSL settings.
    :param method: HTTP method (e.g., 'get', 'post')
    :param url: URL to make the request to
    :param kwargs: Additional arguments to pass to the requests method
    :return: Response object
    """
    session = requests.Session()
    session.mount('https://', SSLAdapter())
    try:
        response = session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise