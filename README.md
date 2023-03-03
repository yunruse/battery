# `battery` v0.1
Cross-platform battery status package in Python.

Public domain. Uses semantic versioning. Pull requests are always welcome!

# Compatibility

|  Method           | macOS | Windows |
| :---------------- | ----- | ------- |
| `active`          | ✔️     | ✔️       |
| `percent`         | ✔️     | ✔️       |
| `capacity`        | ✔️     | ✔️       |
| `design_capacity` | ✔️     | ✔️       |

Note that:
- If a method is not supported for an OS, `NotImplemented` is returned.
- Some device drivers will not return information (a `BatteryError` is raised).
- Windows XP and below is not supported.

# Usage example

```py
import battery
source = 'battery' if battery.active() else 'AC power'
print(f'On {source} at {battery.percent()}%')
print(f'Battery is at {battery.capacity() / battery.design_capacity()*100:4.1f}% health.')
```
