# SerialTool – STM32 Serial Communication Utility
> SerialTool (srltool) - A tool to communicate with a Micropython-based STM32 device<br />
>
> "srltool" is a lightweight command-line tool to communicate with Micropython-based STM32 devices over serial (USB) connection.  It automatically detects connected STM32 devices, establishes a serial connection, and provides convenient methods to interact with the device using MicroPython's raw REPL interface. <br /><br />
Current features include sending and receiving files/directories, creating and removing files or directories, and viewing memory usage and available flash space.<br /><br />
> ⚠️ **Warning:** This tool was developed for personal use.  Exercise caution, especially with destructive commands like `rmdir` or `rmfile`.

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
> - flashstat           Returns the details of allocated and available flash space.
> - memstat             Returns the memory status of the device.
> - stats               Returns the overall flash size details and memory status.
> - tree                Lists the content of the specified directory in Tree format.

## Installation 
`sudo pip install -r requirements.txt`<br />
`sudo python setup.py develop`<br />

## Usage
Note: You might have to use the srltool under superuser/admin privileges(sudo).<br /> 
Note: srltool will find the accessible port to the available stm32 device and communicates over serial with a predefined baudrate of 115200.<br />

### $${\color{blue}[ls]}$$
Lists the content of the specified directory.

Examples:<br />
`srltool ls`<br />
or<br />
`srltool ls [directory]`<br />
`srltool ls --help`<br />

---
### $${\color{blue}[tree]}$$
Lists the content of the specified directory in a Tree format.<br />

Examples:<br />
`srltool tree`<br />
or <br />
`srltool tree [folder]`<br />
or <br />
`srltool tree --show-hidden --dir-only`<br />
`srltool tree --help`<br />

---
### $${\color{blue}[memstat]}$$
Returns the memory status of the device.<br />

Example:<br />
`srltool memstat`<br />
`srltool memstat --help`<br />

---
### $${\color{blue}[flashstat]}$$
Returns details of the allocated and available flash space.<br />

Example:<br />
`srltool flashstat`<br />
`srltool flashstat --help`<br />

---
### $${\color{blue}[stats]}$$
Returns the overall flash size details and memory status.<br />

Example:<br />
`srltool stats`<br />
`srltool stats --help`<br />

---
### $${\color{blue}[mkdir]}$$
Creates the specified directory.<br />
The [--ignore-if-exists] option if passed then if the directory exists will be preserved ignoring the deletion.<br />

Example:<br />
`srltool mkdir [directory_to_create]`<br />
or<br />
`srltool mkdir [directory_to_create] --ignore-if-exists`<br /> 
`srltool mkdir --help`<br />

---
### $${\color{blue}[rmfile]}$$
Removes the specified file without further notice, please be cautious!<br />

Example:<br />
`srltool rmfile [file_to_delete]`<br />
`srltool rmfile --help`<br />

---
### $${\color{blue}[rmdir]}$$
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
### $${\color{blue}[sendfile]}$$
Sends the specified file [filename_to_send] and will save as the specified file [filename_to_save].
If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.<br />
[buffer_size] argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32 bytes.<br />
The [--forced or -f] option can be passed to overwrite the existing file, please be cautious!<br />

Examples:<br />
`srltool send-file [filename_to_send] [filename_to_save]`<br />
or<br />
`srltool send-file [filename_to_send]` <br />
or<br />
`srltool send-file [filename_to_send] --forced buffer_size=128`<br />
`srltool send-file --help`<br />

---
### $${\color{blue}[senddir]}$$
### [senddir] 
Sends the specified directory [dirname_to_send] and all its included files to the specified directory [dirname_to_save].<br />
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_send] will be designated to save the folder. <br />The [--forced or -f] option can be passed to overwrite the existing folder and all its included files, please be cautious!

Examples:<br />
`srltool send-dir [dirname_to_send] [dirname_to_save]`<br />
or<br /><br />
`srltool send-dir [dirname_to_send]`<br />
or<br />
`srltool send-dir [dirname_to_send] --forced`<br />
`srltool send-dir --help`<br />

---
### $${\color{blue}[recvfile]}$$
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
### $${\color{blue}[recvdir]}$$
Receives the specified directory [dirname_to_get] and its included files and will save in the specified directory [dirname_to_save].<br />
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_get] will be designated to save the folder. <br />
    
Examples:<br />
`srltool recv-dir dirname_to_get dirname_to_save`<br />
or<br />
`srltool recv-dir dirname_to_get`<br />
`srltool recv-dir --help`<br />

---
### $${\color{blue}[astroid]}$$
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

