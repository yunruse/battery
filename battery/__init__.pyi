def is_discharging() -> bool: ...
def is_charging() -> bool: ...
def percent() -> int: ...
def minutes_to_empty() -> int | None: ...
def minutes_to_full() -> int | None: ...
def capacity() -> int: ...
def design_capacity() -> int: ...