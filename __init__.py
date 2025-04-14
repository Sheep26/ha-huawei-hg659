# HG659 home assistant integration.
import logging
from typing import Final

_LOGGER = logging.getLogger(__name__)

DOMAIN = "huawei_hg659"

async def async_setup(hass, config):
    #hass.states.async_set("hello_state.world", "Paulus")
    
    # Setup component.
    return True