# Entities Calendar
A custom component for Home Assistant to allow regular entities to be used as a calendar

This initial release only really supports sensors with a device_class of "timestamp".
These will create all-day calendar events using the state of the sensor as the date.

Other entity types can be used, but these will create all-day events based on the **last_changed** attribute.
Support for other types of sensors (and for events which are not all-day) may be added in future releases.


### Installation

###
```yaml
calendar:
  - platform: entities_calendar
    calendars:
      name: Bin Collection
      entities:
        - sensor.bin_collection_grey
        - sensor.bin_collection_green
        - sensor.bin_collection_garden
```
