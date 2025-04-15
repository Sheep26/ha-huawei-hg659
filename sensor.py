from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from datetime import timedelta

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    # Create and add entities
    entities = [HG659UptimeSensor(client), HG659DeivceCountSensor(client)]
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
        if self._state is None:
            return None
        return str(timedelta(seconds=self._state))

class HG659DeivceCountSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Device count"
        self._attr_unique_id = "hg659_device_count"
        self._state = None

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._state = self._client.get_device_count()
        except Exception as e:
            _LOGGER.warning(f"Failed to update device count sensor: {e}")

    @property
    def state(self):
        return self._state