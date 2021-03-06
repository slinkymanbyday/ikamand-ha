"""Sensor data from iKamand."""
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, PROBES


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the iKamand sensors."""
    if discovery_info is None:
        return
    sensors = []
    for name in PROBES:
        sensors.append(iKamandProbeSensor(name))
    sensors.append(iKamandFanSensor("Fan"))
    add_entities(sensors, True)


class iKamandProbeSensor(Entity):
    """Represents a iKamand sensor."""

    def __init__(self, item):
        """Initialize the iKamand sensor."""
        self._name = item
        self._state = None

    @property
    def icon(self):
        """Return the icon for this sensor."""
        return "mdi:thermometer"

    @property
    def name(self):
        """Return the name for this sensor."""
        return f"iKamand {self._name}"

    @property
    def state(self):
        """Return the state for this sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return the unique ID for this sensor."""
        return f"{self.hass.data[DOMAIN]['instance']}#{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement the value is expressed in."""
        return TEMP_CELSIUS

    def update(self):
        """Update the sensor."""
        self._state = self.hass.data[DOMAIN][PROBES[self._name]]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.hass.data[DOMAIN]["online"]


class iKamandFanSensor(Entity):
    """Represents a iKamand sensor."""

    def __init__(self, item):
        """Initialize the iKamand sensor."""
        self._name = item
        self._state = None

    @property
    def icon(self):
        """Return the icon for this sensor."""
        return "mdi:fan"

    @property
    def name(self):
        """Return the name for this sensor."""
        return f"iKamand {self._name}"

    @property
    def state(self):
        """Return the state for this sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return the unique ID for this sensor."""
        return f"{self.hass.data[DOMAIN]['instance']}#{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement the value is expressed in."""
        return PERCENTAGE

    def update(self):
        """Update the sensor."""
        self._state = self.hass.data[DOMAIN]["fan"]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.hass.data[DOMAIN]["online"]
