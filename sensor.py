from homeassistant.helpers.entity import Entity
from homeassistant.const import DEVICE_CLASS_TIMESTAMP
from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    # Create and add entities
    entities = [HG659UptimeSensor(client)]
    async_add_entities(entities)

class HG659UptimeSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Uptime"
        self._attr_unique_id = "hg659_uptime"
        self._state = None

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._state = self._client.get_uptime()
        except Exception as e:
            _LOGGER.warning(f"Failed to update uptime sensor: {e}")

    @property
    def state(self):
        return self._state