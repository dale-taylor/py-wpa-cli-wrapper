# py-wpa-cli-wrapper
A simple wrapper for a few `wpa_cli` functions that simplifies the control of wifi connections.

## Requirements
* wpa_supplicant
* wpa_cli
* Python 3.5+

## About
This wrapper does not provide functions for adding/removing wpa_supplicant network profiles. It presumes that all networks have already been configured with wpa_supplicant.

Can be used for:
* Getting the SSID of the current network (see `current_network_ssid()`)
* Checking if a network with the given SSID is available (see `is_network_available(ssid)`)
* Connecting to a different network by specifying the SSID (see `connect_to(ssid)`)

## Example Usage
Assuming wpa_cli.py is in the same directory as your script:
```python
import wpa_cli

# Use wlan1 interface (wlan0 is the default interface)
wpa_cli.set_interface('wlan1')

# Which wifi network are we connected to?
current_ssid = wpa_cli.current_network_ssid()
print("Currently connected to {}".format(current_ssid))

# Is the network MyWifiNetwork currently available?
if wpa_cli.is_network_available('MyWifiNetwork'):
  print("MyWifiNetwork is available!")
 else:
  print("MyWifiNetwork is not available.")
  
# Connect to MyWifiNetwork
try:
  wpa_cli.connect_to('MyWifiNetwork')
except WpaCliNetworkNotConfiguredError as e:
  print("{} has not been configured in wpa_supplicant".format(e))
except WpaCliNetworkNotAvailableError as e:
  print("{} is not available at the moment".format(e))

```
