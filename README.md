# Srltool
> Serial Tool (srltool) - A tool to communicate with a Micropython-based STM32 device<br />
>
> "srltool" is a simplified command-line tool to communicate with Micropython-based STM32 devices over serial connection. Send/receive directories and files, make/remove directories and files, details about the memory usage and available space on flash are examples of the features currently included in the tool. "srltool" was a personal project for personal use; please be cautious specifically while using features such rmdir/rmfile.<br />
> 
> Usage: cli.py [OPTIONS] COMMAND [ARGS]...
>
> Options:
>  -h, --help  Show this message and exit.
> <pre>
> Commands:<br />
> - ls                  Lists the content of the specified directory.
> - mkdir               Creates the specified directory.
> - recv-dir            Receives the specified directory.
> - recv-file           Receives the specified file.
> - rmdir               Removes the specified directory.
> - rmfile              Removes the specified file.
> - send-dir            Sends the specified directory.
> - send-file           Sends the specified file.
> - stat_flash          Returns the details of allocated and available flash space.
> - stat_mem            Returns the memory status of the device.
> - stats               Returns the overall flash size details and memory status.
> - tree                Lists the content of the specified directory in Tree format.

## Installation 
`sudo pip install -r requirements.txt`<br />
`sudo python setup.py develop`<br />

## Usage
Note: You might have to use the srltool under superuser privileges(sudo).<br /> 
Note: srltool will find the accessible port to the available stm32 device and communicates over serial with a predefined baudrate of 115200<br />
### [ls]
Lists the content of the specified directory.

Examples:<br />
`srltool ls`<br />
or<br />
`srltool ls [directory]`<br />
`srltool ls --help`<br />

---
### [tree]
Lists the content of the specified directory in a Tree format.<br />

Examples:<br />
`srltool tree`<br />
or <br />
`srltool tree [folder]`<br />
or <br />
`srltool tree --show-hidden --dir-only`<br />
`srltool tree --help`<br />

---
### [stat_mem]
Returns the memory status of the device.<br />

Example:<br />
`srltool stat_mem`<br />
`srltool stat_mem --help`<br />

---
### [stat_flash]
Returns details of the allocated and available flash space.<br />

Example:<br />
`srltool stat_flash`<br />
`srltool stat_flash --help`<br />

---
### [stats]
Returns the overall flash size details and memory status.<br />

Example:<br />
`srltool stats`<br />
`srltool stats --help`<br />

---
### [mkdir]
Creates the specified directory.<br />
The [--ignore-if-exists] option if passed then if the directory exists will be preserved ignoring the deletion.<br />

Example:<br />
`srltool mkdir [directory_to_create]`<br />
or<br />
`srltool mkdir [directory_to_create] --ignore-if-exists`<br /> 
`srltool mkdir --help`<br />

---
### [rmfile]
Removes the specified file without further notice, please be cautious!<br />

Example:<br />
`srltool rmfile [file_to_delete]`<br />
`srltool rmfile --help`<br />

---
### [rmdir]
Removes the specified directory.<br />
If the [--forced or -f] option is passed then if the existed folder and all its contents including
all files and subdirectories will be deleted recursively.<br /> 
The default flag is True, please be cautious!<br />

Examples:<br />
`srltool rmdir [dir_to_delete]`<br />
or<br />
`srltool rmdir [dir_to_delete] --forced`<br />
`srltool rmdir --help`<br />

---
### [sendfile]
Sends the specified file [filename_to_send] and will save as the specified file [filename_to_save].
If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.<br />
[buffer_size] argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32 bytes.<br />
The [--forced or -f] option can be passed to over-write the existing file, please be cautious!<br />

Examples:<br />
`srltool send-file [filename_to_send] [filename_to_save]`<br />
or<br />
`srltool send-file [filename_to_send]` <br />
or<br />
`srltool send-file [filename_to_send] --forced buffer_size=128`<br />
`srltool send-file --help`<br />

---
### [senddir] 
Sends the specified directory [dirname_to_send] and all its included files to the specifieddirectory [dirname_to_save].<br />
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_send] will be designated to save the folder. <br />The [--forced or -f] option can be passed to overwrite the existing folder and all its included files, please be cautious!

Examples:<br />
`srltool send-dir [dirname_to_send] [dirname_to_save]`<br />
or<br /><br />
`srltool send-dir [dirname_to_send]`<br />
or<br />
`srltool send-dir [dirname_to_send] --forced`<br />
`srltool send-dir --help`<br />

---
### [recvfile]
Receives the specified file [filename_to_get] and will save as the specified file [filename_to_save].<br />
If the [filename_to_save] has not been specified as an argument,  then the same name as the [filename_to_get] will be designated to save the file.<br />
[check_exist] argument may be passed to check if the file exists; the default value is True.<br />
[buffer_size] argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32.<br />

Examples:<br />
`srltool recv-file [filename_to_get] [filename_to_save]`<br />
or<br />
`srltool recv-file [filename_to_get]` <br />
or<br />
`srltool recv-file [filename_to_get] check_exist=True buffer_size=64`<br />
or<br />
`srltool recv-file [filename_to_get] [filename_to_save]`<br />
`srltool recv-file --help`<br />

---
### [recvdir]
Receives the specified directory [dirname_to_get] and its included files and will save in the specified directory [dirname_to_save].<br />
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_get] will be designated to save the folder. <br />
    
Examples:<br />
`srltool recv-dir dirname_to_get dirname_to_save`<br />
or<br />
`srltool recv-dir dirname_to_get`<br />
`srltool recv-dir --help`<br />

---
### [astroid] 
Requests a list of coordinates and will plot an astroid as a serial test.<br/>
This module was written to assess the serial connection. It requests a list of coordinates to be generated by the STM32 device and returned to be plotted.<br />

Examples:<br />
`srltool astroid [iterations]`<br />
or <br />
`srltool astroid 10`<br />
`srltool astroid --help`<br />

## License
[MIT License](https://opensource.org/licenses/MIT)

---
## To-do
* ESP32 compatibility

