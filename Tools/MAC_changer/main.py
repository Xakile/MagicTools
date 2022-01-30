#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface to change its MAC address')
    parser.add_option('-m', '--mac', dest='mac', help='New MAC address')
    (options, argumets) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info')
    elif not options.mac:
        parser.error('[-] Please specify a new MAC, use --help for more info')
    return options

def change_mac(interface, mac):
    print(f'[+] Changing MAC address for {interface} to {mac}')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"Current MAC: {current_mac}")

change_mac(options.interface, options.mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac:
    print(f"[+] MAC address was successfully changed to {current_mac}.")
else:
    print("[-] MAC address did not get changed.")

