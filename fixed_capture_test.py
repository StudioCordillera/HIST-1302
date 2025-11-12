"""
Fixed Window Capture - Captures ONLY client area content
"""
import time
import win32gui
import win32con
import win32ui
from PIL import Image
from pathlib import Path

def find_window():
    """Find scrcpy/Phone Mirror window"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if any(kw in title.lower() for kw in ['scrcpy', 'phone mirror', 'android']):
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    if windows:
        return windows[0]
    return None, None

def capture_client_area(hwnd, path):
    """Capture ONLY the client area (content without borders/titlebar)"""
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    # Get CLIENT area dimensions (content only, no borders/titlebar)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top
    
    print(f"  Client area size: {width}x{height}")
    
    # Get the DC of the CLIENT area
    hwnd_dc = win32gui.GetDC(hwnd)  # Use GetDC instead of GetWindowDC for client area
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)
    
    # BitBlt from client area
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    
    # Save to file
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)
    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    img.save(path, 'PNG')
    
    # Cleanup
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

def swipe_page():
    """Swipe to next page via ADB"""
    import subprocess
    adb = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
    subprocess.run([adb, "shell", "input", "swipe", "800", "500", "200", "500", "200"], capture_output=True)

# Main test
print("="*60)
print(" Fixed Window Capture Test - Client Area Only")
print("="*60)

hwnd, title = find_window()
if not hwnd:
    print("\n[FAIL] No scrcpy/Phone Mirror window found!")
    input("Press Enter to exit...")
    exit()

print(f"\n[OK] Found: {title}")

# Show window dimensions
window_rect = win32gui.GetWindowRect(hwnd)
client_rect = win32gui.GetClientRect(hwnd)
print(f"\nWindow rect: {window_rect[2]-window_rect[0]}x{window_rect[3]-window_rect[1]} (includes borders)")
print(f"Client rect: {client_rect[2]-client_rect[0]}x{client_rect[3]-client_rect[1]} (content only)")

print("\nMake sure Kindle is on page iii (Brief Contents)")
input("Press Enter when ready...")

out = Path("test_captures")
out.mkdir(exist_ok=True)

print("\n[1/2] Capturing page iii (client area only)...")
capture_client_area(hwnd, out / "fixed_page_iii.png")
print("  [OK] Saved")

print("[1/2] Turning page...")
swipe_page()
time.sleep(2.5)

print("[2/2] Capturing page iv (client area only)...")
capture_client_area(hwnd, out / "fixed_page_iv.png")
print("  [OK] Saved")

print("\n" + "="*60)
print(f" Test complete! Check: {out.absolute()}")
print("="*60)
print("\nCompare these with the previous captures.")
print("These should show FULL CONTENT with NO black borders!")

input("\nPress Enter to exit...")
