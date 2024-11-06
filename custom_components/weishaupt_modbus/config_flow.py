"""Config flow."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PREFIX
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
# from homeassistant.config_entries import ConfigFlowResult

# from . import wp
from .const import (
    CONST,
    CONF_DEVICE_POSTFIX,
    CONF_KENNFELD_FILE,
    CONF_HK2,
    CONF_HK3,
    CONF_HK4,
    CONF_HK5,
    CONF_NAME_DEVICE_PREFIX,
    CONF_NAME_TOPIC_PREFIX,
)

# DATA_SCHEMA = vol.Schema({("host"): str, ("port"): cv.port})
# The caption comes from strings.json / translations/en.json.
# strings.json can be processed into en.json with some HA commands.
# did not find out how this works yet.
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default="502"): cv.port,
        vol.Optional(CONF_PREFIX, default=CONST.DEF_PREFIX): str,
        vol.Optional(CONF_DEVICE_POSTFIX, default=""): str,
        vol.Optional(CONF_KENNFELD_FILE, default=CONST.DEF_KENNFELDFILE): str,
        vol.Optional(CONF_HK2, default=False): bool,
        vol.Optional(CONF_HK3, default=False): bool,
        vol.Optional(CONF_HK4, default=False): bool,
        vol.Optional(CONF_HK5, default=False): bool,
        vol.Optional(CONF_NAME_DEVICE_PREFIX, default=False): bool,
        vol.Optional(CONF_NAME_TOPIC_PREFIX, default=False): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the input."""
    # Validate the data can be used to set up a connection.

    # This is a simple example to show an error in the UI for a short hostname
    # The exceptions are defined at the end of this file, and are used in the
    # `async_step_user` method below.
    if len(data["host"]) < 3:
        raise InvalidHost

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    # "Title" is what is displayed to the user for this hub device
    # It is stored internally in HA as part of the device config.
    # See `async_step_user` below for how this is used
    return {"title": data["host"]}


class ConfigFlow(config_entries.ConfigFlow, domain=CONST.DOMAIN):
    """Class config flow."""

    VERSION = 4
    # Pick one of the available connection classes in homeassistant/config_entries.py
    # This tells HA if it should be asking for updates, or it'll be notified of updates
    # automatically. This example uses PUSH, as the dummy hub will notify HA of
    # changes.
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Step for setup process."""
        # This goes through the steps to take the user through the setup process.
        # Using this it is possible to update the UI and prompt for additional
        # information. This example provides a single form (built from `DATA_SCHEMA`),
        # and when that has some validated input, it calls `async_create_entry` to
        # actually create the HA config entry. Note the "title" value is returned by
        # `validate_input` above.
        errors = {}
        info = None
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)

            except Exception:  # noqa: BLE001
                errors["base"] = "unknown error"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Trigger a reconfiguration flow."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()
        myhostname = reconfigure_entry.data[CONF_HOST]
        # await self.async_set_unique_id(username)
        if user_input:
            return self.async_update_reload_and_abort(
                reconfigure_entry, data_updates=user_input
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                CONF_HOST: "myhostname",
            },
        )


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""


class ConnectionFailed(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
