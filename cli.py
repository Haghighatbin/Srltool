# Serial tool (srltool) - A tool to communicate with a Micropython-based STM32 device
# Author: Amin Haghighatbin
# Copyright 2022 - MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

import click
from src import SerialTool

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None:
    """
    Serial Tool(srltool): A tool to communicate with a Micropython(STM32) device\n
    "srltool" is an extremely simplified command-line tool to communicate with Micropython-based STM32 devices over serial connection. 
    send/receive directories and files, make/remove directories and files, details about the memory usage and 
    availabe space on flash are examples of the features included in the tool.\n 
    Note: "srltool" was a personal project for personal use; please be cautious specifically while using features such rmdir/rmfile.
    """
    global _command
    _command = SerialTool()

@cli.command()
@click.argument('dir', type=click.STRING, default='')
def ls(dir) -> None:
    """Lists the content of the specified directory.
    \b

    Examples:

    srltool ls 

    srltool ls [directory]
    \f
    """
    _command.ls(dir)

@cli.command()
@click.argument('path', type=click.STRING, default='.')
@click.option('--dir-only', is_flag=True, help='Shows only directories.')
@click.option('--show-hidden', is_flag=True, help='Shows hidden files as well.')
def tree(path, show_hidden, dir_only) -> None: 
    """Lists the content of the specified directory in Tree format.

    The [--show-hideden] option if passed will also show the hidden files, the default flag is False.
    The [--dir-only] option if passed ignore the files and only shows the directories, the default flag is False.
    \b

    Examples:

    srltool tree 

    srltool tree [path-to-dir]
    
    srltool tree --dir-only --show-hidden
    \f
    """
    _command.tree(path, show_hidden, dir_only)

@cli.command('stat_mem')
def mem_stat() -> str:
    """Returns the memory status of the device.
    \b

    Example:

    srltool stat_mem
    \f
    """
    _command.mem_stat()

@cli.command('stat_flash')
def flash_stat() -> str:
    """Returns the details of allocated and available flash space.
    \b

    Example:

    srltool stat_flash
    \f
    """
    _command.flash_stat()

@cli.command('stats')
def overall_stat() -> str:
    """Returns the overall flash size details and memory status.

    It essentially calls the mem_stat and flash_stat consecutively. 
    \b

    Example:

    srltool stats
    \f
    """
    _command.overall_stat()

@cli.command()
@click.option('--ignore-if-exists', is_flag=True, help='Ignores the deletion if directory exists')
@click.argument('dir', type=click.STRING)
def mkdir(dir, ignore_if_exists) -> None:
    """Creates the specified directory.

    The [--ignore-if-exists] option if passed then if the directory exists will be preserved without deletion.
    \b
    
    Example:

    srltool mkdir [directory_to_create]

    srltool mkdir [directory_to_create] --ignore-if-exists 
    \f
    """
    if ignore_if_exists:
        _command.mkdir(dir, True)
    else:
        _command.mkdir(dir, False)

@cli.command()
@click.argument('file', type=click.STRING)
def rmfile(file: str) -> None:
    """Removes the specified file.

    Removes the specified file without further notice, Please be cautious!
    \b

    Example:
    srltool rmfile [file_to_delete]
    \f
    """
    _command.rmfile(file)

@cli.command()
@click.argument('dir', type=click.STRING)
@click.option('--forced','-f', is_flag=True, help='Removes the directory recursively; use with caution!')
def rmdir(dir: str, forced) -> None:
    """Removes the specified directory.

    If the [--forced or -f] option is passed then if the existed folder and all its contents including all files and subdirectories will be 
    deleted recursively; the default flag is True, please be cautious!
    \b

    Examples:
    srltool rmdir [dir_to_delete]

    srltool rmdir [dir_to_delete] --forced
    \f
    """
    if forced:
        _command.rmdir(dir, True)
    else:
        _command.rmdir(dir, False)

@cli.command('send-file')
@click.argument('filename_to_send', type=click.STRING)
@click.argument('filename_to_save', type=click.STRING, default='')
@click.argument('buffer_size', type=click.INT, default=64)
@click.option('--forced','-f', is_flag=True, help='Replaces the exisiting file; use with caution!')
def sendfile(filename_to_send: str, filename_to_save: str, forced: bool, buffer_size: int) -> None:
    """Sends the specified file.
    
    Sends the specified [filename_to_send] and will save as the specified [filename_to_save];
    If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.
    buffer_size argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32;
    the [--forced or -f] option can be passed to over-write the exisitng file, please be cautious!
    \b

    Examples:

    srltool send-file [filename_to_send] [filename_to_save]

    srltool send-file [filename_to_send] 

    srltool send-file [filename_to_send] --forced buffer_size=128
    \f
    """
    if filename_to_save == '':
       filename_to_save = filename_to_send
    if forced:
        _command.sendfile(filename_to_send, filename_to_save, True, buffer_size)
    else:
        _command.sendfile(filename_to_send, filename_to_save, False, buffer_size)


@cli.command('send-dir')
@click.argument('dirname_to_send', type=click.STRING)
@click.argument('dirname_to_save', type=click.STRING, default='')
@click.option('--forced','-f', is_flag=True, help='Replaces the existing directory; use with caution!')
def senddir(dirname_to_send: str, dirname_to_save: str, forced: bool) -> None:
    """Sends the specified directory
    
    Sends the specified [dirname_to_send] and all its included files to the specified [dirname_to_save];
    If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_send] will be designated to save the folder. 
    the [--forced or -f] option can be passed to over-write the exisitng folder and all its included files, please be cautious!
    \b

    Examples:

    srltool send-dir [dirname_to_send] [dirname_to_save]

    srltool send-dir [dirname_to_send]

    srltool send-dir [dirname_to_send] --forced\f
    """
    if dirname_to_save == '':
        dirname_to_save = dirname_to_send
    if forced:
        _command.senddir(dirname_to_send, dirname_to_save, True)
    else:
        _command.senddir(dirname_to_send, dirname_to_save, False)

@cli.command('recv-file')
@click.argument('filename_to_get', type=click.STRING)
@click.argument('filename_to_save', type=click.STRING, default='')
@click.argument('check_exist', type=click.BOOL, default=True)
@click.argument('buffer_size', type=click.INT, default=32)
def recvfile(filename_to_get: str, filename_to_save: str, check_exist: bool, buffer_size: int) -> None:
    """Receives the specified file.
    
    Receives the specified [filename_to_get] and will save as the specified [filename_to_save];
    If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.
    check_exist argument may be passed to check if the file exists; the default value is True;
    buffer_size argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32.
    \b

    Examples:

    srltool recv-file [filename_to_get] [filename_to_save]

    srltool recv-file [filename_to_get] 

    srltool recv-file [filename_to_get] check_exist=True buffer_size=64

    srltool recv-file [filename_to_get] [filename_to_save]\f
    """
    if filename_to_save == '':
        filename_to_save = filename_to_get
    _command.recvfile(filename_to_get, filename_to_save, check_exist, buffer_size)

@cli.command('recv-dir')
@click.argument('dirname_to_get', type=click.STRING)
@click.argument('dirname_to_save', type=click.STRING, default='')
def recvdir(dirname_to_get, dirname_to_save: str) -> None:
    """Receives the specified directory.
    
    Receives the specified directory [dirname_to_get] and its included files and will save in the specified [dirname_to_save];
    If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_get] will be designated to save the folder. 
    \b
    
    Examples:

    srltool recv-dir [dirname_to_get] [dirname_to_save]
    
    or
    
    srltool recv-dir dirname_to_get\f
    """
    if dirname_to_save == '':
        direname_to_save = dirname_to_get
    _command.recvdir(dirname_to_get, dirname_to_save)

@cli.command('astroid')
@click.argument('iterations', type=click.INT, default=10)
def astroid(iterations) -> int:
    """Requests a list of coordinates and will plot an astroid as a serial test.
    
    This module was written to assess the serial connection; it will request a list of coordinates to be generated by the STM32 device;
    The list will be returned and plotted.
    \b

    Examples:

    srltool astroid [iterations]

    or 

    srltool astroid 10\f
    """
    _command.astroid(iterations)

def main():
    cli()

