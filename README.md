# Eac3to Audio Delay

A Python utility that uses [eac3to](https://www.videohelp.com/software/eac3to) to adjust audio delay based on frame count or a directly specified millisecond value.

The script supports batch processing, drag-and-drop operation, custom output paths, and automatic logging.

## Features

- **Frame-based delay:** Calculate audio delay using a selected framerate and frame offset.
- **Millisecond-based delay:** Enter the desired delay directly in milliseconds.
- **8 supported framerates:** Including fractional framerates such as 23.976 and 29.970 fps.
- **Batch processing:** Process multiple files in one operation.
- **Drag and drop:** Accept files and folders directly.
- **Recursive scanning:** Automatically scan subdirectories.
- **Custom output:** Specify an output path for single-file processing.
- **Automatic naming:** Prefix output filenames with `synced_`.
- **Logging:** Save eac3to log files in the script directory.
- **Overwrite protection:** Skip files when the output already exists.

## Requirements

- Windows
- Python 3.9 or later
- [eac3to](https://www.videohelp.com/software/eac3to)

### Configuration

Before running the script, configure the path to `eac3to.exe`.

Open `Eac3to_Audio_Delay.py` and locate:

```python
EAC3TO = r"I:\Software\Tools\Eac3to\eac3to.exe"
```

Replace the path with the actual location of your eac3to executable.

## Command-Line Options

| Option | Description |
|---|---|
| `-h`, `--help` | Display help information |
| `-v`, `--version` | Display version information |
| `-i`, `--input` | Specify input files or folders |
| `-o`, `--output` | Specify the output file path (single input only) |
| `-d`, `--delay` | Specify audio delay in frames |
| `-f`, `--framerate` | Select framerate (1–8) |
| `-m`, `--milliseconds` | Specify audio delay directly in milliseconds |

`-d` and `-m` are mutually exclusive.

## Supported Framerates

| Option | Framerate |
|:---:|:---|
| 1 | 23.976 fps (24000/1001) |
| 2 | 24 fps |
| 3 | 25 fps |
| 4 | 29.970 fps (30000/1001) |
| 5 | 30 fps |
| 6 | 50 fps |
| 7 | 59.940 fps (60000/1001) |
| 8 | 60 fps |

## Usage

### 1. Frame-Based Delay

Specify a framerate and the desired delay in frames.

```bash
Eac3to_Audio_Delay.py -i "audio.ac3" -f 1 -d -16
```

This example applies a delay of -16 frames at 23.976 fps, equivalent to approximately -667 ms.

If the framerate is omitted, the script prompts you to select one.

```bash
Eac3to_Audio_Delay.py -i "audio.ac3" -d -16
```

### 2. Millisecond-Based Delay

Specify the delay directly in milliseconds without selecting a framerate.

```bash
Eac3to_Audio_Delay.py -i "audio.ac3" -m -667
```

Positive and negative values are supported.

```bash
Eac3to_Audio_Delay.py -i "audio.ac3" -m 500
```

### 3. Custom Output Path

Use `-o` to specify the output filename and location.

```bash
Eac3to_Audio_Delay.py -i "audio.ac3" -m -667 -o "output.ac3"
```

Custom output paths are supported when processing exactly one input file.

### 4. Batch Processing

Process multiple files in one operation.

```bash
Eac3to_Audio_Delay.py -i "audio1.ac3" "audio2.dts" -f 1 -d -16
```

Process an entire folder, including its subdirectories.

```bash
Eac3to_Audio_Delay.py -i "I:\Audio" -m -667
```

### 5. Drag and Drop

Drag one or more supported files or folders onto the Python script.

The script will prompt you to select a delay mode:

1. Frames
2. Milliseconds

Follow the prompts to configure the delay.

### 6. Interactive Mode

Run the script without arguments:

```bash
Eac3to_Audio_Delay.py
```

The script will prompt for input paths, delay mode, and the required parameters.

## Delay Calculation

Frame-based delay is converted into milliseconds using:

```text
Delay (ms) = Frames / Framerate × 1000
```

The result is rounded to the nearest millisecond.

Example at 23.976 fps:

| Frames | Delay |
|---:|---:|
| -16 | -667 ms |
| -8 | -334 ms |
| +8 | +334 ms |
| +16 | +667 ms |

## Supported File Formats

`.mkv`, `.mka`, `.mp4`, `.m4v`, `.mov`, `.ts`, `.m2ts`, `.mts`, `.avi`, `.mpg`, `.mpeg`, `.vob`, `.webm`, `.mp3`, `.m4a`, `.aac`, `.ac3`, `.eac3`, `.dts`, `.thd`, `.wav`, `.flac`, `.ogg`, `.opus`, `.wma`

Actual processing support depends on eac3to and the input format.

## Output

By default, processed files are saved alongside their original files with the `synced_` prefix.

Example:

```text
Input:
I:\Audio\cmt.eng.ac3

Output:
I:\Audio\synced_cmt.eng.ac3
```

Existing output files are skipped to prevent accidental overwriting.

## Log Files

eac3to log files are saved in the same directory as `Eac3to_Audio_Delay.py`.

Log filenames are based on the original input filenames.

Example:

```text
Eac3to-Audio-Delay/
├── Eac3to_Audio_Delay.py
├── cmt.eng.log
├── audio1.log
└── audio2.log
```

## Notes

- Original input files are never modified.
- Files with the `synced_` prefix are automatically excluded.
- Existing output files are skipped.
- `-d` and `-m` cannot be used together.
- `-f` is only applicable to frame-based delay.
- Custom output paths (`-o`) support one input file at a time.
- Log files with identical source filenames may overwrite each other when processing files from different directories.

## License

MIT License
