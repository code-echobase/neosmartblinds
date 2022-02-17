"""Support for NeoSmartBlinds covers."""
import logging

import requests
import voluptuous as vol

from homeassistant.components.cover import (
    PLATFORM_SCHEMA,
    CoverEntity,
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
    SUPPORT_STOP,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_NAME,
    CONF_HOST,
    CONF_ID,
    CONF_DEVICES,
)

from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)
supported_features = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP

# api call is http://{ip address}:8838/neo/v1/transmit?command={blind id}-{command}&id={controller id (24 chars)}'
# commands are up (UP), dn (DOWN) and sp (STOP)

############
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_ID): cv.string,
        vol.Optional(CONF_DEVICES, default={}): {
            cv.string: vol.Schema({vol.Required(CONF_NAME): cv.string,})
        },
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the NEOSMARTBLINDS global variables."""
    controller_host = config.get(CONF_HOST)
    controller_id = config.get(CONF_ID)
    """Set up the NEOSMARTBLINDS covers."""
    covers = []
    devices = config.get(CONF_DEVICES)
    if devices:
        for _, entity_info in devices.items():
            name = entity_info.get(CONF_NAME)
            id = _
            _LOGGER.info("Adding %s neosmartblinds cover", name, " ", id)
            cover = NeoSmartBlindsCover(
                hass,
                id=id,
                name=name,
                controller_host=controller_host,
                controller_id=controller_id,
            )
            covers.append(cover)

    if not covers:
        _LOGGER.error("No covers added")
        return False

    add_entities(covers)


#########################
class NeoSmartBlindsCover(CoverEntity):
    """Representation of NEOSMARTBLINDS cover."""

    def __init__(self, hass, name, controller_host, id, controller_id):
        """Initialize the cover."""
        self._id = id
        self._hass = hass
        self._name = name
        self._controller_host = controller_host
        self._controller_id = controller_id
        self._available = True
        self._device_class = None
        self._is_closed = None
        self._state = None

    @property
    def should_poll(self):
        """Return the polling state. No polling available from controller."""
        return False

    @property
    def name(self):
        """Return the name of the cover."""
        return self._name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def is_closed(self):
        """Return None as no state from controller."""
        return None

    @property
    def id(self):
        """Return the id of the cover."""
        return self._id

    @property
    def name(self):
        """Return the name of the cover."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique id for the entity"""
        return "neosmartblinds" + "." + self._id 

    @property
    def should_poll(self):
        """Return the polling state. No polling available from controller."""
        return False

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def is_closed(self):
        """Return None as no state from controller."""
        return None

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return self._device_class

    @property
    def supported_features(self):
        """Flag supported features."""
        return supported_features

    def close_cover(self, **kwargs):
        """Close the cover."""
        self.move_cover(self, command="dn")

    def open_cover(self, **kwargs):
        """Open the cover."""
        self.move_cover(self, command="up")

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self.move_cover(self, command="sp")

    @staticmethod
    def move_cover(self, command):
        """Build the uri and execute the actual commands."""
        httpuri = f"http://{self._controller_host}:8838/neo/v1/transmit?command={self._id}-{command}&id={self._controller_id}"
        request = requests.get(httpuri)
        if request.status_code != 200:
            if request.status_code == "400":
                response = "400: Blind ID incorrect"
            elif request.status_code == "401":
                response = "401: Controller ID incorrect"
            else:
                response = request.status_code

            _LOGGER.debug(
                "Error executing: %s %s-%s %s - return code: %s",
                self._controller_host,
                self._id,
                command,
                self._controller_id,
                response,
            )
            self._available = False
        return True
