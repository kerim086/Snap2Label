from mss import mss, tools
from pathlib import Path
import time

class Screenshoter:
    def __init__(self, path: Path, monitor: int = 1):
        self.sct = mss()
        self.path = path
        self.monitor = monitor
        self.count = 0

        self.path.mkdir(parents=True, exist_ok=True)

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

    print(f"Capturing... Press CTRL+C to stop")
    try:
        while True:
            saved_to = shooter.take_screenshot()
            print(f"Saved to: {saved_to}")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()