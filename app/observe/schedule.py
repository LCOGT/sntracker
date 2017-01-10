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
    client = requests.session()

    url = 'https://lco.global/observe/auth/accounts/login/'
    r = requests.get(url)
    token = r.cookies['csrftoken']
    r = client.post(url, data={'username':settings.PROPOSAL_USER,'password':settings.PROPOSAL_PASSWD, 'csrfmiddlewaretoken' : token}, cookies={'csrftoken':token})
    url = 'https://lco.global/observe/service/request/submit'

    user_request = {'proposal': settings.PROPOSAL_CODE, 'request_data':params}
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
    # "group_id" : "Supernova_Tracker_%s" % supernova.name
    }
    return json.dumps(user_request)
