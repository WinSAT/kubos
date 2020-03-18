# Command Definitions Documentation
Command Definitions define the set of Commands that can be run on a System (a Satellite or Ground Station).

Note: This information was retrieved from Major Tom Documentation provided by Kubos.

## Structure

Command Definitions are uploaded as JSON files that look like the following:

```JSON
{
  "definitions": {
    "command": {
      "display_name": "Command Name To Display",
      "description": "Description to give context to the operator.",
      "tags": ["operations"],
      "fields": [
        {"name": "Field Name 1", "type": "number", "range": [1, 10]},
        {"name": "Field Name 2", "type": "number", "value": 15},
        {"name": "Field Name 3", "type": "string"},
        {"name": "Field Name 4", "type": "text"},
        {"name": "Field Name 5", "type": "enum", "enum": {
          "LOW": 1, "MEDIUM": 5, "HIGH": 11
        }}
      ]
    },
    "deploy": {
      "display_name": "Deploy",
      "description": "Deploy the Solar Panels on the satellite.",
      "tags": ["commissioning", "one-time"],
      "fields": [
        {"name": "timeout", "type": "number", "value": 10}
      ]
    },
    "attitude_control": {
      "display_name": "Attitude Control",
      "description": "Sets the target quaternion for the ADCS",
      "tags": ["operations", "adacs"],
      "fields": [
        {"name": "X", "type": "number"},
        {"name": "Y", "type": "number"},
        {"name": "Z", "type": "number"},
        {"name": "W", "type": "number"}
      ]
    },
    "hardware_test": {
      "display_name": "Hardware Test",
      "description": "Runs the test command for all subsystems.",
      "tags": ["commissioning", "recovery"],
      "fields": []
    }
  }
}
```

The JSON structure always has a top level key of "definitions" that contains a map of command names (e.g., "deploy", "attitude_control", and "hardware_test" above) to command definitions. Command definitions are defined as follows.

## Command Definitions

Each Command Definition must contain the display_name, description, and fields keys.

Command Definition keys:

* display_name: The name of the command to display in Major Tom's UI.
* description: A description of what the command does, to show in Major Tom's UI.
* tags: An optional array of zero or more alphanumeric tags under which to group this command in the Major Tom UI.
* fields: An array of zero or more Field Definitions, as defined below.

### Field Definitions

The fields key must map to an array of zero or more Field Definitions with the following keys.

Field Definition keys:

* name (required): The name of the field.
* type (required): The type of the field — must be one of the following:
* * number (deprecated, use integer instead)
* * integer
* * float
* * enum
* * string
* * text
* * datetime
* value (optional): A constant value that the field must always take.
* default (optional): The default, placeholder, or starting value for a field that can be changed.
* characterLimit (optional): A number indicating the character limit for a string or text field.
* range (optional):
* * For the number type, an array of exactly two elements defining the field's valid numeric range.
* * For the string type, an array of one or more elements to populate a select field of valid string values for the field.
* enum (required if type is enum, ignored otherwise)
* * An object whose keys are string descriptions of their integer values. Values do not need to be sequential.
* * Once the definition for an enum field is uploaded, its range of values will be displayed in a dropdown menu.
* * When a user selects one of those values, only the numerical value will be sent over the API.
* * See the example below for usage details of an enum field.

### Example Usage of enum Type

`In the command definition JSON`

```JSON
{
  "definitions": {
    "example_enum": {
      "display_name": "Example Enum Command",
      "description": "Example command for enum usage",
      "fields": [
        {
          "name": "Enum Setting",
          "type": "enum",
          "enum": {
            "OFF": 0,
            "LOW": 10,
            "MEDIUM": 40,
            "HIGH": 80
          }
        }
      ]
    }
  }
}
```

`In the command UI`

The above enum definition will translate to a dropdown list with the following values:

0 - OFF
10 - LOW
40 - MEDIUM
80 - HIGH

`What will be sent in the command fields JSON`

Selecting the option 40 - MEDIUM will result in the following JSON value being sent over the API:

```JSON
{
  "fields": [{ "Enum Setting": 40 }]
}
```

* datetime
* * Setting the datetime type will display this field as an input, along with options to use a visual date & time picker and seconds manipulator. Starting values for the pickers correspond to the time that the UI for this command was opened.
* * The output of the pickers, and the expected use of this type, is Unix UTC epoch time in milliseconds.
* * The displayed text field can receive direct input and editing if needed.
* * Sub-second milliseconds can only be adjusted manually in the text field, not using the picker or the seconds manipulator.
datetime will accept any positive integer, so be careful.
* * The keyword "now" can be used in the definition JSON under the default property. When this is set, the field will have the value of the time the UI for this command was opened. Otherwise, a default or value can be set as a Unix time value.

### Example Usage of datetime Type

`In the command definition JSON`

```JSON
{
  "definitions": {
    "example_datetime": {
      "display_name": "Example DateTime Command",
      "description": "Example command for datetime usage",
      "fields": [
        {
          "name": "time",
          "type": "datetime",
          "default": "now" // Optional
        }
      ]
    }
  }
}
```

## File transfer Command Definitions

Major Tom's file transfer features use three "reserved" Command Definitions. If you want to use these file transfer features, you should include the following in your Command Definitions document. You can also add additional fields to these definitions to provide context to your file transfer system.

```JSON
{
  "definitions": {
    "update_file_list": {
      "display_name": "Update File List",
      "description": "Request an updated file list from the System",
      "fields": []
    },
    "uplink_file": {
      "display_name": "Uplink File",
      "description": "Uplink a file to the System",
      "fields": [
        {"name": "gateway_download_path", "type": "string"}
      ]
    },
    "downlink_file": {
      "display_name": "Downlink File",
      "description": "Downlink a file from the System",
      "fields": [
        {"name": "filename", "type": "string"}
      ]
    }
  }
}
```

Details:

* update_file_list: When your Gateway receives the update_file_list command, it should trigger whatever process is appropriate to fetch an updated file list from the remote system and then use the file_list Gateway API message to inform Major Tom about it. Please see the Gateway API documentation under any Gateway for details.
* uplink_file: When your Gateway receives the uplink_file command, it should download the file referenced by the gateway_download_path field. Please see the file_download section of the Gateway API documentation under any Gateway for details.
* downlink_file: When your Gateway receives the downlink_file command, it should request the provided filename from the remote system. When downlinked, the Gateway should upload the file data to Major Tom. Please see the file_upload section of the Gateway API documentation under any Gateway for details.
