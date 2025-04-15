from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    # Add entities
    entities = [
        HG659UptimeSensor(client),
        HG659DeivceCountSensor(client),
        HG659ExternalIPAddr(client)
    ]
    
    async_add_entities(entities)

class HG659UptimeSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Uptime"
        self._attr_unique_id = "hg659_uptime"
        #self._state = None
        self._attr_native_unit_of_measurement = "s"
        self._attr_suggested_unit_of_measurement = "d"
        self._attr_device_class = "duration"
        self._attr_state_class = "measurement"
        self._attr_native_value = None

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._attr_native_value = self._client.get_uptime()
            #self._state = self._client.get_uptime()
        except Exception as e:
            _LOGGER.warning(f"Failed to update uptime sensor: {e}")
            self._attr_native_value = None

    #@property
    #def state(self):
        #return self._state
    
    @property
    def available(self):
        return self._attr_native_value is not None

class HG659DeivceCountSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Device count"
        self._attr_unique_id = "hg659_device_count"
        self._attr_native_value = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._attr_native_value = self._client.get_device_count()
        except Exception as e:
            _LOGGER.warning(f"Failed to update device count sensor: {e}")
            self._attr_native_value = None

    @property
    def available(self):
        return self._attr_native_value is not None

class HG659ExternalIPAddr(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 External IP Address"
        self._attr_unique_id = "hg659_external_ip_addr"
        self._attr_native_value = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"
    
    def update(self):
        """Fetch new state data from the router."""
        try:
            self._attr_native_value = self._client.get_external_ip_addr()
        except Exception as e:
            _LOGGER.warning(f"Failed to update device count sensor: {e}")
            self._attr_native_value = None
    
    @property
    def available(self):
        return self._attr_native_value is not None