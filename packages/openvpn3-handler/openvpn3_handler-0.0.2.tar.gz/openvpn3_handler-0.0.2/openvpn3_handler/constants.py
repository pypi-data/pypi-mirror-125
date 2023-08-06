import os

__version__: str = '0.0.2'
START_FLAG: str = 'start'
STOP_FLAG: str = 'stop'
RESTART_FLAG: str = 'restart'
CONFIG_FLAG: str = 'config'
CHECK_FLAG: str = 'check'

VPN_CHECK_COMMAND: str = "sudo openvpn3 session-manage --cleanup"
VPN_START_COMMAND: str = "sudo openvpn3 session-start --config {path}"
VPN_STOP_COMMAND: str = "sudo openvpn3 session-manage --disconnect --config {path}"

VPN_ENV_PATTERN: str = "{name}_OPENVPN3_{property}"
PROPERTY_USERNAME: str = 'USERNAME'
PROPERTY_PASSWORD: str = 'PASSWORD'
PROPERTY_PATH: str = 'PATH'

PROPERTIES: list = [
    PROPERTY_PATH,
    PROPERTY_USERNAME,
    PROPERTY_PASSWORD
]

INPUT_PROPERTY: str = '{property}='

PROFILE_FILE: str = os.path.join(
    os.path.expanduser("~"),
    '.openvpn3.env'
)

DEFAULT_NAME: str = 'DEFAULT'
