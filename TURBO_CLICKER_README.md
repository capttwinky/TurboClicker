# Turbo Clicker

Ultra-high speed clicking automation tool that can perform up to 1 million clicks at maximum possible speeds OR click continuously for a specified time duration.

## Prerequisites

### Installing UV (Required)

Turbo Clicker uses [UV](https://docs.astral.sh/uv/) for fast Python package management. Install UV first:

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

### Dependencies

The script automatically manages these dependencies via UV:
- **PyAutoGUI**: Cross-platform GUI automation library
- **keyboard**: Global hotkey support for emergency stop and pause/resume

No manual installation required - UV handles everything automatically!

## Features

- **Million Click Capability**: Click up to 1,000,000 times (or any number you specify)
- **Time-Based Clicking**: Click continuously for a specified duration (seconds)
- **🚨 Emergency Stop**: Instantly stop with F12 key (default, customizable)
- **⏸️ Pause/Resume Toggle**: Press F9 to pause, F9 again to resume (default, customizable)
- **⏸️ Interactive Pause Prompts**: Pause at intervals to ask "Continue to iterate?" 
- **TURBO++ Speed**: Maximum possible clicking speed with all safety delays disabled
- **Flexible Coordinates**: Click at specific X,Y coordinates or use current mouse position
- **Real-time Progress**: Live updates showing clicks per second and estimated completion time
- **Safety Features**: Built-in failsafe and confirmation prompts
- **Customizable Delays**: Optional delays between clicks for testing or specific applications

## Quick Start

### Basic Usage (Interactive coordinate selection)
```powershell
# Click 1 million times at current mouse position
uv run --with pyautogui --with keyboard turbo_clicker.py

# Click for 30 seconds at current mouse position
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=30

# Click 100,000 times at current mouse position with progress updates
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --verbose
```

### Time-Based Clicking (NEW!)
```powershell
# Click for 60 seconds at coordinates (400, 300)
uv run --with pyautogui --with keyboard turbo_clicker.py --x=400 --y=300 --duration=60

# Click for 2 minutes at maximum speed
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=120 --turbo-mode --verbose
```

### Interactive Pause Control (NEW!)
```powershell
# Pause every 1000 clicks to ask "Continue to iterate?"
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --pause-interval=1000

# Pause every 30 seconds during time-based clicking
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=300 --pause-interval=30

# Pause every 500 clicks with verbose output
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=5000 --pause-interval=500 --verbose
```

### Specific Coordinates
```powershell
# Click 500,000 times at coordinates (400, 300)
uv run --with pyautogui --with keyboard turbo_clicker.py --x=400 --y=300 --clicks=500000

# Maximum speed clicking at specific location
uv run --with pyautogui --with keyboard turbo_clicker.py --x=500 --y=400 --clicks=1000000 --turbo-mode
```

### Emergency Stop Features
```powershell
# Default hotkeys: F12=emergency stop, F9=pause/resume toggle
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --verbose

# Custom hotkeys: F1=emergency stop, F2=pause/resume
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=120 --emergency-hotkey=f1 --pause-hotkey=f2

# Multiple stop methods available:
# 1. F12 emergency stop (customizable)
# 2. F9 pause/resume toggle (customizable)
# 3. Mouse corner failsafe
# 4. Ctrl+C interrupt
```

### Testing and Development
```powershell
# Test with small number of clicks and full progress output
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100 --verbose --confirm

# Ultra-fast test with minimal delay
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000 --turbo-mode --delay=0.001 --verbose

# Test time-based clicking for 5 seconds
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=5 --verbose --confirm
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--clicks, -c` | Number of clicks to perform | 1,000,000 (if no duration) |
| `--duration, -t` | Duration in seconds to click | None (conflicts with clicks) |
| `--x` | X coordinate to click | Current mouse position |
| `--y` | Y coordinate to click | Current mouse position |
| `--delay, -d` | Delay between clicks (seconds) | 0.0 |
| `--turbo-mode, --turbo` | Enable maximum speed mode | Off |
| `--verbose, -v` | Show progress updates | Off |
| `--confirm` | Skip confirmation prompt | Off |
| `--failsafe` | Enable mouse corner abort | On |
| `--emergency-hotkey` | Emergency stop hotkey | f12 |
| `--pause-hotkey` | Pause/Resume toggle hotkey | f9 |
| `--pause-interval` | Pause every N clicks/seconds to ask "Continue?" | 0 (disabled) |

## 🚨 Emergency Stop Methods

The script provides multiple ways to stop clicking immediately:

### 1. Emergency Stop Hotkey (BEST)
- **Default**: `F12` (customizable)
- **Instant stop** - Fastest response time
- **Global hotkey** - Works even when terminal not focused
- **Examples**:
  ```powershell
  # Use F1 as emergency stop
  uv run --with pyautogui --with keyboard turbo_clicker.py --emergency-hotkey=f1
  
  # Use Ctrl+Q as emergency stop
  uv run --with pyautogui --with keyboard turbo_clicker.py --emergency-hotkey="ctrl+q"
  ```

### 2. Pause/Resume Toggle (NEW!)
- **Default**: `F9` (customizable)
- **Press once to pause**, press again to resume
- **Global hotkey** - Works even when terminal not focused
- **Perfect for**: Taking breaks, adjusting settings, checking results
- **Examples**:
  ```powershell
  # Use F2 as pause/resume toggle
  uv run --with pyautogui --with keyboard turbo_clicker.py --pause-hotkey=f2
  
  # Use Space as pause/resume toggle
  uv run --with pyautogui --with keyboard turbo_clicker.py --pause-hotkey=space
  ```

### 3. Mouse Corner FailSafe
- Move mouse to **top-left corner** of screen
- Built into PyAutoGUI
- Always enabled by default

### 4. Keyboard Interrupt
- Press **Ctrl+C** in terminal
- Requires terminal to be focused
- Shows completion statistics

### 5. Interactive Pause Prompts
- **Configurable intervals**: Pause every N clicks or N seconds
- **User choice**: "Continue to iterate?" prompt
- **Flexible control**: Continue or stop at any pause point
- **Examples**:
  ```powershell
  # Pause every 1000 clicks
  uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --pause-interval=1000
  
  # Pause every 60 seconds during time-based clicking  
  uv run --with pyautogui --with keyboard turbo_clicker.py --duration=600 --pause-interval=60
  ```

## Performance Modes

### Maximum Speed (TURBO++ Mode)
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --turbo-mode --clicks=1000000
```
- Disables ALL PyAutoGUI safety delays
- Achieves 500-1000+ clicks per second (hardware dependent)
- Use for maximum performance scenarios

### Time-Based Mode (NEW!)
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=60 --turbo-mode
```
- Click continuously for specified seconds
- No click count limit
- Perfect for time-sensitive scenarios
- Shows real-time progress with time remaining

### Controlled Speed
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --delay=0.01 --clicks=100000
```
- Add specific delays between clicks
- Useful for applications that need time to process clicks
- More predictable timing

### Test Mode
```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10 --verbose --confirm
```
- Small number of clicks for testing
- Verbose output for debugging
- Confirmation prompt for safety

## Usage Scenarios

### Gaming Applications
```powershell
# Ultra-fast clicking for idle games or clickers (count-based)
uv run --with pyautogui --with keyboard turbo_clicker.py --x=640 --y=360 --clicks=1000000 --turbo-mode --confirm

# Time-based clicking for gaming sessions
uv run --with pyautogui --with keyboard turbo_clicker.py --x=640 --y=360 --duration=300 --turbo-mode --emergency-hotkey=f9

# Measured clicking for games with rate limits
uv run --with pyautogui --with keyboard turbo_clicker.py --x=500 --y=300 --clicks=50000 --delay=0.1 --verbose
```

### Stress Testing
```powershell
# Test application responsiveness for 2 minutes
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=120 --turbo-mode --verbose

# Measured stress testing
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --delay=0.05 --verbose
```

### Automation Tasks
```powershell
# Repetitive UI interaction for specific time
uv run --with pyautogui --with keyboard turbo_clicker.py --x=800 --y=600 --duration=60 --delay=0.5

# Batch processing with clicks
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000 --delay=1.0 --verbose
```

## Interactive Mode

When you don't specify coordinates, the script enters interactive mode:

```powershell
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --verbose
```

1. Script prompts: "Move your mouse to the desired position and press Enter..."
2. Position your mouse where you want to click
3. Press Enter
4. Script shows: "Will click at current mouse position: (X, Y)"
5. Confirmation prompt appears (unless `--confirm` is used)
6. Hotkeys are activated: "🔥 Emergency stop hotkey: F12" and "⏸️ Pause/Resume toggle: F9"
7. Clicking begins

## Safety Features

### FailSafe Protection
- Move mouse to top-left corner to immediately abort
- Enabled by default, disable with `--failsafe=false`

### Confirmation Prompts
- Shows click count, coordinates, and settings before starting
- Skip with `--confirm` flag for automated usage

### Keyboard Interrupt
- Press Ctrl+C to stop clicking at any time
- Shows statistics for clicks performed before interruption

### Hotkey Controls
- **F12**: Emergency stop (instant shutdown)
- **F9**: Pause/resume toggle (preserves progress)
- Both hotkeys work globally (even when terminal not focused)

## Safety Features

### Emergency Hotkey Protection (NEW!)
- **Instant Stop**: Press customizable hotkey to immediately abort
- **Global Hotkey**: Works even when terminal window not focused
- **Default**: Ctrl+Shift+Q (customize with `--emergency-hotkey`)
- **Visual Feedback**: Shows when emergency hotkey is armed

### FailSafe Protection
- Move mouse to top-left corner to immediately abort
- Enabled by default, disable with `--failsafe=false`

### Confirmation Prompts
- Shows click count/duration, coordinates, and settings before starting
- Shows emergency hotkey information
- Skip with `--confirm` flag for automated usage

### Keyboard Interrupt
- Press Ctrl+C to stop clicking at any time
- Shows statistics for clicks performed before interruption

## Performance Benchmarks

Typical performance on modern hardware:

| Mode | Clicks/Second | Use Case |
|------|---------------|----------|
| Normal | 100-300 | General automation |
| Turbo Mode | 500-1000+ | Maximum speed scenarios |
| With Delay (0.01s) | 100 | Controlled rate |
| With Delay (0.1s) | 10 | Slow/careful clicking |

## Advanced Examples

### Million Click Challenge
```powershell
# The full million clicks at maximum speed
uv run --with pyautogui turbo_clicker.py --clicks=1000000 --turbo-mode --verbose --confirm
```

### Coordinate Precision Testing
```powershell
# Test clicking precision at specific pixels
uv run --with pyautogui turbo_clicker.py --x=1920 --y=1080 --clicks=1000 --verbose
```

### Rate-Limited Application Testing
```powershell
# Test applications with click rate limits
uv run --with pyautogui turbo_clicker.py --clicks=10000 --delay=0.1 --verbose
```

### Background Automation
```powershell
# Automated clicking without confirmation prompts
uv run --with pyautogui --with keyboard turbo_clicker.py --x=640 --y=480 --clicks=50000 --confirm --turbo-mode
```

## Performance Benchmarks

Typical performance on modern hardware:

| Mode | Clicks/Second | Use Case |
|------|---------------|----------|
| Normal | 100-300 | General automation |
| Turbo Mode | 500-1000+ | Maximum speed scenarios |
| With Delay (0.01s) | 100 | Controlled rate |
| With Delay (0.1s) | 10 | Slow/careful clicking |

## Advanced Examples

### Million Click Challenge
```powershell
# The full million clicks at maximum speed
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000000 --turbo-mode --verbose --confirm
```

### Coordinate Precision Testing
```powershell
# Test clicking precision at specific pixels
uv run --with pyautogui --with keyboard turbo_clicker.py --x=1920 --y=1080 --clicks=1000 --verbose
```

### Rate-Limited Application Testing
```powershell
# Test applications with click rate limits
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --delay=0.1 --verbose
```

### Hotkey Control Examples
```powershell
# Custom emergency stop and pause keys
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=300 --emergency-hotkey=f1 --pause-hotkey=f2

# Use space bar for pause/resume
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=50000 --pause-hotkey=space

# Complex key combinations
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=120 --emergency-hotkey="ctrl+q" --pause-hotkey="ctrl+p"
```

## Troubleshooting

### Common Issues

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
- Check if antivirus is scanning the script

**Coordinates not working**
- Verify X,Y coordinates are correct for your screen resolution
- Use interactive mode to capture exact coordinates
- Check if target application moved or resized
- Consider multi-monitor setups (coordinates might be on different screen)

**Hotkeys not working**
- Ensure keyboard module is loaded (`--with keyboard`)
- Try running PowerShell as Administrator
- Check if other applications are using the same hotkeys
- Verify key names (f1, f2, space, ctrl+q, etc.)

### Performance Tips

1. **Use Turbo Mode**: `--turbo-mode` for maximum clicking speed
2. **Minimize Delays**: Set `--delay=0.0` or omit for fastest operation
3. **Skip Confirmations**: Use `--confirm` for automated operation
4. **Monitor Progress**: Use `--verbose` to see real-time performance
5. **Close Background Apps**: Free up system resources for maximum speed
6. **Use Specific Coordinates**: Faster than interactive coordinate capture
7. **Run as Administrator**: May improve hotkey responsiveness

## Compatibility

- **Operating System**: Windows 10/11 (PowerShell 5.1+)
- **Python**: 3.8+ (automatically managed by UV)
- **Dependencies**: PyAutoGUI, keyboard (automatically managed by UV)
- **Hardware**: Any modern CPU, benefits from faster processors
- **Memory**: ~50MB RAM for basic operation
- **Network**: Internet required for initial UV setup and dependency download

## System Requirements

### Minimum Requirements
- Windows 10 or later
- 4GB RAM
- 100MB free disk space
- Active desktop session (not headless)

### Recommended Requirements  
- Windows 11
- 8GB+ RAM
- SSD storage for faster startup
- Dedicated graphics card (for better GUI performance)
- Multiple monitors supported

### Dependencies Automatically Installed
```powershell
# These are installed automatically when you run:
uv run --with pyautogui --with keyboard turbo_clicker.py

# PyAutoGUI dependencies include:
# - pillow (screenshot/image recognition)
# - pygetwindow (window management)  
# - pymsgbox (message boxes)
# - pytweening (smooth movement)
# - pyscreeze (screen capture)

# keyboard dependencies include:
# - global hotkey support
# - low-level keyboard hooks
```

## Safety and Ethics

This tool is designed for:
- Personal automation tasks
- Software testing and QA
- Game automation (where permitted)
- Educational purposes

Please ensure compliance with:
- Terms of service of target applications
- Local laws and regulations
- Ethical automation practices

---

**Ready to click a million times? Get started with:**
```powershell
# 1. Install UV (if not already installed)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Run turbo clicker with help
uv run --with pyautogui --with keyboard turbo_clicker.py --help

# 3. Start clicking!
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000 --verbose
```

## Quick Reference

### Essential Commands
```powershell
# Interactive coordinate selection
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=10000 --verbose

# Specific coordinates  
uv run --with pyautogui --with keyboard turbo_clicker.py --x=500 --y=400 --clicks=100000

# Time-based clicking
uv run --with pyautogui --with keyboard turbo_clicker.py --duration=60 --turbo-mode

# Maximum speed test
uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000000 --turbo-mode --confirm
```

### Default Hotkeys
- **F12**: Emergency stop (instant shutdown)
- **F9**: Pause/resume toggle  
- **Mouse to top-left corner**: PyAutoGUI failsafe
- **Ctrl+C**: Keyboard interrupt

### Command Structure
```
uv run --with pyautogui --with keyboard turbo_clicker.py [OPTIONS]
```

**Required**: `--with pyautogui --with keyboard` (installs dependencies)
**Choose one**: `--clicks=N` OR `--duration=N`
**Optional**: All other flags for customization