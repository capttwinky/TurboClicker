# Turbo Clicker

High-speed clicking automation tool for Windows. Perform millions of clicks or click continuously for a specified duration.

## Prerequisites

Install [UV](https://docs.astral.sh/uv/) for Python package management:

**Windows PowerShell (Recommended):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative methods:**
- **winget**: `winget install astral-sh.uv`
- **scoop**: `scoop install uv`  
- **pipx**: `pipx install uv`

**Verify installation:**
```powershell
uv --version
```

Dependencies (PyAutoGUI, keyboard) are installed automatically when you run the script.

## Features

- **Count or Time-based**: Click N times or for N seconds
- **Emergency Controls**: F12 stop, F9 pause/resume (customizable)
- **TURBO Mode**: Maximum clicking speed (500-1000+ CPS)
- **Interactive or Coordinate-based**: Click at mouse position or specific coordinates
- **Real-time Progress**: Live CPS and completion estimates
- **Safety**: Mouse corner failsafe, confirmation prompts

## Quick Start
Open PowerShell, 
`cd` to the dirctory your files are in and ....

**Step 1:** Open PowerShell and navigate to your TurboClicker directory:
```powershell
cd c:\Users\YourName\path\to\TurboClicker
```

**Step 2:** Choose your clicking method:

```powershell
# Basic clicking (interactive coordinate selection)
uv run --with pyautogui --with keyboard turbo_clicker.py

# Click 100,000 times at current mouse position
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --verbose

# Click for 30 seconds at maximum speed
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=30 --turbo-mode

# Click at specific coordinates
uv run --with pyautogui --with keyboard turbo_clicker.py --x=400 --y=300 --clicks=50000
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--clicks, -c` | Number of clicks | 1,000,000 |
| `--duration, -t` | Duration in seconds | None |
| `--x`, `--y` | Click coordinates | Current mouse position |
| `--delay, -d` | Delay between clicks | 0.0 |
| `--turbo-mode` | Maximum speed mode | Off |
| `--verbose, -v` | Show progress | Off |
| `--confirm` | Skip confirmation | Off |
| `--emergency-hotkey` | Emergency stop key | f12 |
| `--pause-hotkey` | Pause/resume key | f9 |
| `--pause-interval` | Pause every N clicks/seconds | 0 (disabled) |

## Emergency Controls

- **F12**: Emergency stop (instant)
- **F9**: Pause/resume toggle
- **Mouse to top-left corner**: PyAutoGUI failsafe
- **Ctrl+C**: Keyboard interrupt

Hotkeys work globally (even when terminal not focused).

## Performance Modes

| Mode | Speed (CPS) | Command |
|------|-------------|---------|
| Normal | 100-300 | Default |
| Turbo | 500-1000+ | `--turbo-mode` |
| Controlled | Custom | `--delay=0.1` |

## Common Use Cases

**Gaming/Idle Clickers:**
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --x=640 --y=360 --clicks=1000000 --turbo-mode
```

**Stress Testing:**
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=120 --turbo-mode --verbose
```

**Rate-Limited Applications:**
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --delay=0.1
```

## Safety & Ethics

Use responsibly:
- Personal automation only
- Respect application ToS
- Software testing/QA purposes
- Educational use

## Interactive Mode for Beginners

When you don't specify coordinates, the script enters interactive mode:

```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --verbose
```

**What happens:**
1. Script prompts: "Move your mouse to the desired position and press Enter..."
2. Position your mouse where you want to click
3. Press Enter
4. Script shows: "Will click at current mouse position: (X, Y)"
5. Confirmation prompt appears (unless `--confirm` is used)
6. Hotkeys are activated: "🔥 Emergency stop hotkey: F12" and "⏸️ Pause/Resume toggle: F9"
7. Clicking begins

## Troubleshooting

**"'uv' is not recognized as an internal or external command"**
- UV is not installed or not in PATH
- Install UV using the PowerShell command above
- Restart PowerShell after installation

**"keyboard module not available" warning**
- Hotkeys will be disabled but script still works
- UV automatically installs keyboard module with `--with keyboard`
- Ensure you're using the full command: `uv run --with pyautogui --with keyboard turbo_clicker.py`

**Script stops immediately**
- Check that coordinates are within screen bounds
- Ensure target application window is visible and active
- Verify PyAutoGUI failsafe isn't triggering (mouse in top-left corner)

**Slower than expected performance**
- Use `--turbo-mode` for maximum speed
- Reduce or eliminate `--delay` values
- Close unnecessary background applications

**Coordinates not working**
- Verify X,Y coordinates are correct for your screen resolution
- Use interactive mode to capture exact coordinates
- Check if target application moved or resized

## System Requirements

**Minimum:**
- Windows 10 or later
- 4GB RAM
- 100MB free disk space
- Active desktop session

**Recommended:**
- Windows 11
- 8GB+ RAM
- SSD storage
- Multiple monitors supported

## Performance Tips

1. **Use Turbo Mode**: `--turbo-mode` for maximum clicking speed
2. **Skip Confirmations**: Use `--confirm` for automated operation
3. **Monitor Progress**: Use `--verbose` to see real-time performance
4. **Close Background Apps**: Free up system resources for maximum speed
5. **Use Specific Coordinates**: Faster than interactive coordinate capture

---

**TLDR:**
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --help
```