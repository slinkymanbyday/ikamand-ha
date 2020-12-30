"""Support for the EPH Controls Ember themostats."""
from datetime import timedelta
import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Return cached results if last scan was less then this time ago
SCAN_INTERVAL = timedelta(seconds=30)

OPERATION_LIST = [HVAC_MODE_HEAT, HVAC_MODE_OFF]


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the iKamand sensors."""
    if discovery_info is None:
        return
    try:
        ikamand = hass.data[DOMAIN]["api"]
        add_entities([IkamandThermostat(ikamand)])
    except RuntimeError:
        _LOGGER.error("Cannot connect to iKamand")
        return

    return


class IkamandThermostat(ClimateEntity):
    """Representation of a iKamand thermostat."""

    def __init__(self, ikamand):
        """Initialize the thermostat."""
        self._ikamand = ikamand

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return "iKamand"

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._ikamand.pit_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._ikamand.target_pit_temp

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""

        return 1

    @property
    def hvac_action(self):
        """Return current HVAC action."""
        return HVAC_MODE_HEAT

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        return HVAC_MODE_HEAT if self._ikamand.cooking else HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the supported operations."""
        return OPERATION_LIST

    def set_hvac_mode(self, hvac_mode):
        """Set the operation mode."""
        if hvac_mode == HVAC_MODE_HEAT:
            self._ikamand.start_cook(self.target_temperature)
        elif hvac_mode == HVAC_MODE_OFF:
            self._ikamand.stop_cook()
        else:
            _LOGGER.error("Invalid operation mode provided %s", hvac_mode)

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        if temperature == self.target_temperature:
            return

        if temperature > self.max_temp or temperature < self.min_temp:
            return

        self._ikamand.start_cook(temperature)

    @property
    def min_temp(self):
        """Return the minimum temperature."""

        return 0

    @property
    def max_temp(self):
        """Return the maximum temperature."""

        return 390

    def update(self):
        """Get the latest data."""
        self._ikamand.get_data()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._ikamand._online
