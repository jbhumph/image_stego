# Stega Pal
An experiment in image steganogrophy

## About
This program allows the user to hide a message inside of an image and then later allows the user to reveal the hidden message. The message may optionally be encrypted using AES. This can be useful across a variety of applications. I hope to grow this project to include additional methods of embedding and encryption.


## Contents
- [About](#about)
- [Author](#author)
- [Info](#info)
- [Usage Instructions](#usage-instructions)
- [Attribution](#attribution)
- [Usage Examples](#usage-examples)
- [Version Info](#version-info)



## Author
Created by: John Humphrey<br>
GitHub: https://github.com/jbhumph/image_stego<br>
<br>
This project was created during my 2025 college summer break in order to further explore areas of personal interest including steganography, encryption, pixel and bit manipulation, as well as general application development.

## Info
Steganography is the practice of concealing messages or information within other non-secret data, deriving its name from the Greek words for "covered writing." While cryptography scrambles data to make it unreadable, steganography hides the very existence of the communication itself, a technique with roots stretching back to ancient Greece where messages were hidden on wooden tablets beneath wax or tattooed on messengers' scalps. Throughout history, steganography has evolved from invisible inks and microdots to sophisticated digital methods used in modern computing and security applications. Image steganography specifically involves embedding hidden data within digital image files by subtly modifying pixel values in ways imperceptible to the human eye.

This program explores some basic aspects of image steganography. It allows the user to embed a text or message within an image file. Due to the nature of some image formats, only a select few will work with this program. 

Stega-Pal at this point explores some rudimentary methods for embedding text into an image. The basic concept works as such: The program takes a message and converts it from a string of its text to a string of the binary bits that make up its ASCII characters. Each character, number, whitespace, etc is made up of one byte or 8 bits represented by a 1 or 0. Inside an image file such as a .PNG, the image file itself is represented by an array of pixels, each of which contains data for red, green, and blue. These primary colors are each represented as 8 bits, which provide 256 different shades of that primary color. Within each byte, the bit furthest to the right is referred to as the "least significant bit" as it has the least effect on the entire color, affecting its value by one. At it's basic settings, the program will start at the beginning of the binary string and put that value in the red channel of pixel 1, replacing it's least significant bit. We then move to the next bit in the string and the blue channel of pixel 1, and on and on.

For example, we may have the following string representing "abc":
```
{ 01100001 01100010 01100011 }
```
with our first couple pixels represented as:

```
{ 10010111 01111011 11110110 10010111 01111011 11110110}

or 

PIXEL 1
RED: 		10010111
GREEN:		01111011
BLUE:		11110110

PIXEL 2
RED: 		10010111
GREEN:		01111011
BLUE:		11110110

```
Then, after moving through our chain, our first two pixels would look like this:

```
{ 10010110 01111011 11110111 10010110 01111010 11110110}

or 

PIXEL 1
RED: 		10010110
GREEN:		01111011
BLUE:		11110111

PIXEL 2
RED: 		10010110
GREEN:		01111010
BLUE:		11110110
```
As you can see, the difference is rather minimal and generally one that the human eye cannot detect. Sometimes a bit is changed and sometimes it is not. The program will later go on to allow to change the 2 least insignificant bits or only specific color channels. This results in a file of the exact size as the original.

Original Image:
![alt text](docs/a.png)

Image containing Shakespeare's Macbeth in it's entirety:
![alt text](docs/b.png)

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
                                                                        

