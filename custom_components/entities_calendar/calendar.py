"""Support for calendars based on entities."""
from datetime import datetime, timedelta
import logging

import voluptuous as vol

from homeassistant.components.calendar import PLATFORM_SCHEMA, CalendarEventDevice
from homeassistant.const import CONF_ID, CONF_NAME, CONF_TOKEN
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.template import DATE_STR_FORMAT
from homeassistant.util import Throttle, dt

_LOGGER = logging.getLogger(__name__)

CONF_CALENDARS = "calendars"
CONF_CALENDAR_ENTITIES = "entities"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CALENDARS): vol.All(
            cv.ensure_list,
            vol.Schema(
                [
                    vol.Schema(
                        {
                            vol.Required(CONF_NAME): cv.string,
                            vol.Required(CONF_CALENDAR_ENTITIES): vol.All(
                                cv.ensure_list, [vol.All(cv.string, vol.Lower)]
                            )
                        }
                    )
                ]
            ),
        ),
    }
)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=15)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the entities platform."""
    calendars = config[CONF_CALENDARS]
    calendar_devices = []
    
    for calendar in calendars:
        # Special filter: By date
        entities = calendar.get(CONF_CALENDAR_ENTITIES)

        # Create the calendar and add it to the devices array.
        calendar_devices.append(
            EntitiesCalendarDevice(
                hass,
                calendar,
                entities,
            )
        )

    add_entities(calendar_devices)


def _parse_date(date) -> datetime:
    """Parse the due date dict into a datetime object."""
    # Add time information to date only strings.
    if len(date) == 10:
        date += "T00:00:00"
    # If there is no timezone provided, use UTC.
    if not date.endswith("Z") and not "+" in date[11:] and not "-" in date[11:]:
        date += "Z"
    return dt.parse_datetime(date)


class EntitiesCalendarDevice(CalendarEventDevice):
    """A device for getting calendar events from entities."""

    def __init__(
        self,
        hass,
        calendar,
        entities,
    ):
        """Create the Todoist Calendar Event Device."""
        self.data = EntitiesCalendarData(
            hass,
            calendar,
            entities,
        )
        self._cal_data = {}
        self._name = calendar[CONF_NAME]

    @property
    def event(self):
        """Return the next upcoming event."""
        return self.data.event

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    def update(self):
        """Update all Calendars."""
        self.data.update()


    async def async_get_events(self, hass, start_date, end_date):
        """Get all events in a specific time frame."""
        return await self.data.async_get_events(hass, start_date, end_date)

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        if self.data.event is None:
            # No tasks, we don't REALLY need to show anything.
            return None

        return {}


class EntitiesCalendarData:
    """
    Class used by the Entities Calendar Device service object to hold all entity events.

    This is analogous to the GoogleCalendarData found in the Google Calendar
    component.

    The 'update' method polls for any updates to the entities. This is throttled to every
    MIN_TIME_BETWEEN_UPDATES minutes.
    """

    def __init__(
        self,
        hass,
        calendar,
        entities,
    ):
        """Initialize an Entities Calendar Project."""
        self.event = None

        self._hass = hass
        self._name = calendar[CONF_NAME]
        self._calendar = calendar
        self._entities = entities

        self.all_events = []


    async def async_get_events(self, hass, start_date, end_date):
        """Get all tasks in a specific time frame."""
        events = []
        for entity in self._entities:
            state_object = hass.states.get(entity)
            if state_object.attributes.get("device_class") == "timestamp":
                start = _parse_date(state_object.state)
            else:
                start = state_object.attributes.get("last_changed")

            if start_date < start < end_date:
                event = {
                    "uid": entity,
                    "summary": state_object.attributes.get("friendly_name"),
                    "start": {
                    	"date": start.strftime('%Y-%m-%d'),
                    },
                    "end": {
                    	"date": start.strftime('%Y-%m-%d'),
                    },
                    "allDay": True,
                }
                events.append(event)
        return events

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data."""
        events = []
        for entity in self._entities:
            state_object = self._hass.states.get(entity)
            if state_object.attributes.get("device_class") == "timestamp":
                start = _parse_date(state_object.state)
            else:
                start = state_object.attributes.get("last_changed")
            event = {
                "uid": entity,
                "summary": state_object.attributes.get("friendly_name"),
                "start": {
                    	"date": start.strftime('%Y-%m-%d'),
                },
                "end": {
                    "date": start.strftime('%Y-%m-%d'),
                },
                "allDay": True,
            }
            events.append(event)

        events.sort(key=lambda x: x["start"]["date"])

        self.event = events[0]
        _LOGGER.debug("Updated %s", self._name)