#! /usr/bin/env python3
'''
Cross-platform battery status package in Python.
'''

# SOURCES
# Windows: https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-battery

from platform import system
from os import popen

class BatteryError(Exception):
    "Cannot load a certain property."


def _get_win32_battery(key: str):
    status = popen(f'WMIC PATH Win32_Battery Get {key}')
    if status.readline().strip() != key:
        raise BatteryError(f'Windows: unknown key {key}.')
    result = status.readline().strip()
    if not result:
        raise BatteryError(f'Windows: key {key} not supported on this device.')

    return result

def _darwin_ioreg(key: str):
    return int(popen(rf"ioreg -l -w0 | grep '\"{key}\" = ' | grep -Eo '\d+'").read())


def active():
    "Return True iff the device is on battery."
    if system() == 'Darwin':
        return 'Battery' in popen('pmset -g batt | head -n1').read()
    if system() == 'Windows':
        return _get_win32_battery('BatteryStatus') in ['1', '4', '5']  # discharging, low, critical
    return NotImplemented

def percent():
    "Return percentage charge of battery in [0, 100]."
    if system() == 'Darwin':
        percentage = popen(r"pmset -g batt | grep InternalBattery | grep -Eo '\d+%'").read()
        return float(percentage[:-2])
    if system() == 'Windows':
        return float(_get_win32_battery('EstimatedChargeRemaining'))
    return NotImplemented

def capacity():
    "Return actual current capacity in mAh."
    if system() == 'Darwin':
        return _darwin_ioreg('MaxCapacity')
    if system() == 'Windows':
        return float(_get_win32_battery('FullChargeCapacity'))
    return NotImplemented

def design_capacity():
    """
    Return battery's original design capacity in mAh.
    
    (In Windows, this is multiplied by voltage and in mWh).
    """
    if system() == 'Darwin':
        return _darwin_ioreg('DesignCapacity')
    if system() == 'Windows':
        return float(_get_win32_battery('DesignCapacity'))
    return NotImplemented
