# Stega Pal
An experiment in image steganogrophy

## About


## Contents


## Info


## Usage Instructions

<br>

### General

``` json
"general": {
	"verbose_mode": true,
	"show_original_preview": false,
	"show_encoded_preview": false,
	"show_decode_preview": false,
	"!!!auto_backup": false,
	"!!!preserve_metadata": false,
	"show_summary": true
}
```
#### Verbose Mode
- **Default:** true
- **Options:** true / false
- **Description:** This mode prints to the terminal a confirmation of each critical step in the encoding / decoding process. Can be useful for troubleshooting.
#### Show Original Preview
- **Default:** false
- **Options:** true / false
- **Description:** Enabling this preview will display the original unedited image to be encoded using your systems default image viewer.

> **NOTE:** This is not technically opening the actual file. the Pillow library loads it as a temporary object in memory and your system opens that file.
#### Show Encoded Preview
- **Default:** false
- **Options:** true / false
- **Description:** Enabling this preview will display the new edited and encoded image using your systems default image viewer.

> **NOTE:** This is not technically opening the actual file. the Pillow library loads it as a temporary object in memory and your system opens that file.

#### Show Decode Preview
- **Default:** false
- **Options:** true / false
- **Description:** Enabling this preview will display the image to be decoded using your systems default image viewer.

> **NOTE:** This is not technically opening the actual file. the Pillow library loads it as a temporary object in memory and your system opens that file.
#### Auto Backup 
***Not Started***
#### Preserve Metadata
***Not Started***
#### Show Summary
***In Progress***
### Embedding
``` json
"embedding": {
	"delimiter_type": "null_terminator",
	"magic_sequence": "1111111100000000",
	"channels_to_use": [
		"R",
		"G",
		"B"
	],
	"bits_per_channel": 1,
	"embedding_pattern": "sequential",
	"skip_pixels": 0,
	"capacity_warning_threshold": 80
}
```

#### Delimiter Type
- **Default:** null_terminator
- **Options:**
	- null_terminator
	- magic_sequence
	- none
	- length_prefix
- **Description:** The delimiter choice represents how the end of the message is communicated. `null_terminator` adds an 8-bit null sign at the end of the  message to be encoded. `magic_sequence` adds a 128-bit binary sequence (see below) to the end of the message to be encoded. `none` will not add any additional prefix or delimiter. `length_prefix` adds a 32-bit binary sequence to the beginning of the message to be encoded. Currently this has a maximum value of 9,999. *If the key is not any of the options the program currently defaults to using length prefix* 
#### Magic Sequence
- **Default:** 1111111100000000
- **Options:** This is merely a string rather than a binary sequence so it can be whatever you like.
- **Description:** If magic_sequence is selected as the delimiter type, this setting sets the actual sequence that is embedded after the primary message. The primary constraint is length, with each character representing an additional 8-bits. Once the decoder encounters this sequence it will know that the message is complete.

> **NOTE:** The user will want to ensure that there is no possible way that the magic sequence could possibly occur anywhere in their primary text, otherwise the decoding process will terminate early, resulting in an incomplete decoding.


#### Channels to Use
***Not Started***
#### Bits Per Channel
***Not Started***
#### Embedding Pattern
***Not Started***
#### Skip Pixels
***Not Started***
#### Capacity Warning Threshold
***Not Started***

### Security
#### Encryption Enabled
***Not Started***
#### Encryption Algorithm
***Not Started***
#### Password Hash Algorithm
***Not Started***
### File Handling
#### Supported Input Formats
***Not Started***
#### Default Output Format
***Not Started***
#### Compression Level
***Not Started***
#### Max Message Length
***Not Started***
#### Min Image Size
***Not Started***
#### Output Filename Template
***Not Started***
### Validation
#### Strict Mode
***Not Started***
#### Allow Overwrite
***Not Started***
#### Verify Embedding
***Not Started***
### Logging
#### Save Logs
***Not Started***
#### Log File
***Not Started***
#### Log Level
***Not Started***


```json
{

"general": {

"verbose_mode": true,

"show_original_preview": false,

"show_encoded_preview": false,

"!!!auto_backup": false,

"!!!preserve_metadata": false,

"show_summary": true

},

"embedding": {

"delimiter_type": "length",

"magic_sequence": "1111111100000000",

"channels_to_use": [

"R",

"G",

"B"

],

"bits_per_channel": 1,

"embedding_pattern": "sequential",

"skip_pixels": 0,

"capacity_warning_threshold": 80

},

"!!!security": {

"encryption_enabled": false,

"encryption_algorithm": "AES",

"password_hash_algorithm": "SHA256"

},

"!!!file_handling": {

"supported_input_formats": [

".png",

".bmp",

".tiff",

".jpg",

".jpeg"

],

"default_output_format": ".png",

"compression_level": 6,

"max_message_length": 10000,

"min_image_size": [

100,

100

],

"output_filename_template": "{original_name}_encoded{extension}"

},

"!!!validation": {

"strict_mode": true,

"allow_overwrite": false,

"verify_embedding": true

},

"!!!logging": {

"save_logs": false,

"log_file": "steganography.log",

"log_level": "INFO"

}

}
```




## Attribution


## Usage Examples


## Version Info
                                                                        

