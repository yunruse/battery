# `battery` v1.0: Cross-platform battery status

The following functions are available:

- `is_discharging`:        Check if battery is discharging (i.e. in use).
- `is_charging`:           Check if battery is charging.
- `percent`:               Return percentage charge of battery in [0, 100].
- `minutes_to_empty`:      Minutes of battery life left (may be empty if not known yet).
- `minutes_to_full`:       Minutes until the battery is charged (may be 0 if full, or empty if not on charge or not known).
- `capacity`:              Battery's current capacity in mWh (mAh on macOS).
- `design_capacity`:       Battery's original capacity in mWh (mAh on macOS).

The following OS versions are supported:

- macOS 10.2 and later
- Linux 2.6.24 and later
- Windows Vista and later

A `NotImplementedError` is raised for unsupported OSes.

Pull requests and issues are always welcome for better compatibility!

# Usage example

Obtain with `pip install battery` and use like:

```py
import battery
source = 'battery' if battery.is_discharging() else 'AC power'
print(f'On {source} at {battery.percent()}%')
print(f'Battery is at {battery.capacity() / battery.design_capacity()*100:4.1f}% health.')
```

The CLI always returns a JSON value:

```
$ python -m battery
{"is_discharging": true, "percent": 92, "minutes_to_empty": 215, "minutes_to_full": null, "capacity": 2388, "design_capacity": 4381}
$ python -m battery percent
92
```

# Other notes

This package is **public domain**! Feel free to hack with it as needed.

Also check out [`psutil`](https://github.com/giampaolo/psutil/)!

Note that the Python is just a wrapper around the annotated `.toml` of commands that give standardised output.
(For maximum compatibility this is converted via `make` to a `.json` for use.)
