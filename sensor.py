from homeassistant.components.sensor import SensorEntity
from datetime import timedelta

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    # Add entities
    entities = [
        HG659UptimeSensor(client),
        HG659DeivceCountSensor(client),
        HG659ExternalIPAddrSensor(client)
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
        self._uptime = None

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._uptime = self._client.get_uptime()
            #self._state = self._client.get_uptime()
        except Exception as e:
            _LOGGER.warning(f"Failed to update uptime sensor: {e}")
            self._uptime = None
    
    @property
    def native_value(self):
        return self._uptime
    
    #@property
    #def state(self):
        #return self._state
    
    @property
    def available(self):
        return self.native_value is not None

class HG659DeivceCountSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 Device count"
        self._attr_unique_id = "hg659_device_count"
        #self._attr_native_value = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"
        self._active_devices = None
        self._device_count = None

    def update(self):
        """Fetch new state data from the router."""
        try:
            self._device_count = self._client.get_device_count()
            self._active_devices = self._client.get_active_devices()
        except Exception as e:
            _LOGGER.warning(f"Failed to update device count sensor: {e}")
            self._device_count = None
            self._active_devices = None
    
    @property
    def native_value(self):
        return self._device_count
    
    @property
    def extra_state_attributes(self):
        return {
            "Devices": [{
                "Hostname": d["HostName"],
                "IP Address": d["IPAddress"],
                "MAC Address": d["MACAddress"],
                "Connection Time": str(timedelta(seconds=int(d["LeaseTime"]))),
            } for d in self._active_devices] if not self._active_devices == None else "None"
        }

    @property
    def available(self):
        return self.native_value is not None

class HG659ExternalIPAddrSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "HG659 External IP Address"
        self._attr_unique_id = "hg659_external_ip_addr"
        self._external_ip = None
    
    def update(self):
        """Fetch new state data from the router."""
        try:
            self._external_ip = self._client.get_external_ip_addr()
        except Exception as e:
            _LOGGER.warning(f"Failed to update device count sensor: {e}")
            self._external_ip = None
    
    @property
    def native_value(self):
        return self._external_ip
    
    @property
    def available(self):
        return self.native_value is not None