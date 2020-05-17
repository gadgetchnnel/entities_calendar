# Entities Calendar
A custom component for Home Assistant to allow regular entities to be used as a calendar

This initial release only really supports sensors with a device_class of "timestamp".
These will create all-day calendar events using the state of the sensor as the date.

Other entity types can be used, but these will create all-day events based on the **last_changed** attribute.
Support for other types of sensors (and for events which are not all-day) may be added in future releases.


### Installation

## Via HACS

Add this repository as a custom repository to HACS (type Integration)

### Configuration
```yaml
calendar:
  - platform: entities_calendar
    calendars:
      - name: My Entities
        entities:
          - sensor.my_entity1
          - sensor.my_entity2
          - sensor.my_entity3
      - name: Other Entities
        entities:
          - sensor.other_entity1
          - sensor.other_entity2
          - sensor.other_entity3
```
