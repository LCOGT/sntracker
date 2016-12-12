import requests
import logging
import json
from django.conf import settings

from observe.models import Supernova

logger = logging.getLogger('supernova')

def submit_scheduler_api(params):
    '''
    Send the observation parameters and the authentication cookie to the Scheduler API
    '''
    client = requests.session()

    url = 'https://lco.global/observe/auth/accounts/login/'
    r = requests.get(url)
    token = r.cookies['csrftoken']
    r = client.post(url, data={'username':settings.PROPOSAL_USER,'password':settings.PROPOSAL_PASSWD, 'csrfmiddlewaretoken' : token}, cookies={'csrftoken':token})
    url = 'https://lco.global/observe/service/request/submit'

    user_request = {'proposal': 'LCOEPO2014B-010', 'request_data':params}
    r = client.post(url, data=user_request, cookies=client.cookies)
    client.close()
    if r.status_code == 200:
        tracking_num = r.json()['id']
        logger.debug('Request submitted - %s' % tracking_num)
        return True, tracking_num
    else:
        logger.error(r.content)
        return False, r.content

def get_headers(url):
    auth_data = {'username':settings.PROPOSAL_USER, 'password':settings.PROPOSAL_PASSWD}
    response = requests.post(url, data = auth_data).json()
    token = response.get('token')
    # Store the Authorization header
    headers = {'Authorization': 'Token {}'.format(token)}
    return headers

def format_request(supernova):

    # this selects any telescope on the 1 meter network
    location = {
        'telescope_class' : filters[0].aperture,
        }

    molecules = []
    for f in filters:
        molecule = {
          # Required fields
        'exposure_time'   : f.exposure,  # Exposure time, in secs
        'exposure_count'  : f.repeats,  # The number of consecutive exposures
        'filter'          : f.filter_name,  # The generic filter name
        # Optional fields. Defaults are as below.
        # fill_window should be defined as True on a maximum of one molecule per request, or you should receive an error when scheduling
        'fill_window'     : False, # set to True to cause this molecule to fill its window (or all windows of a cadence) with exposures, calculating exposure_count for you
        'type'            : 'EXPOSE',  # The type of the molecule
        'ag_name'         : '',  # '' to let it resolve; same as instrument_name for self-guiding
        'ag_mode'         : 'Optional',
        'instrument_name' : supernova.instrument,  # This resolves to the main science camera on the scheduled resource
        'bin_x'           : supernova.binning,  # Your binning choice. Right now these need to be the same.
        'bin_y'           : supernova.binning,
        'defocus'         : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
        }
        molecules.append(molecule)

    # define the target
    target = {
        'name'              : supernova.name,
        'type'              : 'SIDEREAL',

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
    # "group_id" : "Supernova_Tracker_%s" % supernova.name
    }
    return json.dumps(user_request)
