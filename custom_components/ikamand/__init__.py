"""Advantage Air climate integration."""

from datetime import timedelta
import logging

from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.event import track_time_interval
from ikamand.ikamand import Ikamand
import voluptuous as vol

from .const import DOMAIN

IKAMAND_SYNC_INTERVAL = timedelta(seconds=15)
PLATFORMS = ["sensor", "climate"]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_IP_ADDRESS): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Set up iKamand config."""
    conf = config[DOMAIN]
    ip_address = conf[CONF_IP_ADDRESS]
    ikamand = Ikamand(
        ip_address,
    )
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["api"] = ikamand
    hass.data[DOMAIN]["instance"] = ip_address
    # setting initial to zero to help with graphing
    hass.data[DOMAIN]["pt"] = 0
    hass.data[DOMAIN]["t1"] = 0
    hass.data[DOMAIN]["t2"] = 0
    hass.data[DOMAIN]["t3"] = 0
    hass.data[DOMAIN]["online"] = False
    hass.data[DOMAIN]["fan"] = 0

    def ikamand_update(event_time):
        """Update data from nextcloud api."""
        try:
            ikamand.get_data()
            hass.data[DOMAIN]["pt"] = ikamand.pit_temp
            hass.data[DOMAIN]["t1"] = ikamand.probe_1
            hass.data[DOMAIN]["t2"] = ikamand.probe_2
            hass.data[DOMAIN]["t3"] = ikamand.probe_3
            hass.data[DOMAIN]["online"] = ikamand.online
            hass.data[DOMAIN]["fan"] = ikamand.fan_speed
        except Exception:
            _LOGGER.error("iKamand update failed")
            return False

    track_time_interval(hass, ikamand_update, IKAMAND_SYNC_INTERVAL)

    for component in PLATFORMS:
        discovery.load_platform(hass, component, DOMAIN, {}, config)

    return True
