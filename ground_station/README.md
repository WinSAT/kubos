Command Definitions Documentation
Command Definitions define the set of Commands that can be run on a System (a Satellite or Ground Station).

Structure
Command Definitions are uploaded as JSON files that look like the following:

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
The JSON structure always has a top level key of "definitions" that contains a map of command names (e.g., "deploy", "attitude_control", and "hardware_test" above) to command definitions. Command definitions are defined as follows.

Command Definitions
Each Command Definition must contain the display_name, description, and fields keys.

Command Definition keys:

display_name: The name of the command to display in Major Tom's UI.
description: A description of what the command does, to show in Major Tom's UI.
tags: An optional array of zero or more alphanumeric tags under which to group this command in the Major Tom UI.
fields: An array of zero or more Field Definitions, as defined below.
Field Definitions
The fields key must map to an array of zero or more Field Definitions with the following keys.

Field Definition keys:

name (required): The name of the field.
type (required): The type of the field — must be one of the following:
number (deprecated, use integer instead)
integer
float
enum
string
text
datetime
value (optional): A constant value that the field must always take.
default (optional): The default, placeholder, or starting value for a field that can be changed.
characterLimit (optional): A number indicating the character limit for a string or text field.
range (optional):
For the number type, an array of exactly two elements defining the field's valid numeric range.
For the string type, an array of one or more elements to populate a select field of valid string values for the field.
enum (required if type is enum, ignored otherwise)
An object whose keys are string descriptions of their integer values. Values do not need to be sequential.
Once the definition for an enum field is uploaded, its range of values will be displayed in a dropdown menu.
When a user selects one of those values, only the numerical value will be sent over the API.
See the example below for usage details of an enum field.
Example Usage of enum Type
In the command definition JSON
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
In the command UI
The above enum definition will translate to a dropdown list with the following values:

0 - OFF
10 - LOW
40 - MEDIUM
80 - HIGH
What will be sent in the command fields JSON
Selecting the option 40 - MEDIUM will result in the following JSON value being sent over the API:

{
  "fields": [{ "Enum Setting": 40 }]
}
datetime
Setting the datetime type will display this field as an input, along with options to use a visual date & time picker and seconds manipulator. Starting values for the pickers correspond to the time that the UI for this command was opened.
The output of the pickers, and the expected use of this type, is Unix UTC epoch time in milliseconds.
The displayed text field can receive direct input and editing if needed.
Sub-second milliseconds can only be adjusted manually in the text field, not using the picker or the seconds manipulator.
datetime will accept any positive integer, so be careful.
The keyword "now" can be used in the definition JSON under the default property. When this is set, the field will have the value of the time the UI for this command was opened. Otherwise, a default or value can be set as a Unix time value.
Example Usage of datetime Type
In the command definition JSON
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
File transfer Command Definitions
Major Tom's file transfer features use three "reserved" Command Definitions. If you want to use these file transfer features, you should include the following in your Command Definitions document. You can also add additional fields to these definitions to provide context to your file transfer system.

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
Details:

update_file_list: When your Gateway receives the update_file_list command, it should trigger whatever process is appropriate to fetch an updated file list from the remote system and then use the file_list Gateway API message to inform Major Tom about it. Please see the Gateway API documentation under any Gateway for details.
uplink_file: When your Gateway receives the uplink_file command, it should download the file referenced by the gateway_download_path field. Please see the file_download section of the Gateway API documentation under any Gateway for details.
downlink_file: When your Gateway receives the downlink_file command, it should request the provided filename from the remote system. When downlinked, the Gateway should upload the file data to Major Tom. Please see the file_upload section of the Gateway API documentation under any Gateway for details.






Gateway API Documentation
Gateways connect a system (a satellite or ground station) to Major Tom using Major Tom's WebSocket-based Gateway API.

New to Major Tom?
We recommend running our Example Python Gateway locally to get started! It's intended to give you a feel for how to interact with satellites from Major Tom and give an example of how to use the API documented below. No coding is required to use it! Just follow the README instructions in the repository.

Gateways in Major Tom
Major Tom's concept of a Gateway is simply a named channel of communication. Gateways have a token that is used to authenticate with Major Tom. Setup a Gateway on your Mission and copy the token.

Gateways are just named communication channels with authentication.
If you want to have dev and prod environments, make two Gateways.
Connecting to Major Tom
Open a WebSocket connection to Major Tom at /gateway_api/v1.0 (this probably looks like: wss://you.majortom.cloud/gateway_api/v1.0).
Include the X-Gateway-Token HTTP header or gateway_token query param, set to a token from one of your Major Tom Gateways.
Provide Basic Auth credentials for your Major Tom deployment. If your websocket client supports it, you may be able to include these in the connection string (e.g. wss://user:password@you.majortom.cloud/gateway_api/v1.0). Alternatively, your websocket client may allow you to provide the username and password as options. If not, you can do it yourself by encoding them in the HTTP Authorization header. See information on correct encoding.
You should receive a message like {'type': 'hello', 'hello': { 'mission': 'your-mission' }} on connection if your X-Gateway-Token header (or gateway_token param) and Authorization header are valid.
Response Codes
401 - If the server requires Basic Auth credentials and you haven't provided them, you will receive a 401 error.
403 - If the Gateway Token is invalid, you will receive a 403 error.
404 or 503 - If the Major Tom service is temporarily unavailable, you may receive a 404 or 503 error. You should wait a few seconds and try again.
Rate Limits
Major Tom enforces rate limits on Gateway messages using a credit system. There is a credit bucket that can hold 300 credits and refills at 2000 credits/min. All messages sent to Major Tom over the Gateway use 1 credit. In addition, measurements and events messages use an additional 0.1 credit per measurement or event included.

For message details, see rate_limit.

General implementation advice
In order to be forward compatible, ignore messages and message fields that you don't understand.
Reconnect on disconnection after a short delay.
Buffer telemetry, events, and command updates until successful reconnection.
Dual-write any critical telemetry & events to local log files for redundancy.
Interactive Testing
You can issue test messages against this Gateway here. Warning: this is a live connection to your Gateway!

File Transfer in Major Tom
There are examples of uplink and downlink flows, and suggestions of how to use the API to accomplish file transfers, in the file transfer section. The examples assume knowledge of how Commands interact with a Gateway.
Messages from Major Tom
A Gateway will receive the following message types from Major Tom:

hello
command
cancel
rate_limit
error
Messages to Major Tom
A Gateway can send the following message types to Major Tom:

command_update
measurements
events
command_definitions_update
file_list
file_metadata_update
Other API actions
Some flows occur over a RESTful API:

file_upload
file_download

Commands
A command from Major Tom represents a user's action to create and queue a Command based on a CommandDefinition.

{
  "type": "command",
  "command": {
    "id": 20,
    "type": "PowerUp",
    "system": "hamilton",
    "fields": [
      { "name": "parameter-1", "value": 1 },
      { "name": "parameter-2", "value": "foo" }
    ]
  }
}
Updating Commands
Note: Major Tom previously updated commands using a command_status message. This is (currently) still supported, but we recommend upgrading to the new command_update message, detailed here.

Setting Command state
Commands in Major Tom transition through a series of states based on messages sent by your Gateway. The current state of a command is displayed in the Major Tom UI along with the command's payload representation, current status, progress bars, final output, and any errors that you report. It is up to you and your Gateway how you use these fields and the available states, which are:

queued (reserved for Major Tom)
waiting_for_gateway (reserved for Major Tom)
sent_to_gateway (reserved for Major Tom)
preparing_on_gateway
uplinking_to_system
transmitted_to_system
acked_by_system
executing_on_system
downlinking_from_system
processing_on_gateway
cancelled
completed
failed
The job of your Gateway is to transition a Command through the most appropriate series of these states. All states are optional. You can update a command's state by sending the original Command's command.id field as id, like so:

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "acked_by_system"
  }
}
Validating the Command
When you first receive a Command, you should validate that the Command's fields are valid and correctly formatted for your system given the command's type. If there is a validation error, your Gateway should transition the Command to the failed state and provide one or more errors. For example:

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "failed",
    "errors": ["parameter-2 must be longer than 5 characters", "PowerUp is invalid in the current run level"]
  }
}
Providing a Command payload & status
If the Command is valid, you will likely want to transition to preparing_on_gateway or uplinking_to_system, whichever is appropriate for your Command lifecycle. At the same time, we recommend that you provide a payload containing the domain-specific command representation that will be sent to your remote system. E.g., a HEX code or JSON blob. This is optional, but if provided, Major Tom will show it in the UI for future debugging.

You may also choose to provide an optional status for the Command. This field will be cleared whenever the command changes state. It is shown in the UI to the operator and saved as an event. You can take advantage of status to help illuminate what is happening with the Command as it moves through its lifecycle.

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "uplinking_to_system",
    "status": "Waiting for pass",
    "payload": "mutation { powerUp { success, errors, pid } }"
  }
}
Update your Command fields as often as needed
When updating payload, errors, status, and the progress and output fields explained below, you do not have to also provide state, although you can. You can provide any combination of these fields in a command_update message, allowing you to repeatedly update the Major Tom UI when inside of a state.

Note: to ensure correct Command update ordering, Commands are updated directly by the Gateway thread in Major Tom, so you should avoid updating Commands faster than an average of a few times per second or the Gateway can back up. This is particularly important for statuses and progress bars (outlined below) where you should be sure to avoid sending repeated updates for some common event, such as on every byte received or fractional percent complete.

Completing or failing your Command
When your Command completes, you should move it into the completed state and provide an optional output field for the operator.

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "completed",
    "output": "Power enabled"
  }
}
On the other hand, if the Command fails on the remote system (or anywhere in its lifecycle), you should move it into the failed state and provide errors and possibly a status:

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "failed",
    "status": "Command failed on satellite",
    "errors": ["Error code 123"]
  }
}
Note that output and errors can only be set in the completed and failed states, as they're intended to represent the final results of a Command.

Progress bars
Finally, in any of the ing progress states (e.g., preparing_on_gateway, uplinking_to_system, executing_on_system, downlinking_from_system, and processing_on_gateway), Major Tom can display progress bars to provide visual feedback to the operator. A progress bar will be displayed in a progress state when you provide progress_1_current, progress_1_max, and (optionally) progress_1_label. Example usage would be to show progress of an analysis step on your Gateway or of queue state on a remote system.

Additionally, you may display a second progress bar by providing progress_2_current, progress_2_max, and (optionally) progress_2_label. This may be helpful if you want to display progress of a substep or dependent value. For example, when uplinking, you could display transmitted chunks with progress 1 and ACKed chunks with progress 2.

{
  "type": "command_update",
  "command": {
    "id": 20,
    "state": "preparing_on_gateway",
    "status": "Compressing",
    "progress_1_current": 5,
    "progress_1_max": 100,
    "progress_1_label": "percent compressed"
  }
}
Summary
In summary, the following fields can be set on commands:

Field	Type	Available in States	Cleared on State Transition	Suggested Usage
state	string enum	all	n/a	Indicate phase of command lifecycle
payload	string	all	No	Record command payload representation for future debugging
status	string	all	Yes	Display what is currently happening with the command
output	string	completed or failed	Yes	Final command output
errors	array of strings	completed or failed	Yes	Final command errors
progress_1_current	integer	Progress states (those containing ing)	Yes	Current value of a process to display as a progress bar
progress_1_max	integer	Progress states (those containing ing)	Yes	Max value of a process to display as a progress bar
progress_1_label	string	Progress states (those containing ing)	Yes	Label for the progress bar (e.g., "bytes uplinked")
progress_2_current	integer	Progress states (those containing ing)	Yes	Current value of a secondary process to display as a second progress bar
progress_2_max	integer	Progress states (those containing ing)	Yes	Max value of a secondary process to display as a second progress bar
progress_2_label	string	Progress states (those containing ing)	Yes	Label for the second progress bar (e.g., "chunks ACKed")

Command Cancellation
If a user requests command cancellation, Major Tom will send the Gateway a cancel message of the following form:

{
  "type": "cancel",
  "timestamp": 1528391020767,
  "command": {
    "id": 20
  }
}
It is the responsibility of the Gateway to transition the command into the cancelled state.


Rate Limit
There is a maximum allowed Gateway messaging rate. If you exceed this rate, Major Tom will ignore your message and send a message of type: "rate_limit" with a "rate_limit" field containing information.

{
    "type": "rate_limit",
    "rate_limit": {
        "rate": 120,
        "retry_after": 0.5,
        "error": "Rate limit exceeded. Please limit request rate to a burst of 20 and an average of 120/minute.",
    }
}
rate is the average number of requests per minute that will be accepted, and retry_after is the number of seconds until the next message will be accepted.


Errors
If Major Tom needs to send your gateway an error, you'll receive a message of type: "error" with an error field indicating the cause. You should generally log this error.

Some errors (those with "disconnect": "true") will also result in Major Tom disconnecting your Gateway.

{
  "type": "error",
  "error": "This Gateway's token has been rotated. Please use the new one.",
  "disconnect": true
}
Sending data to Major Tom

Sending Measurements to Major Tom
To send measurements to Major Tom, send messages of the form:

{
  "type": "measurements",
  "measurements": [
    {
      "system": "hamilton",
      "subsystem": "eps",
      "metric": "voltage",
      "value": 10,
      "timestamp": 1528391020767
    },
    { ... }
  ]
}
The system field must be the name of a system (Satellite or Ground Station) on this Mission.
The subsystem field must be the name of a Subsystem on the given System. It will be created automatically if it doesn’t yet exist.
The metric field must be the name of a Metric on the given Subsystem. It will be created automatically if it doesn't yet exist.
The value field currently only supports ints and floats.
The timestamp field is UTC in milliseconds. It is optional, and if left unset, it will default to the time Major Tom processes the measurements. We recommend including this field.
Please note: it is significantly more performant to send Major Tom batches of telemetry in a single "type": "measurements" message instead of via many separate messages. You may send up to 10,000 measurements per measurements messages.


Sending events to Major Tom
To send events to Major Tom, send messages of the form:

{
  "type": "events",
  "events": [
    {
      "system": "hamilton",
      "type": "SatelliteAlert",
      "message": "Reactor is critical",
      "level": "error",
      "command_id": 123,
      "debug": { "some_key": "some_value" },
      "timestamp": 1528391020767
    },
    { ... }
  ]
}
system - (optional) the name of a system (Satellite or Ground Station) on this Mission
type - (optional) a custom type for this Event, defaults to Event. You will likely use this type to select a subset of events in the UI and in future scripts. We recommend CamelCase or equivalent.
message - the text of the Event
level - (optional) one of debug, nominal (the default), warning, error, or critical
command_id (optional) - the ID of a Command associated with this Event
debug (optional) - arbitrary JSON key-value metadata
timestamp (optional) - when this Event was generated in milliseconds UTC. Excluding it defaults to the time Major Tom receives the message.
Some important notes:
Single events commands can contain up to 100 events.
While you can and should send multiple events at once, for performance and UI usability, we recommend limiting your logging to important events only.
Events that are submitted at the debug level are dropped after 2 weeks.

Updating the Command Definitions for a System
Given the name of a System (Satellite or GroundStation), you can update its Command Definitions via a message sent over the Gateway websocket API:

{
  "type": "command_definitions_update",
  "command_definitions": {
    "system": "hamilton",
    "definitions": {
      "set_power": {
        "display_name": "Set Power",
        "description": "Set system power on the Example Rust Service",
        "fields": [
          {"name": "power", "type": "number", "range": [0, 1]}
        ]
      },
      "calibrate_thermometer": {
        "display_name": "Calibrate Thermometer",
        "description": "Calibrate the thermometer on the Example Rust Service",
        "fields": []
      }
    }
  }
}
As with a Command Definition upload in the Major Tom UI, the uploaded Command Definitions will completely replace the existing ones for the given System.


Updating the File List for a System
Major Tom can display a list of remote files for downlink under each top-level System. The list for each system is updated en masse over the Gateway API.

To replace the full file list of a System with a full new file list, send a message of the form:

{
  "type": "file_list",
  "file_list": {
    "system": "hamilton",
    "timestamp": 1528391020767,
    "files": [
      {
        "name": "earth.tiff",
        "size": 1231040,
        "timestamp": 1528391000000,
        "metadata": { "type": "image", "lat": 40.730610, "lng": -73.935242 }
      },
      ...
    ]
  }
}
The system (required) -- must be the name of a system (Satellite or Ground Station) on this Mission.
The timestamp (optional) -- a UNIX epoch in milliseconds UTC. It is intended to represent the time that the file list was generated on the System.
The files (required) -- must be an array of objects, each with the following fields:
name (required) -- this can be the file path on disk or some other unique identifier for the file. This is what will be passed to your Gateway when a downlink is requested.
size (required) -- this is the size of the file in bytes.
timestamp (required) -- a UNIX epoch in milliseconds UTC that can represent the mtime or ctime of the file, or some other relevant timestamp. It will be displayed in the Major Tom UI.
metadata (optional) -- any key/value pairs provided will be shown for informational purposes in the Major Tom UI.
If you provide a Command Definition called update_file_list, for convenience Major Tom will provide a button in the File List UI that you can press to trigger that command.


Updating the metadata of a DownlinkedFile
Given the id of a DownlinkedFile (see the previous section), you can update the JSON string key-value pairs associated with that file whenever you like using a message sent over the Gateway websocket API:

{
  "type": "file_metadata_update",
  "downlinked_file": {
    "id": "29",
    "metadata": { "location": "32.7767 N, 96.7970 W", "analyzed": "true" }
  }
}
Note that the new metadata will be merged with the existing metadata. If you wish to delete a field, you must send a null value for it.


File Transfer in Major Tom
Major Tom serves as an interface for interacting with the file transfer system that works with your remote system and does not directly manage the protocol required for your remote system. Through Major Tom, you can send commands to trigger the start of a file transfer, see progress updates for the status of that transfer, interact with files that have been downlinked, and stage files to be uplinked. The handling of the space - ground connection and the file transfer itself must be done by the Gateway, and the Gateway is responsible for telling Major Tom about the progress, downloading files from Major Tom that need to be uplinked, and uploading files to Major Tom that have been downlinked.

Note on terminology: "Uplink" and "Downlink" refers to the space - ground portion of the file transfer, while "Upload" and "Download" refer to interaction with Major Tom.

Example Flows
Uplink a file to the satellite/system:
User uploads a file under the "Uplink" tab under the desired system. This stages the file so it's accessible by the Gateway.
User sends a command to start the file uplink with a field that contains the reference to the staged file for the Gateway. See command definition documentation under the settings tab for your system for how to streamline this process.
The Gateway receives the command, updates the command state to "preparing_on_gateway", and downloads the staged file from Major Tom.
The Gateway begins uplinking the file to the system, setting command state to "uplinking_to_system" and issuing command_update messages as needed to represent progress.
The Gateway either confirms the file was transferred successfully by setting the command state to "complete" or lists any errors that occurred by setting the command state to "failed" and submitting the errors.
Downlink a file from the satellite/system:
(Optional) The Gateway uploads a file_list which represents the files on the system that are available for downlinking.
The user issues a command to the Gateway to start the transfer process with the filename/indicator required to reference the appropriate file. See command definition documentation under the settings tab for your system for how to streamline this process.
The Gateway receives the command, updates the command state to "transmitted_to_system", and sends the appropriate command to the system to trigger the file downlink process.
Once the downlink has started, the Gateway updates the command state to "downlinking_from_system", and issues command update messages as appropriate to represent progress.
Once the downlink has finished, the Gateway updates the command state to "processing_on_gateway" and uploads the file to Major Tom.
(Optional) The Gateway can update the file metadata as appropriate, now or in the future.
The Gateway sets the command state to "completed".
The user can view or download the file from the Downlinked tab on the Files page, accessible via the icon on the sidebar.

Uploading DownlinkedFiles to Major Tom
In the Major Tom UI, under the appropriate System, you can view the contents of the latest File List in the Downlink tab. Here, you can copy a filename for any file, or Major Tom can pre-fill that filename into a Command Definition called downlink_file, if you have provided one. Given this filename, your Gateway should downlink the associated file from the remote system.

Once a file has been downlinked from your remote system to your Gateway, you can upload it to Major Tom for display in the UI and for eventual download to users' computers.

The upload flow is different from the other Gateway API actions because it does not use the Gateway Websocket API. Instead, upload is performed via a series of RESTful API requests.

We will now walk through the process. We recommend following along using this bash script that demonstrates the flow via curl.

Step 1: Request permission to upload a file
Make a JSON POST request to /rails/active_storage/direct_uploads including your Gateway token in the X-Gateway-Token header and the following required parameters:

filename - the name the file should have on disk when downloaded to a user's computer (not the full path)
byte_size - The size of the file in bytes (cat file | wc -c)
content_type - The MIME type that the file should have when downloaded. For images that may be previewed in Major Tom, please provide the correct MIME type, such as image/jpeg or image/png. For other file types, binary/octet-stream should be fine.
checksum - A base64 encoded MD5 of the file's contents. Please see this snippet for some examples of computing this.
An example with curl:

curl "https://you.majortom.cloud/rails/active_storage/direct_uploads" \
  -H "X-Gateway-Token: YOUR_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary '{"filename":"file.txt","byte_size":123,"content_type":"binary/octet-stream","checksum":"CHECKSUM"}'
The response will look something like this:

{
  ...
  "signed_id": "...eyJfcmiOnsibWVzc2Fn--91b3da29d1eb12f4e...",
  "direct_upload": {
    "url": "http://THE-LONG-UPLOAD-URL",
    "headers": {
      "Content-Type": "binary/octet-stream",
      "Content-MD5": "CHECKSUM"
    }
  }
}
You will need these fields in the next two steps.

Step 2: Upload the file with a PUT request
Make an HTTP PUT request to the URL provided in the direct_upload.url field in the response from the previous step. Include the exact request headers provided in the direct_upload.headers fields from the previous step. The file can be up to 2GB in size.

With curl, this looks like:

curl \
  -H 'Content-Type: binary/octet-stream' \
  -H "Content-MD5: CHECKSUM" \
  --upload-file "file.txt" \
  "http://THE-LONG-UPLOAD-URL"
Step 3: Tell Major Tom about the file's details
When the upload has completed successfully, tell Major Tom about the System, remote timestamp, name, and optional metadata of the file. Make a JSON POST request to /gateway_api/v1.0/downlinked_files including your Gateway token in the X-Gateway-Token header and the following parameters:

signed_id - The long unique ID that was returned in Step 1.
name - The full name of the file on the remote system (can be a filename or a full path).
timestamp - The timestamp used to sort DownlinkedFiles in Major Tom's UI. (We suggest using the time that you received the downlinked file.)
system - The name of the System in Major Tom.
command_id - (optional) The Major Tom Command ID that triggered this file downlink.
metadata - (optional) Arbitrary JSON string key-value pairs to display with the DownlinkedFile in the Major Tom UI.
An example with curl:

curl "https://you.majortom.cloud/gateway_api/v1.0/downlinked_files" \
  -H "X-Gateway-Token: YOUR_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary '{"signed_id":"THE-SIGNED-ID-FROM-STEP-1",
                  "name":"file.txt",
                  "timestamp":1552004346241,
                  "system":"my-satellite",
                  "command_id":"123",
                  "metadata":{"location":"32.7767 N, 96.7970 W"}
                 }'
If this requests succeeds, your file has been uploaded and recorded in Major Tom.

An example response:

{
  "id": 29,
  "name": "file.txt",
  ...
}
Note the returned id, as you may want to use it to issue file metadata updates later.

Again, we recommend reviewing this bash script for an example of this complete upload flow using curl.


Downloading StagedFiles from Major Tom
In order to uplink files from Major Tom to your remote system, a user will upload files from their web browser to Major Tom. These files can be up to 2GB in size. Once uploaded, these "StagedFiles" are visible under the System to which they have been associated. To uplink these files to your remote system, you need to download them from Major Tom to your Gateway, then uplink via your satellite/system's file transfer protocol. In the Major Tom UI you can copy a gateway_download_path for any StagedFile. Major Tom will also pre-fill this path into a Command Definition called uplink_file, if you provide one.

The gateway_download_path will look something like /rails/active_storage/blobs/eyJfcmF.../file.dat?disposition=attachment. Prepend your Major Tom hostname (including Basic Auth credentials, if needed) to form a complete URL and fetch the file by issuing an HTTP GET request to the combined URL, including your Gateway Token in an X-Gateway-Token header. Note: you must follow HTTP redirects for this to work.

An example with curl (using -L to follow redirects):

curl -L \
     -H "X-Gateway-Token: YOUR_GATEWAY_TOKEN" \
     "https://you.majortom.cloud/rails/active_storage/blobs/eyJfc..."