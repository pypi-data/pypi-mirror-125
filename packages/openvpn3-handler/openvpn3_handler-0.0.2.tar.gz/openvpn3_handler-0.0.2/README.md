# OpenVPN3 Handler

Tool develop to easily handle connections with OpenVPN3 in **Linux**.

## Install `openvpn3`
Go to [openvpn.net](https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/) and install following the instructions

## Install handler
When installing the handler is important to use be super user, thus install by running:
```
sudo pip install openvpn3_handler
```

If using an old distribution in Linux use:
```
sudo pip3 install openvpn3_handler
```

## Configure handler
```
sudo openvpn3_handler config
```

Follow the instructions, the following variables are required:
- `PATH`: **Absolute** path to the `.opvn` file
- `USERNAME`: Username in the credentials of the openvpn configuration
- `PASSWORD`: Password in the openvpn configuration
- `CONFIG_NAME`: Name of the current configuration (keep the default value, unless multiple configurations are needed)
- `WRITE_TO`: Where to store the credentials (keep the default value `/root/.openvpn3.env`, unless you know what you are doing)

