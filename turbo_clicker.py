#!/usr/bin/env python3
"""
Turbo Clicker: Ultra-high speed clicking automation
Clicks up to 1 million times at maximum possible speeds on specified coordinates.
Features emergency hotkey kill switch and time-based clicking duration.
"""

import argparse
import time
import sys
import threading
from typing import Tuple, Optional
import pyautogui as pg # pyright: ignore[reportMissingModuleSource]
try:
    import keyboard # pyright: ignore[reportMissingModuleSource]
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# Global variables for emergency stop and pause control
emergency_stop = False
emergency_stop_reason = ""
is_paused = False
pause_reason = ""


def setup_hotkeys(emergency_hotkey: str = "f12", pause_hotkey: str = "f9") -> Optional[threading.Thread]:
    """Setup emergency hotkey and pause/resume toggle in a background thread."""
    global emergency_stop, emergency_stop_reason, is_paused, pause_reason
    
    if not KEYBOARD_AVAILABLE:
        print("Warning: 'keyboard' module not available. Hotkeys disabled.")
        print("Install with: uv add keyboard")
        return None
    
    def emergency_handler():
        global emergency_stop, emergency_stop_reason
        emergency_stop = True
        emergency_stop_reason = f"Emergency hotkey ({emergency_hotkey}) pressed"
        print(f"\n🚨 EMERGENCY STOP ACTIVATED! ({emergency_hotkey})")
    
    def pause_toggle_handler():
        global is_paused, pause_reason
        is_paused = not is_paused
        if is_paused:
            pause_reason = f"Pause hotkey ({pause_hotkey}) pressed"
            print(f"\n⏸️  PAUSED by hotkey ({pause_hotkey}). Press {pause_hotkey} again to resume.")
        else:
            print(f"\n▶️  RESUMED by hotkey ({pause_hotkey}). Continuing...")
    
    try:
        keyboard.add_hotkey(emergency_hotkey, emergency_handler)  # type: ignore
        keyboard.add_hotkey(pause_hotkey, pause_toggle_handler)  # type: ignore
        print(f"🔥 Emergency stop hotkey: {emergency_hotkey.upper()}")
        print(f"⏸️  Pause/Resume toggle: {pause_hotkey.upper()}")
        return None  # keyboard handles this internally
    except Exception as e:
        print(f"Warning: Could not setup hotkeys: {e}")
        return None


def cleanup_hotkeys():
    """Cleanup hotkey listeners."""
    if KEYBOARD_AVAILABLE:
        try:
            keyboard.unhook_all_hotkeys()  # type: ignore
        except Exception:
            pass


def parse_arguments() -> argparse.Namespace:
    """Cleanup emergency hotkey listener."""
    if KEYBOARD_AVAILABLE:
        try:
            keyboard.unhook_all_hotkeys() # type: ignore
        except Exception:
            pass
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Turbo Clicker: Ultra-high speed clicking automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Normal usage examples:

  # Standard run:
  uv run --with pyautogui  --with keyboard turbo_clicker.py --verbose --delay=0.005 --confirm
  
  # Click 1 million times at current mouse position
  uv run --with pyautogui  --with keyboard turbo_clicker.py --clicks=1000000
  
  # Click for 30 seconds at current mouse position
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --duration=30
  
  # Click at specific coordinates for 60 seconds
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --x=400 --y=300 --duration=60

  # Click at specific coordinates
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --x=400 --y=300 --clicks=500000

  # Maximum speed (no delays)
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --x=500 --y=400 --clicks=1000000 --turbo-mode

  # Click with minimal delay between clicks
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --clicks=100000 --delay=0.001
  
  # Custom hotkeys
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --duration=120 --emergency-hotkey="f12" --pause-hotkey="f9"
  
  # Pause every 1000 clicks to ask if user wants to continue
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --clicks=10000 --pause-interval=1000
  
  # Pause every 30 seconds during time-based clicking
  uv run --with pyautogui  --with keyboard  turbo_clicker.py --duration=300 --pause-interval=30
        """)
    
    parser.add_argument('--clicks', '-c', type=int, 
                       help='Number of clicks to perform (conflicts with --duration)')
    parser.add_argument('--duration', '-t', type=float,
                       help='Duration in seconds to click (conflicts with --clicks)')
    parser.add_argument('--x', type=int, help='X coordinate to click (if not provided, uses current mouse position)')
    parser.add_argument('--y', type=int, help='Y coordinate to click (if not provided, uses current mouse position)')
    parser.add_argument('--delay', '-d', type=float, default=0.0,
                       help='Delay between clicks in seconds (default: 0.0 for maximum speed)')
    parser.add_argument('--turbo-mode', '--turbo', action='store_true',
                       help='Enable maximum speed mode (disables all PyAutoGUI safety delays)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output with progress updates')
    parser.add_argument('--confirm', action='store_true',
                       help='Skip confirmation prompt and start immediately')
    parser.add_argument('--failsafe', action='store_true', default=True,
                       help='Enable PyAutoGUI failsafe (move mouse to corner to abort)')
    parser.add_argument('--emergency-hotkey', default='f12',
                       help='Emergency stop hotkey (default: f12)')
    parser.add_argument('--pause-hotkey', default='f9',
                       help='Pause/Resume toggle hotkey (default: f9)')
    parser.add_argument('--pause-interval', type=int, default=0,
                       help='Pause every N clicks/seconds to ask "Continue to iterate?" (0 = no pauses)')
    
    args = parser.parse_args()
    
    # Validate mutually exclusive options
    if args.clicks is not None and args.duration is not None:
        parser.error("--clicks and --duration are mutually exclusive. Use one or the other.")
    
    if args.clicks is None and args.duration is None:
        args.clicks = 1000000  # Default to 1 million clicks
    
    return args


def get_click_coordinates(x: Optional[int], y: Optional[int]) -> Tuple[int, int]:
    """Get the coordinates to click on."""
    if x is not None and y is not None:
        return (x, y)
    
    print("No coordinates specified. Move your mouse to the desired position and press Enter...")
    input()
    current_pos = pg.position()
    print(f"Will click at current mouse position: ({current_pos.x}, {current_pos.y})")
    return (current_pos.x, current_pos.y)


def configure_pyautogui(turbo_mode: bool, failsafe: bool = True) -> None:
    """Configure PyAutoGUI for optimal clicking performance."""
    pg.FAILSAFE = failsafe
    
    if turbo_mode:
        # Maximum speed: disable all built-in delays
        pg.PAUSE = 0.0
        pg.MINIMUM_DURATION = 0.0
        pg.MINIMUM_SLEEP = 0.0
        print("TURBO MODE ENABLED: All safety delays disabled for maximum speed!")
    else:
        # Minimal delays for fast but safer operation
        pg.PAUSE = 0.001


def check_continue_prompt(pause_interval: int, clicks_performed: int, elapsed_time: float, time_based: bool) -> bool:
    """Check if we should pause and ask user to continue."""
    if pause_interval <= 0:
        return True  # No pausing enabled
    
    if time_based:
        # For time-based clicking, pause based on elapsed seconds
        if elapsed_time > 0 and int(elapsed_time) % pause_interval == 0 and int(elapsed_time) > 0:
            return ask_continue(f"after {elapsed_time:.0f} seconds")
    else:
        # For count-based clicking, pause based on click count
        if clicks_performed > 0 and clicks_performed % pause_interval == 0:
            return ask_continue(f"after {clicks_performed:,} clicks")
    
    return True


def ask_continue(context: str) -> bool:
    """Ask user if they want to continue iterating."""
    print(f"\n\n⏸️  PAUSE {context}")
    while True:
        response = input("Continue to iterate? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("Continuing...\n")
            return True
        elif response in ['n', 'no']:
            print("Stopping by user request.")
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def turbo_click(x: int, y: int, clicks: Optional[int] = None, duration: Optional[float] = None, 
                delay: float = 0.0, verbose: bool = False, emergency_hotkey: str = "f12",
                pause_hotkey: str = "f9", pause_interval: int = 0) -> None:
    """Perform ultra-fast clicking at the specified coordinates."""
    global emergency_stop, emergency_stop_reason, is_paused, pause_reason
    
    # Reset emergency stop and pause state
    emergency_stop = False
    emergency_stop_reason = ""
    is_paused = False
    pause_reason = ""
    
    # Setup hotkeys
    setup_hotkeys(emergency_hotkey, pause_hotkey)
    
    # Determine operation mode
    time_based = duration is not None
    if time_based:
        print(f"Starting time-based clicking: {duration} seconds at ({x}, {y})")
        target_end_time = time.perf_counter() + duration
        clicks_performed = 0
        total_target = "∞"
    else:
        print(f"Starting count-based clicking: {clicks:,} clicks at ({x}, {y})")
        clicks_performed = 0
        total_target = clicks
        target_end_time = 0.0  # Not used in count-based mode
        if clicks is None:
            raise ValueError("Either clicks or duration must be specified")
    
    print(f"Delay between clicks: {delay}s")
    print(f"Emergency stop: {emergency_hotkey.upper()}")
    print(f"Pause/Resume toggle: {pause_hotkey.upper()}")
    if pause_interval > 0:
        interval_desc = f"every {pause_interval} seconds" if time_based else f"every {pause_interval:,} clicks"
        print(f"Pause prompts: {interval_desc}")
    
    if verbose:
        print("Starting in 3 seconds... Move mouse to top-left corner to abort if needed.")
        time.sleep(3)
    
    start_time = time.perf_counter()
    last_progress_update = start_time
    last_pause_check = 0  # Track when we last checked for pause
    
    try:
        if time_based:
            # Time-based clicking loop
            while time.perf_counter() < target_end_time:
                if emergency_stop:
                    break
                
                # Check if paused - wait until unpaused
                while is_paused:
                    if emergency_stop:
                        break
                    time.sleep(0.1)  # Small sleep to prevent busy waiting
                
                if emergency_stop:
                    break
                    
                # Perform the click
                pg.click(x, y)
                clicks_performed += 1
                
                # Check for pause prompt
                elapsed = time.perf_counter() - start_time
                if pause_interval > 0 and int(elapsed) > last_pause_check and int(elapsed) % pause_interval == 0:
                    if not check_continue_prompt(pause_interval, clicks_performed, elapsed, time_based):
                        break
                    last_pause_check = int(elapsed)
                
                # Progress updates for verbose mode
                if verbose and time.perf_counter() - last_progress_update >= 1.0:
                    cps = clicks_performed / elapsed if elapsed > 0 else 0
                    remaining_time = target_end_time - time.perf_counter()
                    print(f"\rProgress: {clicks_performed:,} clicks in {elapsed:.1f}s | "
                          f"Speed: {cps:.1f} clicks/sec | Time remaining: {remaining_time:.1f}s", end="", flush=True)
                    last_progress_update = time.perf_counter()
                
                # Optional delay between clicks
                if delay > 0:
                    time.sleep(delay)
        else:
            # Count-based clicking loop  
            assert clicks is not None  # This should never be None here due to validation above
            for i in range(clicks):
                if emergency_stop:
                    break
                
                # Check if paused - wait until unpaused
                while is_paused:
                    if emergency_stop:
                        break
                    time.sleep(0.1)  # Small sleep to prevent busy waiting
                
                if emergency_stop:
                    break
                    
                # Perform the click
                pg.click(x, y)
                clicks_performed += 1
                
                # Check for pause prompt
                if pause_interval > 0 and clicks_performed % pause_interval == 0:
                    elapsed = time.perf_counter() - start_time
                    if not check_continue_prompt(pause_interval, clicks_performed, elapsed, time_based):
                        break
                
                # Progress updates for verbose mode
                if verbose and time.perf_counter() - last_progress_update >= 1.0:
                    elapsed = time.perf_counter() - start_time
                    cps = clicks_performed / elapsed if elapsed > 0 else 0
                    remaining = clicks - clicks_performed
                    eta = remaining / cps if cps > 0 else 0
                    print(f"\rProgress: {clicks_performed:,}/{clicks:,} clicks ({clicks_performed/clicks*100:.1f}%) | "
                          f"Speed: {cps:.1f} clicks/sec | ETA: {eta:.1f}s", end="", flush=True)
                    last_progress_update = time.perf_counter()
                
                # Optional delay between clicks
                if delay > 0:
                    time.sleep(delay)
                    
    except KeyboardInterrupt:
        print(f"\n\nInterrupted by user (Ctrl+C) after {clicks_performed:,} clicks")
    except pg.FailSafeException:
        print(f"\n\nFailSafe triggered after {clicks_performed:,} clicks")
    finally:
        # Cleanup hotkeys
        cleanup_hotkeys()
    
    # Handle emergency stop
    if emergency_stop:
        print(f"\n\n🚨 EMERGENCY STOP: {emergency_stop_reason}")
        print(f"Clicks performed before stop: {clicks_performed:,}")
    
    # Handle pause state at end
    if is_paused:
        print(f"\n\n⏸️  Script ended while paused: {pause_reason}")
        print(f"Clicks performed before pause: {clicks_performed:,}")
    
    # Final statistics
    end_time = time.perf_counter()
    total_time = end_time - start_time
    
    print(f"\n\nClicking completed!")
    print(f"Total clicks performed: {clicks_performed:,}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average speed: {clicks_performed / total_time:.1f} clicks per second")
    
    if time_based:
        if total_time >= duration * 0.95:  # Within 5% of target
            print("✅ Time duration completed successfully!")
        else:
            print(f"⚠️  Stopped early. Ran for {total_time/duration*100:.1f}% of target duration.")
    else:
        assert clicks is not None  # This should never be None here
        if clicks_performed >= clicks:
            print("✅ All clicks completed successfully!")
        else:
            print(f"⚠️  Stopped early. Completed {clicks_performed/clicks*100:.1f}% of target clicks.")


def main() -> None:
    """Main entry point for the turbo clicker."""
    args = parse_arguments()
    
    # Configuration
    configure_pyautogui(args.turbo_mode, args.failsafe)
    
    # Get coordinates
    click_x, click_y = get_click_coordinates(args.x, args.y)
    
    # Confirmation and safety check
    if not args.confirm:
        mode_str = f"{args.duration} seconds" if args.duration else f"{args.clicks:,} clicks"
        print(f"\nReady to perform {mode_str} at ({click_x}, {click_y})")
        print(f"Turbo mode: {'ON' if args.turbo_mode else 'OFF'}")
        print(f"Delay between clicks: {args.delay}s")
        print(f"FailSafe: {'ON' if args.failsafe else 'OFF'}")
        print(f"Emergency stop: {args.emergency_hotkey.upper()}")
        print(f"Pause/Resume toggle: {args.pause_hotkey.upper()}")
        
        response = input("\nDo you want to continue? (y/N): ").lower().strip()
        if response not in ['y', 'yes']:
            print("Aborted by user.")
            sys.exit(0)
    
    # Start the turbo clicking
    turbo_click(click_x, click_y, args.clicks, args.duration, args.delay, args.verbose, 
                args.emergency_hotkey, args.pause_hotkey, args.pause_interval)


if __name__ == "__main__":
    main()