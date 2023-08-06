import os
import re
import sys
from io import StringIO
from shutil import copyfile
from . import constants
from littlenv import littlenv
from subprocess import run, PIPE
import pexpect
from getpass import getpass


def write_config(
        username: str, password: str, config_file: str,
        config_name: str, write_to: str = constants.PROFILE_FILE
):
    config_file = os.path.abspath(config_file)
    validate_file_exists(config_file)

    try:
        copyfile(write_to, write_to + '.backup')
    except FileNotFoundError:
        pass

    if os.path.exists(write_to):
        with open(write_to, 'r') as file:
            data = file.read()

            # clean previous values
            for value in constants.PROPERTIES:
                pattern = constants.VPN_ENV_PATTERN.format(name=config_name, property=value)
                data = re.sub(rf"^{pattern}\s*=.*", '', data, flags=re.MULTILINE)
    else:
        data = ''

    new_config = "\n".join(
        [
            f"{constants.VPN_ENV_PATTERN.format(name=config_name, property=name)}={value}"
            for name, value in zip(constants.PROPERTIES, [config_file, username, password])
        ]
    )

    with open(write_to, 'w') as file:
        file.write(
            data + '\n' + new_config
        )


def validate_file_exists(filename: str):
    if os.path.exists(filename):
        pass
    else:
        raise FileNotFoundError(f"The file '{filename}' was not found")


def read_config(name: str, read_from: str = constants.PROFILE_FILE) -> dict:
    try:
        validate_file_exists(read_from)
    except FileNotFoundError as e:
        raise(FileNotFoundError(str(s) + ". Create a configuration file by running 'sudo openvpn3_handler config'"))

    littlenv.load(path=read_from[:-4])

    config = {
        prop: os.getenv(
            constants.VPN_ENV_PATTERN.format(name=name, property=prop)
        )
        for prop in [constants.PROPERTY_PATH, constants.PROPERTY_USERNAME, constants.PROPERTY_PASSWORD]
    }
    if all([item is None for item in config.values()]):
        raise ValueError(
            f"Config for '{name}' was not found in '{read_from}'"
        )

    return config


class Menu:
    def __init__(self, *args):
        self._flag = args[0] if len(args) > 0 else constants.CHECK_FLAG
        self._name = args[1] if len(args) > 1 else constants.DEFAULT_NAME
        self._read_from = args[2] if len(args) > 2 else constants.PROFILE_FILE

        if not self.check_sudo():
            command = f"sudo openvpn3_handler {args}".replace("'", '"')
            raise ValueError(f"Please re run with sudo privileges: '{command}'")

            sys.exit(1)

        if self._flag == constants.CONFIG_FLAG:
            self._flag, self._name, self._read_from = self.config_menu()

        self._config = read_config(self._name, self._read_from)

        self._username = self._config[constants.PROPERTY_USERNAME]
        self._password = self._config[constants.PROPERTY_PASSWORD]
        self._path = self._config[constants.PROPERTY_PATH]

        if self._flag == constants.START_FLAG:
            if self._path in self.check():
                self.stop()
            self.start()

        elif self._flag == constants.STOP_FLAG:
            self.stop()
        elif self._flag == constants.RESTART_FLAG:
            self.restart()
        else:
            print(
                self.check()
            )

    @staticmethod
    def check_sudo():
        return os.geteuid() == 0

    @staticmethod
    def config_menu():
        readline = autocomplete_input()

        path = ''
        while not os.path.exists(path):
            path = input(constants.INPUT_PROPERTY.format(property='PATH'))

        username = input(constants.INPUT_PROPERTY.format(property='USERNAME'))
        password = getpass(constants.INPUT_PROPERTY.format(property='PASSWORD'))
        config_name = input(f'CONFIG_NAME [{constants.DEFAULT_NAME}]: ')
        config_name = config_name if config_name else constants.DEFAULT_NAME

        write_to = input(f'WRITE_TO [{constants.PROFILE_FILE}]: ')
        write_to = write_to if write_to else constants.PROFILE_FILE

        write_config(
            username=username,
            password=password,
            config_name=config_name,
            config_file=path,
            write_to=write_to
        )

        autostart = input("AUTO START [Y]: ")
        if autostart in ['y', 'Y']:
            return constants.START_FLAG, config_name, write_to

        return sys.exit(1)

    def start(self):
        command = constants.VPN_START_COMMAND.format(path=self._path)
        child = pexpect.spawn(
            command,
            encoding='utf-8'
        )

        #child.logfile = sys.stdout
        child.logfile = StringIO()

        # Regular expressions
        child.expect_exact("Auth User name: ")
        child.sendline(self._username)
        child.expect_exact("Auth Password: ")
        child.sendline(self._password)
        child.expect_exact(pexpect.EOF)

    @staticmethod
    def _run(command: str, *args, **kwargs):
        return run(
            command.split(' '),
            *args,
            **kwargs
        )

    def stop(self):
        self._run(
            constants.VPN_STOP_COMMAND.format(
                path=self._path
            )
        )

    def restart(self):
        self.stop()
        self.start()

    def check(self):
        check_output = self._run(
            constants.VPN_CHECK_COMMAND,
            stdout=PIPE
        ).stdout.decode()

        return check_output


def autocomplete_input():
    """
    Función que permite activar la posibilidad de autocompletar para directorios en la función `input`

    Returns
    -------
    readline
    """
    import readline
    import glob

    def complete(text, state):
        return (glob.glob(os.path.expanduser(text) + '*') + [None])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return readline
