from tkinter import *
import _thread
from subprocess import Popen, PIPE
import time
import os

class Serve(Button):
    def __init__(self,master=None,text=None):
        Button.__init__(self,master,text=text)
        self['command'] = self._onButtonClick

    def _onButtonClick(self):
        try:
            os.system("gnome-terminal -e 'bash -c \"sudo php artisan serve --port=80 --host=localhost --env=testing;bash\"'")
        except:
            try:
                os.system('start cmd.exe @cmd /k ""')
            except:
                print("Can\'t launch terminal to start PHP artisan serve. Check if gnome-terminal (Linux) or start (windows) cmds are working.")

class RunNormalTests(Button):
    def __init__(self,master=None,text=None):
        Button.__init__(self,master,text=text)
        self['command'] = self._onButtonClick

    def _onButtonClick(self):
        os.system('python vendor/pveltrop/pyrunner/test_app.py debug')
        
class RunTestsDev(Button):
    def __init__(self,master=None,text=None):
        Button.__init__(self,master,text=text)
        self['command'] = self._onButtonClick

    def _onButtonClick(self):
        os.system('python vendor/pveltrop/pyrunner/test_app.py dev debug')
        
class Update(Button):
    def __init__(self,master=None,text=None):
        Button.__init__(self,master,text=text)
        self['command'] = self._onButtonClick

    def _onButtonClick(self):
        os.system('python vendor/pveltrop/pyrunner/update.py')


class App(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)

        self.button1 = Serve(self,text="Serve project")
        self.button1.grid()
        
        self.button2 = RunNormalTests(self,text="Run all tests")
        self.button2.grid()
        
        self.button3 = RunTestsDev(self,text="Development mode")
        self.button3.grid()
        
        self.button4 = Update(self,text="Update PyRunner")
        self.button4.grid()
        
    def start(self):
        _thread.start_new_thread(self.slow_function, ())

def main():
    root = Tk()
    app = App(master=root)
    app.grid()
    root.title("PyRunner")
    root.mainloop()

if __name__ == '__main__':
    main()