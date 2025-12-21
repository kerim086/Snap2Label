from mss import mss, tools
from pathlib import Path
import time
import keyboard
import re

class Screenshoter:
    FRAME_RE = re.compile(r"^frame_(\d{6})\.png$")

    def __init__(self, path: Path, monitor: int = 1):
        self.sct = mss()
        self.path = path
        self.monitor = monitor
        self.path.mkdir(parents=True, exist_ok=True)
        self.count = self.count_from_existing_files()

    def count_from_existing_files(self) -> int:
        max_num = 0
        for p in self.path.glob("frame_*.png"):
            m = self.FRAME_RE.match(p.name)
            if not m:
                continue
            num = int(m.group(1))
            if num > max_num:
                max_num = num
        return max_num

    def take_screenshot(self) -> Path:
        self.count += 1
        filename = f"frame_{self.count:06d}.png"
        path = self.path / filename

        monitor_region = self.sct.monitors[self.monitor]
        shot = self.sct.grab(monitor_region)
        tools.to_png(shot.rgb, shot.size, output=str(path))

        return path


def main():
    path = Path("dataset/images/train")
    shooter = Screenshoter(path=path, monitor=1)

    print("Capturing... Press ESC to stop")
    while True:
        if keyboard.is_pressed("esc"):
            break

        saved_to = shooter.take_screenshot()
        print(f"Saved to: {saved_to}")
        time.sleep(1)


if __name__ == "__main__":
    main()