"""Info Endpoint.
Querying the info endpoint reveals information about existing datasets in this beacon
and their associated metadata.
.. note:: See ``beacon_api`` root folder ``__init__.py`` for changing values used here.
"""

from typing import Dict
from .. import __apiVersion__, __title__, __version__, __description__, __url__, __alturl__, __handover_beacon__
from .. import __createtime__, __updatetime__, __org_id__, __org_name__, __org_description__
from .. import __org_address__, __org_logoUrl__, __org_welcomeUrl__, __org_info__, __org_contactUrl__
from .. import  __handover_drs__, __docs_url__, __service_type__, __service_env__

async def Bp_info(host: str) -> Dict:
    """Construct the `Beacon` app information dict in GA4GH Discovery format.
    :return beacon_info: A dict that contain information about the ``Beacon`` endpoint.
    """
    beacon_info = {
        # TO DO implement some fallback mechanism for ID
        "id": ".".join(reversed(host.split("."))),
        "name": __title__,
        "type": __service_type__,
        "description": __description__,
        "organization": {
            "name": __org_name__,
            "url": __org_welcomeUrl__,
        },
        "contactUrl": __org_contactUrl__,
        "documentationUrl": __docs_url__,
        "createdAt": __createtime__,
        "updatedAt": __updatetime__,
        "environment": __service_env__,
        "version": __version__,
    }
    return beacon_info