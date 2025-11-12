"""
Diagnostic Test for Window Capture - Fixed Version
Tests scrcpy window detection and capture methods
"""

import subprocess
import time
import win32gui
import win32con
import win32ui
from PIL import Image
import os
from pathlib import Path

def list_all_windows():
    """List all visible windows"""
    print("\n=== All Visible Windows ===")
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                rect = win32gui.GetWindowRect(hwnd)
                windows.append((hwnd, title, rect))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    for hwnd, title, rect in windows:
        print(f"HWND: {hwnd} | Title: {title[:50]}")
    
    return windows

def find_scrcpy_window():
    """Find scrcpy window with multiple methods"""
    print("\n=== Finding scrcpy Window ===")
    
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            # Look for common scrcpy window titles
            if any(keyword in title.lower() for keyword in ['scrcpy', 'phone mirror', 'android']):
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        for hwnd, title in windows:
            print(f"[OK] Found: {title} (HWND: {hwnd})")
        return windows[0][0]  # Return first matching window
    else:
        print("[FAIL] No scrcpy window found")
        return None

def get_window_info(hwnd):
    """Get detailed window information"""
    print(f"\n=== Window Info (HWND: {hwnd}) ===")
    
    title = win32gui.GetWindowText(hwnd)
    print(f"Title: {title}")
    
    rect = win32gui.GetWindowRect(hwnd)
    print(f"Position: ({rect[0]}, {rect[1]})")
    print(f"Size: {rect[2] - rect[0]} x {rect[3] - rect[1]}")
    
    is_visible = win32gui.IsWindowVisible(hwnd)
    print(f"Visible: {is_visible}")
    
    is_minimized = win32gui.IsIconic(hwnd)
    print(f"Minimized: {is_minimized}")
    
    return rect

def capture_window_method1(hwnd, output_path):
    """PrintWindow method"""
    print(f"\n=== Testing Method 1: PrintWindow ===")
    try:
        # Make sure window is visible and foreground
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        
        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        
        print(f"Capturing area: {width}x{height}")
        
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)
        
        # PrintWindow with PW_RENDERFULLCONTENT flag
        result = win32gui.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
        print(f"PrintWindow result: {result}")
        
        # Save to file
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        img.save(output_path, 'PNG')
        print(f"[OK] Saved to: {output_path}")
        
        # Cleanup
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def capture_window_method2(hwnd, output_path):
    """Direct BitBlt method"""
    print(f"\n=== Testing Method 2: Direct BitBlt ===")
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        
        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        
        print(f"Capturing area: {width}x{height}")
        
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)
        
        # Direct BitBlt
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
        
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        img.save(output_path, 'PNG')
        print(f"[OK] Saved to: {output_path}")
        
        # Cleanup
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def main():
    print("="*60)
    print(" Kindle Capture - Window Capture Diagnostic")
    print("="*60)
    
    # Create output directory
    output_dir = Path("test_captures")
    output_dir.mkdir(exist_ok=True)
    
    # List all windows
    all_windows = list_all_windows()
    
    # Find existing scrcpy/Phone Mirror window
    hwnd = find_scrcpy_window()
    
    if not hwnd:
        print("\n[FAIL] No scrcpy/Phone Mirror window found!")
        print("Please start scrcpy first, then run this test again.")
        return
    
    # Get window info
    get_window_info(hwnd)
    
    # Test capture methods
    method1_path = output_dir / "test_method1_printwindow.png"
    method2_path = output_dir / "test_method2_bitblt.png"
    
    print("\nWill capture in 2 seconds...")
    time.sleep(2)
    
    success1 = capture_window_method1(hwnd, method1_path)
    time.sleep(1)
    success2 = capture_window_method2(hwnd, method2_path)
    
    # Results
    print("\n" + "="*60)
    print(" Test Results")
    print("="*60)
    status1 = "[OK]" if success1 else "[FAIL]"
    status2 = "[OK]" if success2 else "[FAIL]"
    print(f"Method 1 (PrintWindow): {status1}")
    print(f"Method 2 (BitBlt):      {status2}")
    print(f"\nTest captures saved to: {output_dir.absolute()}")
    print("\nCheck the images to see which method works best!")
    print("If both are black, try:")
    print("  1. Make sure the Phone Mirror window is not minimized")
    print("  2. Make sure Kindle app is visible on your phone")
    print("  3. Run this test again")
    
    print("\n[OK] Test complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[FAIL] Interrupted by user")
    except Exception as e:
        print(f"\n[FAIL] Fatal error: {e}")
        import traceback
        traceback.print_exc()
