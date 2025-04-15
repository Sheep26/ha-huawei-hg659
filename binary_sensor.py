from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    # Add entities
    entities = [
        HG659OnlineSensor(client),
    ]
    
    async_add_entities(entities)

class HG659OnlineSensor(BinarySensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Connected"
        self._attr_unique_id = "hg659_connected"
        self._attr_device_class = "connectivity"
        self._attr_is_on = None

    async def async_update(self):
        """Fetch new state data from the router asynchronously."""
        try:
            self._attr_is_on = await self._client.get_connected()
        except Exception as e:
            _LOGGER.warning(f"Failed to update HG659 online sensor: {e}")