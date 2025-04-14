# HG659 home assistant integration.
import logging
from typing import Final
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, DOMAIN

from .client import HG659Client

_LOGGER = logging.getLogger(__name__)

DOMAIN = DOMAIN
client: HG659Client

async def async_create_entry(hass, config):
    
    
    # Setup component.
    return True