from mss import mss, tools
from pathlib import Path
import time
import keyboard
import re
from datetime import datetime

class Screenshoter:
    FRAME_RE = re.compile(r"^frame_(\d{6})\.png$")

    def __init__(self, out_dir: Path, monitor: int = 1):
        self.sct = mss()
        self.out_dir = out_dir
        self.monitor = monitor

        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.count = self.count_from_existing_files()

    def count_from_existing_files(self) -> int:
        max_num = 0
        for p in self.out_dir.glob("frame_*.png"):
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
        path = self.out_dir / filename

        monitor_region = self.sct.monitors[self.monitor]
        shot = self.sct.grab(monitor_region)
        tools.to_png(shot.rgb, shot.size, output=str(path))

        return path

def create_session_dir(base: Path = Path("dataset")) -> Path:
    session_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return base / session_name / "images"

def main():
    session_images_dir = create_session_dir()
    shooter = Screenshoter(out_dir=session_images_dir, monitor=1)

    print("Capturing... Press ESC to stop")
    print(f"Session folder: {session_images_dir}")
    print("Press X to manually capture and save the image")
    while True:
        if keyboard.is_pressed("esc"):
            break

        if keyboard.is_pressed("X"):
            saved_to = shooter.take_screenshot()
            print(f"Saved to: {saved_to}")

        saved_to = shooter.take_screenshot()
        print(f"Saved to: {saved_to}")
        time.sleep(1)


if __name__ == "__main__":
    main()