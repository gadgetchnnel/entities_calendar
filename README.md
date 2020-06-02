# Entities Calendar
A custom component for Home Assistant to allow regular entities to be used as a calendar

## Installation

### Via HACS

Simply search for Entities Calendar in HACS

### Basic Configuration

```yaml
calendar:
  - platform: entities_calendar
    calendars:
      - name: Bin Collection
        entities:
          - entity: sensor.bin_collection_general
            name: General Waste Collection
          - entity: sensor.bin_collection_recycling
            name: Recycling Collection
          - entity: sensor.bin_collection_garden
            name: Garden Waste Collection
      - name: Other Entities
        entities:
          - entity: sensor.other_entity1
          - entity: sensor.other_entity2
          - entity: sensor.other_entity3
```

### Event start and end time

By default the start and end time of the event will be determined based on the device_class attribute of the entity:

#### Device class "timestamp"

These will create all-day calendar events using the state of the sensor as the date.

#### Other device classes

These will create all-day events based on the **last_changed** attribute.

This can be overridden by using the **start_time** and/or **end_time** options.

### Entity Configuration Options

| Option | Description |
|--------|-------------|
| **entity (Required)** | The entity id of the entity |
| **name (Optional)** | The name to use for the event (defaults to the friendly name of the entity) |
| **start_time (Optional)** | A **time** object as defined below specifying how the start time is determined (defeaults to being determined based on device class) |
| **end_time (Optional)** | A **time** object as defined below specifying how the end time is determined (defeaults to being determined based on device class) |

#### **time** object

| Option | Description |
|--------|-------------|
| timestamp_in_state (Optional) | Setting this to **true** forces the state to be used for the start/end time event if the device class is not "timestamp" |
| timestamp_attribute (Optional) | Setting this to the name of an attribute will use that for the time (even for "timestamp") entities |

#### Example

Given three sensors:

- sensor.attribute_test - a sensor with a start_time and end_time attribute
- sensor.state_test - a sensor with a timestamp in the state but without a device_class of "timestamp"
- sensor.default_test - a sensor with a device_class of "timestamp"

The following configuration would be used:

```yaml
calendar:
  - platform: entities_calendar
    calendars:
      - name: Entities
        entities:
          - entity: sensor.attribute_test
            name: Attribue Test
            start_time:
              timestamp_attribute: start_time
            end_time:
              timestamp_attribute: end_time
          - entity: sensor.state_test
            name: State Test
            start_time:
              timestamp_in_state: true
            end_time:
              timestamp_in_state: true
          - entity: sensor.default_test
            name: Default Test
```
