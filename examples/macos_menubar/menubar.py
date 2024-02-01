"Display battery status in the macOS menubar."

from battery import percent, is_charging, is_discharging, minutes_to_empty, minutes_to_full, capacity, design_capacity
import rumps

def timestring():
    time = None  # type: int | None
    status = ""
    if is_charging():
        status = "⚡️"
        time = minutes_to_full()
    elif is_discharging():
        time = minutes_to_empty()

    timestring = ''
    if time:
        h, m = divmod(time, 60)
        timestring = f'{h}h{m:02d}m'.removeprefix('0h')

    return " ".join((
        f"{percent()}%",
        status,
        timestring,
    )).strip()

class BatteryStatus(rumps.App):
    @rumps.timer(10)
    def update_menu(self, _):
        self.title = timestring()

    @rumps.timer(60 * 60)
    def update_capacity(self, _):
        self.quit_button.title = f"Capacity: {capacity() / design_capacity()*100:4.1f}%"

if __name__ == "__main__":
    BatteryStatus("BatteryStatus", "??% ?:??").run()