# Serial Tool (srltool) - A tool to communicate with a Micropython-based STM32 device
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
# SOFTWARE.

import sys
import os
import serial
import serial.tools.list_ports as lp
from time import sleep
from textwrap import dedent
import matplotlib.pyplot as plt


class SerialTool:
    """Class to communicate with STM32 devices over a serial connection."""
    def __init__(self):
        """Initialising the serial communication with the STM32 device."""
        try:
            if lp.comports():
                for idx, port in enumerate(lp.comports()):
                    print(f"Available port: {str(port.device)}")
                    if "ttyUSB" in str(port.device) or "ttyACM" in str(port.device):
                        serial_port = [str(port.device), 'STM32']
                if serial_port:
                    try:
                        self.serial = serial.Serial(serial_port[0], baudrate=115200)
                        print(f"Connection with the [{serial_port[1]}] established on {port.device}\n")
                    except PermissionError:
                        print("Permission denied.\nPlease run the script in sudo mode.")
                        sys.exit(1)
                    except Exception as e:
                        print(e)
                        print("Are you sure you're running the script in sudo mode?")
                        sys.exit(1)

                else:
                    print("No serial ports were found.")
                    sys.exit(1)
            else:
                print("No communication ports were found.")
                sys.exit(1)

        except Exception as e:
            print(e)

    def enter_raw_repl(self) -> None:
        """Entering the raw-REPL mode."""

        self.serial.write(b'\r\x03')
        sleep(0.1)
        self.serial.write(b'\x03')
        sleep(0.1)

        n = self.serial.inWaiting()
        while n > 0:
            self.serial.read(n)
            n = self.serial.inWaiting()

        for retry in range(3): 
            self.serial.write(b'\r\x01')
            sleep(0.01)
            data = self.serial.read_all()
            if data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
                break
            else:
                if retry >= 3:
                    print(data)
                    return
                sleep(0.2)

    def soft_reset(self) -> None:
        """Soft-reset the device."""
        self.serial.write(b'\r\x04')

    def exit_raw_repl(self) -> None:
        """Exits the raw-REPL mode."""
        self.serial.write(b'\r\x02')

    def execute(self, cmd: str) -> None:
        """Executes the command by first entering the raw-REPL mode, executing the script, soft resetting the device and finally exiting the raw-REPL mode."""
        self.enter_raw_repl()
        if len(cmd) < 256:
            self.serial.write(cmd.encode())
        else:
            for i in range(0, len(cmd), 256):
                self.serial.write(cmd[i:min(i + 256, len(cmd))].encode())
                sleep(0.01)
        self.soft_reset()
        sleep(0.125)
        self.exit_raw_repl()

    def clear(self) -> None:
        """Clears the screen on the REPL"""
        cmd = """
        import sys
        sys.stdout.write("\x1b[2J\x1b[H")
        """
        self.execute(dedent(cmd))

    def close(self) -> None:
        """Closes the serial connection."""
        self.serial.close()
    
    def ls(self, dir: str='', show: bool=True) -> str:
        """Lists the content of the specified directory.
        Examples:
        srltool ls
        or 
        srltool ls [directory]
        """

        cmd = f"""
        try:
            import pyb
            import os
        except ImportError:
            import uos as os
        usb = pyb.USB_VCP()
        resp = [item for item in os.ilistdir('{dir}')]
        usb.write(repr(resp))
        """
        self.execute(dedent(cmd))
        if self.serial.read(2) == b'OK':
            raw_resp = self.serial.read_until(b'>')
            if b'\x04\x04>' not in raw_resp:
                print("Something went wrong!\nPerhaps the parent directory doesn't exist,")
                return
            files, dirs = [], []
            for item in sorted(eval(raw_resp.decode()[:-3])):
                if hex(item[1]) == '0x4000':
                    if show:
                        print('[d]',f'{item[0]:>16}')
                    dirs.append(item[0])
                if hex(item[1]) == '0x8000':
                    if show:
                        print('[f]',f'{item[0]:>16}',f'{item[3]:>10}')
                    files.append(item[0])
        self.exit_raw_repl()
        return(files, dirs)

    def tree(self, path: str='.', show_hidden=True, dir_only=False) -> int:
        """Lists the content of the specified directory in a Tree format.
        Examples:
        srltool tree
        or 
        srltool tree [folder]
        or 
        srltool tree --show-hidden --dir-only
        """

        cmd = f"""
        try:
            import pyb
            import os
        except ImportError:
            import uos as os
        class Tree():
            def __init__(self, path='.', show_hidden=False, dir_only=False):
                self.blank  = '    '
                self.branch = '│   '
                self.elbow  = '└───'
                self.tee    = '├───'
                self.nf, self.nd = 0, 0
                self.path = path
                self.show_hidden, self.dir_only = show_hidden, dir_only
            
            def show_dir(self, level=0, is_last=False, prefix='', *args, **kwargs):
                if self.show_hidden:
                    folder = sorted(os.listdir(self.path))
                else:
                    folder = [f for f in os.listdir(self.path) if not f.startswith('.')]
                
                if self.dir_only:
                    folder = [item for item in folder if os.stat('{{}}/'.format(self.path) + item)[0] & 0x4000]
                
                last_file = folder[-1] if len(folder) > 0 else ''
                for item in folder:
                    if os.stat('{{}}/'.format(self.path) + item)[0] & 0x4000:
                        self.nd += 1
                        if level == 0:
                            print('{{}} (dir)'.format(item))
                        else:
                            if item != last_file:
                                is_last = False
                                print(self.blank, prefix + self.tee + '{{}} (dir)'.format(item))
                            else:
                                is_last = True
                                print(self.blank, prefix + self.elbow + '{{}} (dir)'.format(item))
                        os.chdir(item)
                        level += 1
                        if level > 1:
                            prefix += self.blank if item == last_file else self.branch
                        
                        self.show_dir(level=level, is_last=is_last, prefix=prefix)

                        prefix = prefix[:-4] if level > 0 else prefix
                        os.chdir('..')
                        level -= 1
                    else:
                        if self.dir_only:
                            return self.nd
                        self.nf += 1
                        if level == 0:
                            print(item)
                        else:
                            if item != last_file:
                                print(self.blank, prefix + self.tee + '{{}}'.format(item))
                            else:
                                print(self.blank, prefix + self.elbow + '{{}}'.format(item))
                
                return self.nd, self.nf

            def __repr__(self) -> str:
                nd , nf = self.show_dir()
                if nf:
                    return ('{{}} folder(s), {{}} files.').format(nd, nf)
                else: 
                    return ('{{}} folder(s).').format(nd)
            
        print(Tree(path='{path}', show_hidden={show_hidden}, dir_only={dir_only}))
        """

        self.execute(dedent(cmd))
        sleep(0.2)
        if self.serial.read(2) == b'OK':
            raw_resp = self.serial.read_until(b'>')
            if b'\x04\x04>' not in raw_resp:
                print("Something went wrong!\nPerhaps the parent directory doesn't exist!")
                return
            resp =  raw_resp.decode()[:-3]
        else:
            print('something went wrong!')
            raise RuntimeError
        print(resp if resp else '')
            
    def memstat(self) -> str:
        """Returns the memory status of the device.

        Example:
        srltool memstat
        """

        cmd = f"""
        import gc, pyb
        usb = pyb.USB_VCP()
        free_mem = gc.mem_free()
        allocated_mem = gc.mem_alloc()
        total_mem = free_mem + allocated_mem
        usb.write(repr([total_mem, allocated_mem, free_mem]))
        """
        self.execute(dedent(cmd))
        if self.serial.read(2) == b'OK':
            raw_resp = self.serial.read_until(b'>')       
            resp =  eval(raw_resp.decode()[:-3])
            print('\nTotal memory size: {:.3f} MB'.format(resp[0]/1048576))
            print('Allocated memory : {:.3f} MB'.format(resp[1]/1048576))
            print('Available memory: {:.3f} [{}%] MB\n'.format(resp[2]/1048576, round(resp[2]/resp[0] * 100,1)))
        self.exit_raw_repl()
        return repr(resp)

    def flashstat(self) -> str:
        """Returns details of the allocated and available flash space.

        Example:
        srltool flashstat
        """

        cmd = f"""
        try:
            import pyb
            import os
        except ImportError:
            import uos as os
        usb = pyb.USB_VCP()
        usb.write(repr(os.statvfs('/flash')))
        """
        self.execute(dedent(cmd))
        if self.serial.read(2) == b'OK':
            raw_resp = self.serial.read_until(b'>')
            resp = eval(raw_resp.decode()[:-3])
            _total = resp[0] * resp[3] / 1048576
            _remained = resp[0] * resp[2] / 1048576
            print('\nTotal flash size: {:.3f} MB'.format(_total))
            print('Remained free space: {:.3f} MB'.format(_remained))
        self.exit_raw_repl()
        return repr(resp)

    def overall_stat(self) -> str:
        """ Returns the overall flash size details and memory status.

        Example:
        srltool stats
        """

        self.ls()
        self.flashstat()
        self.memstat()
    
    def mkdir(self, dir: str, ignore_if_exists: bool=True) -> None:
        """ Creates the specified directory.
        The [--ignore-if-exists] option if passed then if the directory exists will be preserved without deletion. 

        Example:
        srltool mkdir [directory_to_create]
        or
        srltool mkdir [directory_to_create] --ignore-if-exists 
        """
        if dir in self.ls(show=False)[1]:
            if ignore_if_exists:
                print('Directory already exists!')
                return
            else:
                print('Directory exists, removing recursively.')
                self.rmdir(dir, recursive=True)
        cmd = f"""
        try:
            import os
        except ImportError:
            import uos as os
        os.mkdir('{dir}')
        """
        self.execute(dedent(cmd))

    def rmfile(self, file: str) -> None:
        """ Removes the specified file without further notice, please be cautious!
    
        Example:
        srltool rmfile [file_to_delete]
        """

        filename = file.split('/')[-1]
        dirname = '/'.join(file.split('/')[:-1])
        if filename not in self.ls(dirname, show=False)[0]:
            print("File doesn't exist!")
            return

        cmd = f"""
        try:
            import os
        except ImportError:
            import uos as os
        os.remove('{file}')
        """
        self.execute(dedent(cmd))
        print('file was removed.')

    def rmdir(self, dir: str, recursive: bool=False) -> None:
        """ Removes the specified directory.
            If the [--forced or -f] option is passed then if the existed folder and all its contents including
            all files and subdirectories will be deleted recursively; the default flag is True, please be cautious!

            Examples:
            srltool rmdir [dir_to_delete]
            or
            srltool rmdir [dir_to_delete] --forced
        """

        if recursive:
            cmd = f"""
            try:
                import os
            except ImportError:
                import uos as os
            def rmdir(directory):
                os.chdir(directory)
                for f in os.listdir():
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                for f in os.listdir():
                    rmdir(f)
                os.chdir('..')
                os.rmdir(directory)
            rmdir('{dir}')
            """
            self.execute(dedent(cmd))
            print('directory was removed.')
            return

        if dir not in self.ls(show=False)[1]:
            print("Directory doesn't exist!")
            return
        if not self.ls(dir, show=False)[0] and not self.ls(dir, show=False)[1]:
            cmd = f"""
            try:
                import os
            except ImportError:
                import uos as os
            os.rmdir('{dir}')
            """
            self.execute(cmd)
            print('directory was removed.')
        else:
            print('directory is not empty, please consider the --forced/-f option to remove recursively.')
 
    def sendfile(self, filename_to_send: str, filename_to_save: str=None, forced: bool=False, BUFFER_SIZE: int=64) -> None:
        """ Sends the specified file [filename_to_send] and will save as the specified file [filename_to_save].
            If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.
            buffer_size argument may also be passed to adjust the size of the buffers to be transferred over serial; the default value is 32;
            the [--forced or -f] option can be passed to over-write the exisitng file, please be cautious!

            Examples:
            srltool send-file [filename_to_send] [filename_to_save]
            or
            srltool send-file [filename_to_send] 
            or
            srltool send-file [filename_to_send] --forced buffer_size=128
        """
        if filename_to_save is None:
            filename_to_save = filename_to_send
        
        # print(f'filename_to_send: {filename_to_send}\nfilename_to_save: {filename_to_save}')

        file = filename_to_save.split('/')[-1]
        dir = '/'.join(filename_to_save.split('/')[:-1])
        if self.ls(dir, show=False) is None:
            print('Saving to root...')
            dir = '/flash'
            filename_to_save = dir + '/' + file
        if not forced:
            if file in self.ls(dir, show=False)[0]:
                print("File exists, please use the -f/--forced option to overwrite the file.")
                return
        
        # print(f'filename_to_send: {filename_to_send}\nfilename_to_save: {filename_to_save}')

        self.enter_raw_repl()
        with open(filename_to_send, 'rb') as f:
            content = f.read()
            self.serial.write(f"with open('{filename_to_save}', 'wb') as f:\r".encode())
            sleep(0.1)
            segments = [content[i:i + BUFFER_SIZE] for i in range(0, len(content), BUFFER_SIZE)]
            sys.stdout.write("\033[?25l")
            for idx, segment in enumerate(segments):
                self.serial.write(textwrap.indent(f"f.write({segment})\r", '    ').encode())
                progress = round((int(idx + 1) / int(len(segments))) * 100)
                sys.stdout.write(f"Sending [{filename_to_send}]: {progress}%\r")
                sys.stdout.flush()
                sleep(0.1)
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
        sys.stdout.write("\033[K")
        sys.stdout.write(f'Sent [{filename_to_send}]\n')
        sleep(0.5)
        self.soft_reset()
        sleep(0.5)
        self.exit_raw_repl()
        sleep(0.5) 

    def senddir(self, dirname_to_send: str, dirname_to_save: str=None, forced:bool = False) -> None:
        """ Sends the specified directory [dirname_to_send] and all its included files to the specifieddirectory [dirname_to_save].
            If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_send] will be designated to save the folder. 
            the [--forced or -f] option can be passed to over-write the exisitng folder and all its included files, please be cautious!

            Examples:
            srltool send-dir [dirname_to_send] [dirname_to_save]
            or
            srltool send-dir [dirname_to_send]
            or
            srltool send-dir [dirname_to_send] --forced
        """
        if dirname_to_save is None:
            dirname_to_save = dirname_to_send
        
        # print(f'dirname_to_send: {dirname_to_send}\ndirname_to_save: {dirname_to_save}')

        if not forced:
            current_path = os.getcwd()
            child_dir = dirname_to_send.split('/')[-1]
            parent_dir = current_path + '/' + '/'.join(dirname_to_send.split('/')[:-1])
            if child_dir not in os.listdir(parent_dir):
                print("Directory doesn't exist.")
                return

        self.mkdir(f'{dirname_to_save}')
        sleep(0.1)
        # print(f'dirname_to_send: {dirname_to_send}\ndirname_to_save: {dirname_to_save}')
        for file in os.listdir(f'{dirname_to_send}/'): 
            if forced:
                self.sendfile(f'{dirname_to_send}/{file}', f'{dirname_to_save}/{file}', forced=True)
            else:
                self.sendfile(f'{dirname_to_send}/{file}', f'{dirname_to_save}/{file}', forced=False)
            sleep(0.5)
        print('Directory was sent.')

    def recvfile(self, filename_to_get: str, filename_to_save: str=None, check_exist: bool=True, BUFFER_SIZE: int=32) -> None:
        """ Receives the specified file [filename_to_get] and will save as the specified file [filename_to_save].
            If the [filename_to_save] has not been specified as an argument, then the same name as the [filename_to_get] will be designated to save the file.
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
        """

        cmd = f"""
        try:
            import pyb
            import os
            from time import sleep
        except ImportError:
            import uos as os
        usb = pyb.USB_VCP()
        with open('{filename_to_get}', 'r') as f:
            content = f.read()
            segments = [content[i:i + {BUFFER_SIZE}] for i in range(0, len(content), {BUFFER_SIZE})]
            for segment in segments:
                usb.write(repr({{}}).format(segment))
                sleep(0.1)
        """
        file = filename_to_get.split('/')[-1]
        dir = '/'.join(filename_to_get.split('/')[:-1])
        if check_exist:
            if file not in self.ls(dir, show=False)[0]:
                print("File doesn't exist.")
                return
        print(f'Reading "{filename_to_get}"')
        self.execute(dedent(cmd))
        sleep(0.01)
        if filename_to_save is None:
            filename_to_save = filename_to_get

        file = filename_to_save.split('/')[-1]
        dir = '/'.join(filename_to_save.split('/')[:-1])
        current_dir = os.getcwd()

        if dir in os.listdir(current_dir):
            os.chdir(dir)
        else:
            os.makedirs(dir)
            os.chdir(dir)

        if self.serial.read(2) == b'OK':
            print(f'Writing "{file}"')
            with open(file, 'wb') as f:
                raw_resp = self.serial.read_until(b">")
                resp = raw_resp[:-3]
                f.write(resp)
        os.chdir(current_dir)
        self.clear()

    def recvdir(self, dirname_to_get:  str, dirname_to_save: str=None) -> None:
        """ Receives the specified directory [dirname_to_get] and its included files and will save in the specified directory [dirname_to_save].
            If the [dirname_to_save] has not been specified as an argument, then the same name as the [dirname_to_get] will be designated to save the folder. 
            
            Examples:
            srltool recv-dir dirname_to_get dirname_to_save
            or
            srltool recv-dir dirname_to_get
        """
        child_dir = dirname_to_get.split('/')[-1]
        parent_dir = '/'.join(dirname_to_get.split('/')[:-1])
        if child_dir not in self.ls(parent_dir, show=False)[1]:
            print("Directory doesn't exist")
            return

        if dirname_to_save == '':
            dirname_to_save = dirname_to_get

        files = self.ls(f'{dirname_to_get}', show=False)[0]
        if not files:
            os.makedirs(dirname_to_save)
            return

        current_dir = os.getcwd()
        os.makedirs(dirname_to_save)
        os.chdir(dirname_to_save)

        for file in files:
            self.recvfile(f'{dirname_to_get}/{file}', f'{dirname_to_save}/{file}', check_exist=False)
            sleep(0.01)
        os.chdir(current_dir)
    
    def astroid(self, n):
        """Requests a list of coordinates and will plot an astroid as a serial test to 
        assess the serial connection with the device.
        """
        def plot(_list):
            plt.axis('off')
            for _ in range(1):
                for i in range(len(_list)):
                    plt.plot(_list[i][0], _list[i][1], 'b-')
                    plt.pause(0.1)
                    plt.plot(_list[i][0], _list[i][2], 'b-')
                    plt.pause(0.1)
                for i in reversed(range(len(_list))):
                    plt.pause(0.1)
                    plt.plot(_list[i][0], _list[i][1], 'w-')
                    plt.pause(0.1)
                    plt.plot(_list[i][0], _list[i][2], 'w-')
                    plt.pause(0.1)
            plt.show()
        cmd = f"""
        import pyb
        from utime import sleep
        usb = pyb.USB_VCP()
        a = [[(i, 0), (0, abs(abs(i) - {n})), (0, -(abs(abs(i) - {n})))] for i in range(-{n}, {n} + 1)]
        segments = [a[i:i + 64] for i in range(0, len(a), 64)]
        for segment in segments:
            usb.write(repr({{}}).format(segment))
            sleep(0.02)
        """
        self.execute(dedent(cmd))
        sleep(0.5)
        if self.serial.read(2) == b'OK':
            raw_resp = self.serial.read_until(b'>')
            if b'\x04\x04>' not in raw_resp:
                print("Something went wrong!\nPerhaps the parent directory doesn't exist!")
                return
            resp =  raw_resp.decode()[:-3]
        else:
            print('something went wrong!')
            raise RuntimeError
        if resp:
            plot(eval(resp))
