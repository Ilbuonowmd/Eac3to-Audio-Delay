
import argparse
import math
import shlex
import subprocess
from pathlib import Path

# ============================================================
# Eac3to Audio Delay
# Version: 1.1.0
# ============================================================

SCRIPT_NAME = "Eac3to Audio Delay"
VERSION = "1.1.0"

# ============================================================
# Configuration
# ============================================================

# Path to the eac3to executable.
# Update this path if eac3to.exe is installed in a different location.
EAC3TO = r"I:\Software\Tools\Eac3to\eac3to.exe"

# ============================================================
# Framerate Options
# ============================================================

FRAMERATES = {
    1: ("23.976 fps", 24000 / 1001),
    2: ("24 fps", 24.0),
    3: ("25 fps", 25.0),
    4: ("29.970 fps", 30000 / 1001),
    5: ("30 fps", 30.0),
    6: ("50 fps", 50.0),
    7: ("59.940 fps", 60000 / 1001),
    8: ("60 fps", 60.0),
}

SUPPORTED_EXTENSIONS = {
    ".mkv", ".mka", ".mp4", ".m4v", ".mov",
    ".ts", ".m2ts", ".mts", ".avi", ".mpg",
    ".mpeg", ".vob", ".webm", ".mp3", ".m4a",
    ".aac", ".ac3", ".eac3", ".dts", ".thd",
    ".wav", ".flac", ".ogg", ".opus", ".wma"
}


# ============================================================
# Console
# ============================================================

def print_banner():
    print("=" * 55)
    print(f"  {SCRIPT_NAME} v{VERSION}")
    print("  Audio delay adjustment using eac3to")
    print("=" * 55)


# ============================================================
# Argument Parser
# ============================================================

def create_parser():
    parser = argparse.ArgumentParser(
        prog="Eac3to_Audio_Delay",
        description="Apply audio delay using eac3to.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:

  Eac3to_Audio_Delay.py -i "audio.ac3" -f 1 -d -16
  Eac3to_Audio_Delay.py -i "audio.ac3" -m -667
  Eac3to_Audio_Delay.py -i "audio.ac3" -m 500 -o "output.ac3"
  Eac3to_Audio_Delay.py -i "Folder" -f 1 -d -16

Framerate options:
  1 = 23.976 fps
  2 = 24 fps
  3 = 25 fps
  4 = 29.970 fps
  5 = 30 fps
  6 = 50 fps
  7 = 59.940 fps
  8 = 60 fps
"""
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"{SCRIPT_NAME} v{VERSION}"
    )

    parser.add_argument(
        "-i", "--input",
        nargs="+",
        metavar="PATH",
        help="Input files or folders"
    )

    parser.add_argument(
        "-o", "--output",
        metavar="PATH",
        help="Output file path (single input file only)"
    )

    delay_group = parser.add_mutually_exclusive_group()

    delay_group.add_argument(
        "-d", "--delay",
        type=int,
        metavar="FRAMES",
        help="Audio delay in frames (positive or negative)"
    )

    delay_group.add_argument(
        "-m", "--milliseconds",
        type=int,
        metavar="MS",
        help="Audio delay directly in milliseconds"
    )

    parser.add_argument(
        "-f", "--framerate",
        type=int,
        choices=range(1, 9),
        metavar="1-8",
        help="Framerate menu option (1-8)"
    )

    parser.add_argument(
        "paths",
        nargs="*",
        help="Input files or folders (drag and drop)"
    )

    return parser


# ============================================================
# User Input
# ============================================================

def get_framerate(selection=None):
    print("\nSelect framerate:")

    for number, (label, _) in FRAMERATES.items():
        print(f"  {number}. {label}")

    while True:
        raw = str(selection) if selection is not None else input(
            "\nChoose (1-8): "
        ).strip()

        selection = None

        try:
            number = int(raw)

            if number in FRAMERATES:
                label, fps = FRAMERATES[number]
                print(f"Selected: {label}")
                return fps

        except ValueError:
            pass

        print("Invalid choice. Please select 1-8.")


def get_frames(value=None):
    while True:
        raw = str(value) if value is not None else input(
            "\nDelay in frames (e.g. -16): "
        ).strip()

        value = None

        try:
            return int(raw)

        except ValueError:
            print("Invalid frame count. Please enter an integer.")


def get_milliseconds(value=None):
    while True:
        raw = str(value) if value is not None else input(
            "\nDelay in milliseconds (e.g. -667): "
        ).strip()

        value = None

        try:
            return int(raw)

        except ValueError:
            print("Invalid delay. Please enter an integer.")


def get_delay(args):
    if args.milliseconds is not None:
        return args.milliseconds, None, None

    if args.delay is not None:
        fps = get_framerate(args.framerate)
        frames = args.delay

    elif args.framerate is not None:
        fps = get_framerate(args.framerate)
        frames = get_frames()

    else:
        print("\nSelect delay mode:")
        print("  1. Frames")
        print("  2. Milliseconds")

        while True:
            choice = input("\nChoose (1-2): ").strip()

            if choice == "1":
                fps = get_framerate()
                frames = get_frames()
                break

            elif choice == "2":
                delay_ms = get_milliseconds()
                return delay_ms, None, None

            print("Invalid choice. Please select 1 or 2.")

    delay_ms = calculate_delay(frames, fps)

    return delay_ms, fps, frames


# ============================================================
# File Handling
# ============================================================

def collect_files(paths):
    files = []

    for item in paths:
        path = Path(item.strip('"')).resolve()

        if path.is_file():
            if (
                path.suffix.lower() in SUPPORTED_EXTENSIONS
                and not path.stem.lower().startswith("synced_")
            ):
                files.append(path)
            else:
                print(f"Skipped: {path}")

        elif path.is_dir():
            for file in path.rglob("*"):
                if (
                    file.is_file()
                    and file.suffix.lower() in SUPPORTED_EXTENSIONS
                    and not file.stem.lower().startswith("synced_")
                ):
                    files.append(file)

        else:
            print(f"Path not found: {path}")

    return list(dict.fromkeys(files))


# ============================================================
# Delay Calculation
# ============================================================

def calculate_delay(frames, fps):
    raw_delay = frames / fps * 1000

    delay_ms = math.copysign(
        math.floor(abs(raw_delay) + 0.5),
        raw_delay
    )

    return int(delay_ms)


# ============================================================
# Processing
# ============================================================

def process_file(source, delay_ms, output=None):
    if output is not None:
        destination = output
    else:
        destination = source.with_name(
            f"synced_{source.name}"
        )

    # Save logs in the same directory as this script.
    script_dir = Path(__file__).resolve().parent
    log_file = script_dir / f"{source.stem}.log"

    if destination.resolve() == source.resolve():
        print("\nError: Input and output paths are identical.")
        return False

    if destination.exists():
        print(f"\nSkipped: Output already exists:\n{destination}")
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)

    delay_option = f"{delay_ms:+d}ms"

    command = [
        EAC3TO,
        str(source),
        str(destination),
        delay_option,
        f"-log={log_file}"
    ]

    print("\n" + "=" * 65)
    print(f"Input        : {source}")
    print(f"Output       : {destination}")
    print(f"Log          : {log_file}")
    print(f"Delay        : {delay_ms:+d} ms")

    print("\nCommand:")
    print(subprocess.list2cmdline(command))

    try:
        result = subprocess.run(command)

        if result.returncode == 0 and destination.exists():
            print("\nSuccess.")
            print(f"Output saved: {destination}")
            print(f"Log saved   : {log_file}")
            return True

        print(f"\nFailed. Exit code: {result.returncode}")

        if destination.exists():
            destination.unlink()

        if log_file.exists():
            print(f"Log saved: {log_file}")

        return False

    except Exception as exc:
        print(f"\nError: {exc}")
        return False


# ============================================================
# Main
# ============================================================

def main():
    print_banner()

    parser = create_parser()
    args = parser.parse_args()

    if not Path(EAC3TO).is_file():
        print(f"\neac3to not found:\n{EAC3TO}")
        input("\nPress Enter to exit...")
        return

    # Framerate is only relevant when using frame-based delay.
    if args.milliseconds is not None and args.framerate is not None:
        parser.error("-f/--framerate cannot be used with -m/--milliseconds")

    paths = []

    if args.input:
        paths.extend(args.input)

    if args.paths:
        paths.extend(args.paths)

    if not paths:
        print("\nPaste file/folder paths below.")
        raw = input("> ").strip()

        if raw:
            paths = shlex.split(raw, posix=False)

    files = collect_files(paths)

    if not files:
        print("\nNo supported files found.")
        input("\nPress Enter to exit...")
        return

    if args.output and len(files) != 1:
        print("\nError: -o/--output requires exactly one input file.")
        input("\nPress Enter to exit...")
        return

    print(f"\nFound {len(files)} file(s).")

    delay_ms, fps, frames = get_delay(args)

    print("\n" + "=" * 65)
    print("Processing configuration")

    if fps is not None:
        print(f"Framerate    : {fps:.6f} fps")
        print(f"Frames       : {frames:+d}")

    print(f"Delay        : {delay_ms:+d} ms")
    print("=" * 65)

    success = 0
    failed = 0

    output = Path(args.output).resolve() if args.output else None

    for source in files:
        if process_file(source, delay_ms, output):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 65)
    print("Processing completed.")
    print(f"Successful   : {success}")
    print(f"Failed/Skip  : {failed}")
    print("=" * 65)

    input("\nFinished. Press Enter to exit...")


if __name__ == "__main__":
    main()
