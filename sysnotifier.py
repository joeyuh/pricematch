import subprocess
import platform
import urllib.request
import pathlib
import ssl
import webbrowser
import os

windows_import = True

try:
    from win10toast import ToastNotifier
except ImportError:
    if platform.system().lower() == 'windows':
        windows_import = False


class SysNotifier:
    def __init__(self):
        sysname = platform.system()
        self.disabled = os.path.exists('disable_notification.txt')
        if self.disabled:
            print(
                "System Notification is set to globally disabled, you can enable by deleting disable_notification.txt")
            return
        self.notifier_path = 'terminal-notifier'  # Default to system wide installation
        if sysname.lower() == 'windows':
            self.os_type = 0
        elif sysname.lower() == 'darwin':
            self.os_type = 1
        elif sysname.lower() == 'linux':
            self.os_type = 2
        else:
            self.disabled = True
            print("Unsupported OS for notification")
            return

        self.test()

    def test(self):
        print('Initializing notification test:')
        test_path = pathlib.Path(__file__).parent.absolute() / 'terminal-notifier.app' \
                    / 'Contents' / 'MacOS' / 'terminal-notifier'
        if os.path.exists(test_path):
            self.notifier_path = test_path
        return_code = 0xFFFF
        if self.os_type == 0:
            try:
                toaster = ToastNotifier()
                toaster.show_toast(title='Test', msg='Test Test',
                                   callback_on_click=lambda: webbrowser.open('http://google.com'))
                return_code = 0
            except Exception as e:
                print('win10toast threw an error. Did you install the original version? A modified one is required')
                print(e)

        elif self.os_type == 1:
            return_code = os.system(
                f"""{self.notifier_path} -title 'Test' -subtitle 'Test' -message 'Test' -open 'https://google.com'""")
        elif self.os_type == 2:
            print('Linux support yet to be added')
            self.disable()
            return

        # os.system('command') returns a 16 bit number, which first 8 bits from left(lsb) talks about signal used by
        # os to close the command, Next 8 bits talks about return code of command.

        exit_code = (return_code >> 8) & 0xFF  # First 4 bits of the integer
        # command_return = return_code & 0xFF         # Next 4 bits of the integer
        if exit_code == 0:
            print('Test OK')
        else:
            print('System notification software not found!')
            self.install()

    def install(self):
        if self.os_type == 1:
            ssl._create_default_https_context = ssl._create_unverified_context
            print('Supported notification method for macOS: terminal-notifier')
            print('If you choose not to install, notification will be disabled')
            if input('Would you like to install it automatically? Enter yes to install: '):
                url = 'https://github.com/julienXX/terminal-notifier/releases/download/2.0.0/terminal-notifier-2' \
                      '.0.0.zip '
                path = pathlib.Path(__file__).parent.absolute() / 'temp.zip'
                urllib.request.urlretrieve(url, path)
                os.system(f'unzip -o -q {path}')
                os.remove(path)
                os.remove('README.markdown')
                print('Retesting')
                self.test()
            else:
                self.disable()
        elif self.os_type == 0 and not windows_import:
            print('Supported notification method for Windows: a modified version of win10toast')
            print('Install with:\n')
            print(
                'pip install git+https://github.com/MaliciousFiles/Windows-10-Toast-Notifications.git#egg=win10toast\n')
            print('If you choose not to install, notification will be disabled')
            if input('Enter yes and the program will terminate, then install and restart the program: ') == 'yes':
                exit(0)
            else:
                self.disable()

    def disable(self):
        self.disabled = True
        print('Notification will be disabled')
        with open('disable_notification.txt', 'w') as f:
            f.write('Anything')
        print('Delete disable_notification.txt to re-enable notification')

    @staticmethod
    def notify(os_type, title, subtitle, message, url, notifier_path=None):
        if os_type == 1:
            os.system(
                f"""{notifier_path} -title '{title}' -subtitle '{subtitle}' -message '{message}' -open '{url}'""")
        elif os_type == 0:
            toaster = ToastNotifier()
            toaster.show_toast(title=title, msg=subtitle + " " + message,
                               callback_on_click=lambda: webbrowser.open(url))
