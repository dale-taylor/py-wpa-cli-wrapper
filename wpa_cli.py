# A simple wrapper for a few wpa_cli functions that simplifies
# the control of wifi connections.
# 
# Python 3.5+
#
# Dale Taylor
# https://github.com/dale-taylor/py-wpa-cli-wrapper
#

import subprocess
import re
from datetime import datetime

last_scan_time = None
last_scan_results = None
interface = 'wlan0' # Default interface

class WpaCliNetworkNotConfiguredError(Exception):
	pass

class WpaCliNetworkNotAvailableError(Exception):
	pass


# Set the wifi interface that will be used by other functions in this
# module
def set_interface(iface):
	global interface
	interface = iface


# Connect to the specified network if a profile for it exists,
# it is available, and it is not already connected
def connect_to(ssid):
	global interface

	networks = get_network_numbers()
	if ssid not in networks:
		raise WpaCliNetworkNotConfiguredError(ssid)

	if current_network_ssid() == ssid:
		return

	if not is_network_available(ssid):
		raise WpaCliNetworkNotAvailableError(ssid)

	subprocess.run(['wpa_cli', '-i', interface, 'select_network', networks[ssid]], stdout=subprocess.PIPE)


# Return ssid of currently connected network
def current_network_ssid():
	global interface

	result = subprocess.run(['wpa_cli', '-i', interface, 'status'], stdout=subprocess.PIPE)
	r = result.stdout.decode('utf-8')

	m = re.search('^ssid\=(.+)$', r, re.MULTILINE)

	if m is None:
		return None

	return m.group(1)


# Checks if the specified wifi network is currently available
def is_network_available(ssid):
	global last_scan_time, last_scan_results, interface

	# If a valid cached result set is not available, run a scan
	if last_scan_time is None or (datetime.now() - last_scan_time).total_seconds() > 30:
			subprocess.run(['wpa_cli', '-i', interface, 'scan'], stdout=subprocess.PIPE)
			result = subprocess.run(['wpa_cli', 'scan_results'], stdout=subprocess.PIPE)
			last_scan_results = result.stdout.decode('utf-8')
			last_scan_time = datetime.now()

	return ssid in last_scan_results


# Returns a dict that maps ssids to wpa_supplicant network numbers
def get_network_numbers():
	global interface

	result = subprocess.run(['wpa_cli', '-i', interface, 'list_networks'], stdout=subprocess.PIPE)
	r = result.stdout.decode('utf-8')

	matches = re.findall('^([\d]+)\s+([^!#;+\]\/"\t][^+\]\/"\t]{0,30}[^ +\]\/"\t]|[^ !#;+\]\/"\t][ \t]+)\s+(?:any|[a-fA-F0-9\:]+)\s+[\[\]A-Za-z0-9]*$', r, re.MULTILINE)
	networks = {}

	if matches is None:
		return networks

	for m in matches:
		key = m[1]
		val = m[0]
		networks[key] = val

	return networks
