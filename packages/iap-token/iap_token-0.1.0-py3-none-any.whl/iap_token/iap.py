import os, sys
from google.oauth2 import id_token
from google.auth.transport.requests import Request as AuthRequest
import mlflow

from pathlib import Path
from subprocess import check_output
import six
import requests
import logging

def get_token(request_uri: str = None):
    """Set valid service-account path to 'GOOGLE_APPLICATION_CREDENTIALS' envvar """
    try:
        redirect_response = requests.get(request_uri, allow_redirects=False)
        redirect_location = redirect_response.headers.get("location")
        parsed = six.moves.urllib.parse.urlparse(redirect_location)
        query_string = six.moves.urllib.parse.parse_qs(parsed.query)
        client_id = query_string["client_id"][0]

        response_id_token = id_token.fetch_id_token(
            AuthRequest(), client_id or os.environ.get("MLFLOW_OAUTH2_CLIENT_ID", "")
        )
        return response_id_token
    except Exception as e:
        logger.debug(e)
        logger.warning("Continue without authentication")


