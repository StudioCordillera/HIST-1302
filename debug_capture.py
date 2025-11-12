"""
Debug capture - show window details and capture analysis
"""
import win32gui
import win32con
import win32ui
from PIL import Image
import numpy as np

def analyze_window_and_capture():
    # Find the scrcpy window
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'kindle' in title.lower() or 'scrcpy' in title.lower():
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if not windows:
        print("❌ No scrcpy/Kindle window found!")
        return
    
    hwnd, title = windows[0]
    print(f"✓ Found window: {title}")
    print(f"  Handle: {hwnd}")
    
    # Get window dimensions
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    
    print(f"\n📏 Window Dimensions:")
    print(f"  Window Rect: {window_rect} (left, top, right, bottom)")
    print(f"  Window Size: {window_rect[2] - window_rect[0]} x {window_rect[3] - window_rect[1]}")
    print(f"  Client Rect: {client_rect} (left, top, right, bottom)")
    print(f"  Client Size: {client_rect[2] - client_rect[0]} x {client_rect[3] - client_rect[1]}")
    
    # Check if window is visible and foreground
    is_visible = win32gui.IsWindowVisible(hwnd)
    is_minimized = win32gui.IsIconic(hwnd)
    fg_window = win32gui.GetForegroundWindow()
    
    print(f"\n🔍 Window Status:")
    print(f"  Visible: {is_visible}")
    print(f"  Minimized: {is_minimized}")
    print(f"  Is foreground: {hwnd == fg_window}")
    print(f"  Foreground window: {win32gui.GetWindowText(fg_window) if fg_window else 'None'}")
    
    # Capture using client area method
    print(f"\n📸 Capturing client area...")
    try:
        # Bring to foreground
        win32gui.SetForegroundWindow(hwnd)
        import time
        time.sleep(0.5)
        
        # Get client area dimensions
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top
        
        print(f"  Client area to capture: {width} x {height}")
        
        # Capture
        hwnd_dc = win32gui.GetDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)
        
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
        
        # Convert to PIL Image
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        
        print(f"  Bitmap info: {bmpinfo}")
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        print(f"  PIL Image size: {img.size}")
        
        # Analyze the image
        img_array = np.array(img)
        print(f"  Image array shape: {img_array.shape}")
        print(f"  Image mean brightness: {img_array.mean():.2f}")
        print(f"  Image min brightness: {img_array.min()}")
        print(f"  Image max brightness: {img_array.max()}")
        
        # Check for black bars
        row_brightness = img_array.mean(axis=(1, 2))
        col_brightness = img_array.mean(axis=(0, 2))
        
        dark_rows = (row_brightness < 10).sum()
        dark_cols = (col_brightness < 10).sum()
        
        print(f"  Dark rows (< 10 brightness): {dark_rows} / {len(row_brightness)}")
        print(f"  Dark columns (< 10 brightness): {dark_cols} / {len(col_brightness)}")
        
        # Save debug image
        debug_path = "debug_capture.png"
        img.save(debug_path, 'PNG')
        print(f"\n✓ Debug capture saved: {debug_path}")
        print(f"  File size: {len(open(debug_path, 'rb').read())} bytes")
        
        # Cleanup
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        
    except Exception as e:
        print(f"❌ Capture failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Debug Window Capture Analysis")
    print("=" * 50)
    analyze_window_and_capture()