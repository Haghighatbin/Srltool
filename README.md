

## Srltool
Author: Amin Haghighatbin - 2022\n 
Serial Tool (srltool) - A tool to communicate with a Micropython-based STM32 device\n 

Srltool is a simplified command-line tool to communicate with Micropython-based STM32 devices over serial connection. Send/Receive directories and files, Make/Remove directories and files, details about the memory usage and availabe space on flash are examples of the features already been included in the tool. Srltool was a personal project for personal use; please be cautious specifically while using features such rmdir/rmfile.

Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  ls          Lists the content of the specified directory.\n
  mkdir       Creates the specified directory.\n
  recv-dir    Receives the specified directory.\n
  recv-file   Receives the specified file.\n
  rmdir       Removes the specified directory.\n
  rmfile      Removes the specified file.\n
  send-dir    Sends the specified directory\n
  send-file   Sends the specified file.\n
  stat_flash  Returns the details of allocated and available flash space.\n
  stat_mem    Returns the memory status of the device.\n
  stats       Returns the overall flash size details and memory status.\n
  tree        Lists the content of the specified directory in Tree format.\n

## Installation 

[sudo pip install -r requirements.txt] -> not neccessary if installed with the next line\n
sudo python setup.py develop

## Usage

# ls
Lists the content of the specified directory.

Examples:\n
srltool ls\n
or\n
srltool ls [directory]\n
srltool ls --help\n

# tree
Lists the content of the specified directory in a Tree format.
Examples:
srltool tree
or 
srltool tree [folder]
or 
srltool tree --show-hidden --dir-only
srltool tree --help
 
# stat_mem
Returns the memory status of the device.

Example:
srltool stat_mem
srltool stat_mem --help

# stat_flash
Returns details of the allocated and available flash space.

Example:
srltool stat_flash
srltool stat_flash --help

# stats
Returns the overall flash size details and memory stauts.

Example:
srltool stats
srltool stats --help

# mkdir
Creates the specified directory.
The [--ignore-if-exists] option if passed then if the directory exists will be preserved without deletion. 

Example:
srltool mkdir [directory_to_create]
or
srltool mkdir [directory_to_create] --ignore-if-exists 
srltool mkdir --help

# rmfile
Removes the specified file without further notice, please be cautious!

Example:
srltool rmfile [file_to_delete]
srltool rmfile --help

# rmdir
Removes the specified directory.
If the [--forced or -f] option is passed then if the existed folder and all its contents including
all files and subdirectories will be deleted recursively; the default flag is True, please be cautious!

Examples:
srltool rmdir [dir_to_delete]
or
srltool rmdir [dir_to_delete] --forced
srltool rmdir --help

# sendfile
Sends the specified file [filename_to_send] and will save as the specified file [filename_to_save].
If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the # file.
buffer_size argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32;
the [--forced or -f] option can be passed to over-write the exisitng file, please be cautious!

Examples:
srltool send-file [filename_to_send] [filename_to_save]
or
srltool send-file [filename_to_send] 
or
srltool send-file [filename_to_send] --forced buffer_size=128
srltool send-file --help

# senddir 
Sends the specified directory [dirname_to_send] and all its included files to the specifieddirectory [dirname_to_save].
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_send] will be designated to save the folder. The [--forced or -f] option can be passed to over-write the exisitng folder and all its included files, please be cautious!

Examples:
srltool send-dir [dirname_to_send] [dirname_to_save]
or
srltool send-dir [dirname_to_send]
or
srltool send-dir [dirname_to_send] --forced
srltool send-dir --help

# recvfile
Receives the specified file [filename_to_get] and will save as the specified file [filename_to_save].
If the [filename_to_save] has not been specified as an argument,  then the same name as the [filename_to_get] will be designated to save the file.
check_exist argument may be passed to check if the file exists; the default value is True;
buffer_size argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32.

Examples:
srltool recv-file [filename_to_get] [filename_to_save]
or
srltool recv-file [filename_to_get] 
or
srltool recv-file [filename_to_get] check_exist=True buffer_size=64
or
srltool recv-file [filename_to_get] [filename_to_save]
srltool recv-file --help

# recvdir
Receives the specified directory [dirname_to_get] and its included files and will save in the specified directory [dirname_to_save].
If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_get] will be designated to save the folder. 
    
Examples:
srltool recv-dir dirname_to_get dirname_to_save
or
srltool recv-dir dirname_to_get
srltool recv-dir --help

# astroid 
Requests a list of coordinates and will plot an astroid as a serial test.
This module was written to assess the serial connection; it will request a list of coordinates to be generated by the STM32 device;
The list will be returned and plotted.

Examples:
srltool astroid [iterations]
or 
srltool astroid 10
srltool astroid --help

## To-do
ESP32 compatibility

