# `battery` v0.1
Cross-platform battery status package in Python. 

Public domain. Uses semantic versioning. Pull requests are always welcome!

# Compatibility

|  Method             | macOS | Windows |
| :------------------ | ----- | ------- |
| `active`            | ✔️     | ✔️       |
| `percent`           | ✔️     | ✔️       |
| `minutes_remaining` | ✔️     | ✔️       |
| `capacity`          | ✔️     | ✔️       |
| `design_capacity`   | ✔️     | ✔️       |

Note that:
- macOS is supported for 10.2 and later.
- Windows is supported for Vista and later.

A `NotImplementedError` is raised for unsupported OSes or versions.

# Usage example

As an import:

```py
import battery
source = 'battery' if battery.is_discharging() else 'AC power'
print(f'On {source} at {battery.percent()}%')
print(f'Battery is at {battery.capacity() / battery.design_capacity()*100:4.1f}% health.')
```

On the CLI (here fetching the OS-specific command on macOS):

```
$ python -m battery
{'active': False, 'percent': 92, 'minutes_remaining': None, 'capacity': 2431, 'design_capacity': 4381}
$ python -m battery percent
92
$ python -m battery --command capacity
ioreg -l -w0 | grep '"MaxCapacity" = ' | grep -Eo '\d+'
```
