# `battery` v1.0: Cross-platform battery status

The following functions are available:

- `is_discharging`:        Check if battery is discharging (i.e. in use).
- `is_charging`:           Check if battery is charging.
- `percent`:               Return percentage charge of battery in [0, 100].
- `minutes_remaining`:     Minutes of battery life left (may be empty if not known yet).
- `minutes_until_charged`: Minutes until the battery is charged (may be 0 if full, or empty if not on charge or not known).
- `capacity`:              Battery's current capacity in mAh (mWh on Windows).
- `design_capacity`:       Battery's original capacity in mAh (mWh on Windows).

The following OS versions are supported for these functions:

- macOS 10.2 and later
- Windows Vista and later (`minutes_until_charged` is not supported by most drivers)

A `NotImplementedError` is raised for unsupported OSes or versions.

Pull requests and issues are always welcome for better compatibility!

Semantic versioning is used.

# Usage example

As an import:

```py
import battery
source = 'battery' if battery.is_discharging() else 'AC power'
print(f'On {source} at {battery.percent()}%')
print(f'Battery is at {battery.capacity() / battery.design_capacity()*100:4.1f}% health.')
```

On the CLI:

```
$ python -m battery
{"is_discharging": true, "percent": 92, "minutes_remaining": 215, "minutes_until_charged": null, "capacity": 2388, "design_capacity": 4381}
$ python -m battery percent
92
```

# Other notes

In the unix philosophy: do a small thing well. 

As the whole package is **public domain**, please hack this code into whatever. (but tell me! I wanna see your cool stuff!)

Note that the Python is just a wrapper around the annotated `.toml` of commands that give standardised output.
(For compatibility this is converted to `.json` for use.)
