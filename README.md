# Cross-platform, Python battery status

Simply `pip install battery` and use like:

```py
import battery
source = 'battery' if battery.is_discharging() else 'AC power'
print(f'On {source} at {battery.percent()}%')
health = battery.capacity() / battery.design_capacity()
print(f'Battery is at {health*100:4.1f}% health.')
```

The CLI always returns a JSON value:

```
$ python -m battery
{"is_discharging": true, "percent": 92, "minutes_to_empty": 215, "minutes_to_full": null, "capacity": 2388, "design_capacity": 4381}
$ python -m battery percent
92
```

## Functions

The following functions are available:

- `is_discharging`:        **True iff battery is discharging.**
- `is_charging`:           **True iff battery is charging.**
- `percent`:               **Integer percentage charge of battery**.
- `minutes_to_empty`:      **Minutes of battery life left.** May be empty.
- `minutes_to_full`:       **Minutes until the battery is charged.** May be empty (or 0 if full).
- `capacity`:              **The present capacity in mWh.** mAh on macOS; on Apple Silicon this may be a percentage.
- `design_capacity`:       **The factory capacity in mWh.** mAh on macOS.

The following minimum OS versions are supported:

- macOS 10.2 and later
- Linux 2.6.24 and later
- Windows Vista and later

A `NotImplementedError` is raised for unsupported OSes.

Pull requests and issues are always welcome for better compatibility! 

## Other notes

Also check out [`psutil`](https://github.com/giampaolo/psutil/)!

The whole package is **public domain**.
