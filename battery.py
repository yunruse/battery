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


def _get_win32_battery(key: str, blank_ok=False):
    status = popen(f'WMIC PATH Win32_Battery Get {key}')
    if status.readline().strip() != key:
        raise BatteryError(f'Windows: unknown key {key}.')
    result = status.readline().strip()
    if not (result or blank_ok):
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

def remaining():
    """
    The remaining battery time in minutes.
    
    May return None if not known (e.g. on charge)
    """
    if system() == 'Darwin':
        seconds = popen(r"pmset -g batt | grep discharging | grep -Eo '\d+:\d+' | awk '{S=($1*60)+$2}END{print S}' FS=:").read().strip()
        return int(seconds) if seconds else None
    if system() == 'Windows':
        seconds = _get_win32_battery('EstimatedRunTime', blank_ok=True)
        return int(seconds) if seconds else None
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
