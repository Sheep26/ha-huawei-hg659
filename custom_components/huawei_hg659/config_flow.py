import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectTimeout
import logging

from .const import DOMAIN

from .client import HG659Client

_LOGGER = logging.getLogger(__name__)

class HuaweiHG659ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input):
        """Handle the initial step."""
        errors = {}
        
        # Check if user input exists.
        if user_input is not None:
            try:
                # Attempt to login, we use self.hass.async_add_executer_job because we are running sync http requests in an async context.
                login_data = await self.hass.async_add_executor_job(lambda: self._create_client(user_input))
                
                # Check if login data ok.
                if login_data["errorCategory"] == "ok":
                    # Create entry.
                    return self.async_create_entry(
                        title=f"HG659 @ {user_input[CONF_HOST]}",
                        data=user_input
                    )
                else:
                    errors[CONF_PASSWORD] = "Invalid username or password."
                    _LOGGER.error("Invalid username or password")
            except (TimeoutError, MaxRetryError, ConnectTimeout):
                errors[CONF_HOST] = "Invalid host."
                _LOGGER.error("Invalid host.")
            except Exception as e:
                _LOGGER.error("Unknown error.")
                _LOGGER.error(e)
                errors["_base"] = "Unknown error."

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors
        )
    
    def _create_client(self, user_input):
        # Create client.
        client = HG659Client(user_input[CONF_HOST], user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
        # Attempt to login.
        login_data = client.login()
        # Attempt to logout.
        client.logout()
        
        # Return data.
        return login_data