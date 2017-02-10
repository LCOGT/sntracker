import requests
import logging
import json
from django.conf import settings

from observe.models import Supernova, Exposure

logger = logging.getLogger('supernova')

def submit_scheduler_api(params):
    '''
    Send the observation parameters and the authentication cookie to the Scheduler API
    '''
    headers = get_headers(mode='O')
    url = settings.SCHEDULE_API_URL
    request_data = {'request_data':json.dumps(params),'proposal':settings.PROPOSAL_CODE}
    r = requests.post(url, data=request_data, headers=headers)
    if r.status_code == 200:
        tracking_num = r.json()['id']
        logger.debug('Request submitted - %s' % tracking_num)
        return True, tracking_num
    else:
        logger.error("Could not send request: {}".format(r.content))
        return False, r.content

def get_headers(mode='O'):
    if mode == 'A':
        token = settings.ARCHIVE_TOKEN
        headers = {'Authorization': 'Token {}'.format(token)}
    elif mode == 'O':
        token = odin_headers()
        headers = {'Authorization': 'Bearer {}'.format(token)}
    return headers

def odin_headers():
        auth_data={
            'grant_type': 'password',
            'username': settings.PROPOSAL_USER,
            'password': settings.PROPOSAL_PASSWD,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET
        }
        response = requests.post(settings.OBSERVE_TOKEN_URL, data= auth_data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return False

def archive_headers(url):
    auth_data = {'username':settings.PROPOSAL_USER, 'password':settings.PROPOSAL_PASSWD}
    response = requests.post(settings.ARCHIVE_TOKEN_URL, data = auth_data)
    if response.status_code == 200:
        response = response.json()
    else:
        return False
    token = response.get('token')
    # Store the Authorization header
    return True

def format_request(supernova):

    exposures = Exposure.objects.filter(supernova=supernova)
    # this selects any telescope on the 1 meter network
    location = {
        'telescope_class' : exposures[0].aperture,
        }

    molecules = []
    for f in exposures:
        molecule = {
        'exposure_time'   : f.exposure_time,
        'exposure_count'  : f.repeats,
        'filter'          : f.filter_name,
        'fill_window'     : False,
        'type'            : 'EXPOSE',
        'instrument_name' : f.instrument,
        'ag_mode'         : 'OPTIONAL',
        }
        molecules.append(molecule)

    # define the target
    target = {
        'name'              : supernova.name,
        'type'              : 'SIDEREAL',
        'ra'                : supernova.ra,
        'dec'               : supernova.dec,
    }

    # this is the actual window
    window = {
          'start' : str(supernova.start),
          'end' : str(supernova.end)
    }

    request = {
    "constraints" : {'max_airmass' : 2.0},
    "location" : location,
    "molecules" : molecules,
    "observation_note" : "",
    "observation_type" : "NORMAL",
    "target" : target,
    "type" : "request",
    "windows" : [window],
    }

    user_request = {
    "operator" : "single",
    "requests" : [request],
    "type" : "compound_request",
    "ipp_value" : 1.0,
    # "group_id" : "Supernova_Tracker_%s" % supernova.name
    }
    return user_request
