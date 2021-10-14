import logging
import voluptuous as vol

from homeassistant.components.device_tracker import (
    DOMAIN,
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    DeviceScanner,
)
from homeassistant.helpers.device_registry import format_mac
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv

from .client import HG659Client


_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PARENT_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
    }
)


def get_scanner(hass, config):
    _LOGGER.info("Setting up HG659DeviceScanner")
    scanner = HG659DeviceScanner(config[DOMAIN])
    _LOGGER.info("HG659DeviceScanner connected")
    return scanner


class HG659DeviceScanner(DeviceScanner):
    def __init__(self, config):
        super().__init__()
        _LOGGER.debug("Initiating HG659 client")
        self.client = HG659Client(
            host=config[CONF_HOST],
            username=config[CONF_USERNAME],
            password=config[CONF_PASSWORD],
        )
        _LOGGER.debug("HG659 client initiated")
        self._devices = dict()

    def scan_devices(self):
        try:
            _LOGGER.debug("Logging in to router")
            output = self.client.login()
            _LOGGER.debug(f"Logged in, output: {output}")
            _LOGGER.debug(f"Getting devices")
            devices_router = self.client.get_devices()
            _LOGGER.debug(f"Got {len(devices_router)} active + inactive devices")
        finally:
            # Don't forget to logout since otherwise the web interface
            # will be blocked for the user
            status = self.client.logout()
            _LOGGER.debug(f"Logged out (status: {status})")

        devices_hass = [
            dict(
                id=format_mac(d["MACAddress"]),
                source_type="router",
                is_connected=d["Active"],
                ip_address=d["IPAddress"],
                mac_address=d["MACAddress"],
                hostname=d["HostName"],
            )
            for d in devices_router
            if d["Active"]  # only include active devices
        ]
        _LOGGER.debug(f"{len(devices_hass)} devices were active")
        self._devices = {d["mac_address"]: d for d in devices_hass}
        return list(self._devices.keys())

    def get_device_name(self, device: str):
        d = self._devices.get(device)
        if d:
            return d["hostname"]

    def get_extra_attributes(self, device: str):
        return self._devices.get(device)
