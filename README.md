# Yunjiaocai Auto-Scroll Tool

<p>
  <a href="./README.md"><img src="https://img.shields.io/badge/Docs-English-2563EB?style=flat-square" alt="English" /></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/%E6%96%87%E6%A1%A3-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-64748B?style=flat-square" alt="简体中文" /></a>
</p>

> Original Development Date: 2025-06-16

A Windows desktop utility that automatically simulates mouse scrollbar dragging and scrolling operations, primarily designed for digital textbook platforms (such as Yunjiaocai) and other continuous-reading scenarios.

## Features

- 🖱️ **Smart Mouse Control**: Simulates holding and dragging a scrollbar thumb up and down
- ⌨️ **Global Hotkeys**: Supports customizable global shortcuts to start or stop scrolling anytime
- ⚙️ **Adjustable Parameters**: Customize scroll distance, interval speed, and total duration
- 🎯 **Multiple Modes**: Supports scrolling upward, downward, or alternating back-and-forth
- 💾 **Persistent Settings**: Automatically saves user configuration to disk
- 🖥️ **Clean GUI**: Intuitive and lightweight graphical user interface
- 📦 **One-Click Packaging**: Easily bundle into a standalone `.exe` executable

## System Requirements

- Windows 7 / 8 / 10 / 11
- Python 3.7+ (when running from source)
- Administrator privileges (required for global hotkey listening on Windows)

## Quick Start

### Option 1: Run the Standalone Executable

1. Download the packaged `.exe` file
2. Right-click and select **Run as administrator**
3. Configure your preferred parameters and save settings
4. Hover the mouse cursor over the target scrollbar thumb
5. Press the configured global hotkey to start automatic scrolling

### Option 2: Run from Source

1. **Clone the repository**
```bash
git clone <repository-url>
cd yunjiaocaijs
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch the application**
```bash
python main.py
```

## Usage Guide

### Basic Workflow

1. **Launch**: Double-click the `.exe` executable or run `python main.py`
2. **Configure Parameters**:
   - **Hotkey**: Key combination to toggle scrolling (default: `Ctrl+Shift+S`)
   - **Scroll Distance**: Pixel distance per movement step (`10–500` px)
   - **Scroll Speed**: Time interval between movement steps (`0.01–1.0` s)
   - **Duration**: Total auto-scrolling time (`1–300` s)
   - **Scroll Direction**: `up`, `down`, or alternating up-and-down
3. **Save Configuration**: Click the **"Save Config"** button
4. **Test**: Click **"Test Scroll"** to verify behavior
5. **Start Scrolling**:
   - Position the mouse cursor directly over the target scrollbar thumb
   - Press your configured hotkey to begin scrolling
   - Press the hotkey again at any time to stop scrolling

### Parameter Reference

| Parameter | Description | Recommended Value |
|-----------|-------------|-------------------|
| Hotkey | Key combination to start/stop scrolling | `ctrl+shift+s` |
| Scroll Distance | Pixels moved per step | `100–200` |
| Scroll Speed | Delay interval between steps | `0.1–0.3` s |
| Duration | Total scrolling duration | `10–60` s |
| Scroll Direction | Movement direction | `down` (downward) |

### Tips for Best Results

1. **Precise Cursor Placement**: Place the mouse cursor accurately on the scrollbar thumb before triggering
2. **Active Window**: Make sure the target application window is focused in the foreground
3. **Tune Parameters First**: Use the **"Test Scroll"** button to fine-tune distance and speed
4. **Avoid Shortcut Conflicts**: Pick a hotkey combination that does not clash with other active software
5. **Administrator Mode**: Run as administrator so global hotkeys register reliably across windows

## Packaging into an Executable

### Automated Build

Run the included build script:
```bash
python build.py
```

The script automatically:
1. Installs required dependencies
2. Invokes PyInstaller
3. Generates a single-file `.exe` executable
4. Copies `config.json` alongside the output

### Manual Build

```bash
# Install PyInstaller
pip install pyinstaller

# Build single-file windowed executable
pyinstaller --onefile --windowed --name=云教材刷课工具 --add-data=config.json;. main.py
```

The packaged executable will be output to the `dist` directory.

## Configuration File

User preferences are stored in `config.json`:

```json
{
  "hotkey": "ctrl+shift+s",
  "scroll_distance": 100,
  "scroll_speed": 0.1,
  "scroll_duration": 10,
  "scroll_direction": "down"
}
```

## FAQ

### Q: Why isn't the global hotkey working?
A: Make sure you run the program as **Administrator**. Windows requires elevated privileges to capture global keyboard hooks across applications.

### Q: Why is the scrolling inaccurate?
A: Ensure the cursor is positioned directly over the scrollbar thumb and adjust the **Scroll Distance** setting as needed.

### Q: The program fails to start from source?
A: Verify that all packages in `requirements.txt` are installed, or check your Python 3.7+ environment setup.

### Q: Packaging fails?
A: Ensure `pyinstaller` is installed properly in an intact Python environment.

### Q: Scrolling is too fast or too slow?
A: Adjust the **Scroll Speed** interval—smaller values produce faster movement.

## Important Notice

⚠️ **Disclaimer & Fair Use**:
- This tool is intended strictly for personal learning and technical research
- Please comply with the terms of service of any website or platform you use
- Using automation to violate platform policies is discouraged
- Ensure usage does not disrupt normal study workflows

## Tech Architecture

- **GUI Framework**: Tkinter (Python standard library)
- **Mouse Automation**: PyAutoGUI
- **Global Hotkey Listener**: `pynput`
- **Executable Bundler**: PyInstaller
- **Configuration Storage**: JSON

## Project Structure

```
yunjiaocaijs/
├── main.py              # Main GUI & automation entry point
├── config.json          # User configuration file
├── requirements.txt     # Python dependencies
├── build.py             # Automated PyInstaller build script
├── README.md            # Project documentation
└── dist/                # Packaged executable output directory
    └── 云教材刷课工具.exe
```

## Changelog

### v1.0.0 (2024-01-XX)
- ✨ Initial release
- 🖱️ Core mouse scrollbar dragging automation
- ⌨️ Global hotkey toggle support
- 🎯 Multiple scrolling directions & modes
- 💾 Persistent JSON configuration
- 📦 One-click PyInstaller build script

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Issues and Pull Requests are welcome!

## Contact

If you have questions or suggestions, feel free to reach out:
- Open a GitHub Issue
- Email: [your-email@example.com]

---

**Disclaimer**: This utility is provided solely for educational and research purposes. Users assume full responsibility for any risks arising from its use.
