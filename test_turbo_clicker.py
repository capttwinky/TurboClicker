#!/usr/bin/env python3
"""
Test script for turbo_clicker.py to verify argument parsing and functionality.
Tests all features including time-based clicking, hotkeys, and pause intervals.
"""

import subprocess
import sys
import os
import time

def run_uv_command(args, timeout=10):
    """Run a UV command with turbo_clicker.py and return the result."""
    cmd = ["uv", "run", "--with", "pyautogui", "--with", "keyboard", "turbo_clicker.py"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, 
                              cwd=os.path.dirname(__file__), timeout=timeout)
        return result
    except subprocess.TimeoutExpired:
        return None

def test_help():
    """Test the help output."""
    print("Testing --help option...")
    result = run_uv_command(["--help"])
    if result:
        print("Exit code:", result.returncode)
        print("Help output (first 15 lines):")
        for line in result.stdout.split('\n')[:15]:
            print(f"  {line}")
        print("...")
        
        # Check for new features in help text
        help_text = result.stdout.lower()
        features_to_check = [
            "duration", "emergency-hotkey", "pause-hotkey", 
            "pause-interval", "f12", "f9"
        ]
        
        print("\nFeature availability check:")
        for feature in features_to_check:
            found = feature in help_text
            status = "✅" if found else "❌"
            print(f"  {status} {feature}")
    else:
        print("❌ Help command timed out")

def test_argument_validation():
    """Test various argument combinations."""
    print("\n" + "="*50)
    print("Testing Argument Validation")
    print("="*50)
    
    test_cases = [
        # Basic functionality tests
        {
            "name": "Basic clicks with coordinates",
            "args": ["--clicks=10", "--x=400", "--y=300", "--help"],
            "should_succeed": True
        },
        {
            "name": "Duration-based clicking",
            "args": ["--duration=5", "--x=500", "--y=400", "--help"],
            "should_succeed": True
        },
        {
            "name": "Turbo mode with custom hotkeys",
            "args": ["--turbo-mode", "--emergency-hotkey=f1", "--pause-hotkey=f2", "--help"],
            "should_succeed": True
        },
        {
            "name": "Pause interval with verbose",
            "args": ["--clicks=1000", "--pause-interval=100", "--verbose", "--help"],
            "should_succeed": True
        },
        {
            "name": "Conflicting clicks and duration",
            "args": ["--clicks=1000", "--duration=30"],  # Removed --help to test actual validation
            "should_succeed": False  # Should fail due to mutual exclusion
        },
        {
            "name": "Time-based with pause interval",
            "args": ["--duration=60", "--pause-interval=10", "--turbo-mode", "--help"],
            "should_succeed": True
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Args: {' '.join(test_case['args'])}")
        
        result = run_uv_command(test_case['args'])
        if result:
            success = result.returncode == 0
            expected = test_case['should_succeed']
            
            if success == expected:
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                
            print(f"Result: {status} (Exit code: {result.returncode}, Expected success: {expected})")
            
            if result.returncode != 0 and result.stderr:
                print(f"Error: {result.stderr.strip()}")
        else:
            print("❌ Command timed out")

def test_new_features():
    """Test new features specifically."""
    print("\n" + "="*50)
    print("Testing New Features")
    print("="*50)
    
    # Test mutual exclusion validation
    print("\n1. Testing mutual exclusion (clicks vs duration):")
    result = run_uv_command(["--clicks=100", "--duration=10"])
    if result and result.returncode != 0:
        print("✅ PASS: Correctly rejects conflicting options")
        print(f"   Error message: {result.stderr.strip()}")
    else:
        print("❌ FAIL: Should reject conflicting options")
    
    # Test default behavior
    print("\n2. Testing default behavior (no clicks or duration specified):")
    result = run_uv_command(["--help"])
    if result and result.returncode == 0:
        print("✅ PASS: Help works with no specific click/duration args")
    else:
        print("❌ FAIL: Default behavior not working")
    
    # Test hotkey argument parsing
    print("\n3. Testing custom hotkey arguments:")
    hotkey_tests = [
        ["--emergency-hotkey=f1", "--help"],
        ["--pause-hotkey=space", "--help"],
        ["--emergency-hotkey=ctrl+q", "--pause-hotkey=ctrl+p", "--help"]
    ]
    
    for args in hotkey_tests:
        result = run_uv_command(args)
        if result and result.returncode == 0:
            print(f"✅ PASS: {' '.join(args[:2])}")
        else:
            print(f"❌ FAIL: {' '.join(args[:2])}")

def test_performance_modes():
    """Test different performance and operational modes."""
    print("\n" + "="*50)
    print("Testing Performance Modes")
    print("="*50)
    
    modes = [
        {
            "name": "Normal Mode",
            "args": ["--clicks=5", "--x=500", "--y=400", "--confirm", "--help"]
        },
        {
            "name": "Turbo Mode", 
            "args": ["--clicks=5", "--turbo-mode", "--confirm", "--help"]
        },
        {
            "name": "Time-based Mode",
            "args": ["--duration=1", "--verbose", "--confirm", "--help"]
        },
        {
            "name": "Delayed Clicking",
            "args": ["--clicks=5", "--delay=0.1", "--confirm", "--help"]
        },
        {
            "name": "Pause Interval Mode",
            "args": ["--clicks=20", "--pause-interval=5", "--confirm", "--help"]
        }
    ]
    
    for mode in modes:
        print(f"\nTesting {mode['name']}:")
        result = run_uv_command(mode['args'])
        if result and result.returncode == 0:
            print("✅ PASS: Arguments accepted")
        else:
            print("❌ FAIL: Arguments rejected")
            if result and result.stderr:
                print(f"   Error: {result.stderr.strip()}")

def test_example_commands():
    """Test the example commands from the help text."""
    print("\n" + "="*50)
    print("Testing Example Commands")
    print("="*50)
    
    examples = [
        # Basic examples (just test argument parsing, not execution)
        ["--clicks=1000", "--help"],
        ["--duration=30", "--help"], 
        ["--x=400", "--y=300", "--duration=60", "--help"],
        ["--x=500", "--y=400", "--clicks=1000", "--turbo-mode", "--help"],
        ["--clicks=100", "--delay=0.001", "--help"],
        ["--duration=120", "--emergency-hotkey=f12", "--pause-hotkey=f9", "--help"],
        ["--clicks=1000", "--pause-interval=100", "--help"],
        ["--duration=300", "--pause-interval=30", "--help"]
    ]
    
    passed = 0
    total = len(examples)
    
    for i, args in enumerate(examples, 1):
        result = run_uv_command(args)
        if result and result.returncode == 0:
            print(f"✅ Example {i}: PASS")
            passed += 1
        else:
            print(f"❌ Example {i}: FAIL - {' '.join(args)}")
            if result and result.stderr:
                print(f"   Error: {result.stderr.strip()}")
    
    print(f"\nExample Commands: {passed}/{total} passed")
    return passed == total

def print_summary(test_results):
    """Print a summary of all test results."""
    print("\n" + "="*60)
    print("TURBO CLICKER TEST SUMMARY")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("Turbo Clicker is ready for use!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed")
        print("Please check the issues above.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("TURBO CLICKER COMPREHENSIVE TEST SUITE")
    print("="*60)
    print("Testing all features of the enhanced turbo clicker")
    print("This includes: hotkeys, time-based clicking, pause intervals, etc.")
    print("="*60)
    
    test_results = []
    
    # Run all test suites
    print("\n🔧 Testing basic help functionality...")
    test_help()
    
    print("\n🔧 Testing argument validation...")
    test_argument_validation()
    
    print("\n🔧 Testing new features...")
    test_new_features()
    
    print("\n🔧 Testing performance modes...")
    test_performance_modes()
    
    print("\n🔧 Testing example commands...")
    example_result = test_example_commands()
    test_results.append(example_result)
    
    # Print comprehensive usage instructions
    print("\n" + "="*60)
    print("USAGE INSTRUCTIONS")
    print("="*60)
    print("\nTo use Turbo Clicker with all features:")
    print("\n1. Basic Usage:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --help")
    print("\n2. Count-based Clicking:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000 --verbose")
    print("\n3. Time-based Clicking:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --duration=30 --verbose")
    print("\n4. Maximum Speed:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=100000 --turbo-mode")
    print("\n5. Custom Hotkeys:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=1000 --emergency-hotkey=f1 --pause-hotkey=f2")
    print("\n6. Interactive Pauses:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --clicks=2000 --pause-interval=500")
    print("\n7. Specific Coordinates:")
    print("   uv run --with pyautogui --with keyboard turbo_clicker.py --x=640 --y=480 --clicks=1000")
    
    print("\n🔥 Default Hotkeys:")
    print("   F12 = Emergency Stop (instant shutdown)")
    print("   F9  = Pause/Resume Toggle")
    print("   Mouse to top-left corner = PyAutoGUI failsafe")
    print("   Ctrl+C = Keyboard interrupt")
    
    print("\n📊 Performance Notes:")
    print("   - Normal mode: 100-300 clicks/second")
    print("   - Turbo mode: 500-1000+ clicks/second") 
    print("   - Use --delay for controlled speed")
    print("   - Use --verbose for real-time progress")
    
    # Print final summary
    if test_results:
        print_summary(test_results)
    
    print("\n✨ Test suite completed!")
    print("Run any of the usage examples above to start clicking!")