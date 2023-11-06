#!/bin/python3

import subprocess
import re

def wireless_card_check():
    try:
        is_installed = subprocess.check_output(["ifconfig"], universal_newlines=True)
        interface = re.findall(r'wlan\d+', is_installed)
        if not interface:
            return str("No wireless card installed.")
        for int in interface:
            print(int)
        
        try:
            monitor_mode = subprocess.check_output(["airmon-ng", "start", int], universal_newlines=True)
            print(monitor_mode)
            problematic_process = re.findall(r"Kill", monitor_mode)
            
            if problematic_process is not None:
                subprocess.run(["airmon-ng", "check", "kill"])
                monitor_mode = subprocess.check_output(["airmon-ng", "start" , str(int)], universal_newlines=True)
                
            try:
                check_mode = subprocess.check_output(["iwconfig"], universal_newlines=True)
                mode = re.findall(r"Mode:Monitor", check_mode)
                
                # try:
                #     subprocess.run(["ifconfig", int, "down"])
                #     check_int = subprocess.check_output("ifconfig", universal_newlines=True)
                #     int_down = re.findall(r"$int", check_int)
                    
            except subprocess.CalledProcessError:
                return str("Something went wrong! Try again.")
            except Exception as e:
                return e
        except subprocess.CalledProcessError:
            return str("Unknown error during turning on monitor mode.")
        except Exception as e:
            return e
    except subprocess.CalledProcessError:
        return str("Unknown error of calling 'ifconfig'.")
    except Exception as e:
        return e

print(wireless_card_check())

