"""
Fixed Full Screen Capture - Capture entire desktop and crop to scrcpy area
This approach captures the full desktop then crops to the scrcpy window area
"""
import win32gui
import win32con
import win32ui
import win32api
from PIL import Image
import numpy as np

def capture_full_desktop():
    """Capture the entire desktop"""
    # Get desktop window
    desktop = win32gui.GetDesktopWindow()
    
    # Get desktop dimensions
    desktop_dc = win32gui.GetWindowDC(desktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()
    
    # Get screen resolution
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    print(f"Desktop resolution: {screen_width} x {screen_height}")
    
    # Create bitmap
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, screen_width, screen_height)
    mem_dc.SelectObject(screenshot)
    
    # Copy desktop to bitmap
    mem_dc.BitBlt((0, 0), (screen_width, screen_height), img_dc, (0, 0), win32con.SRCCOPY)
    
    # Convert to PIL Image
    bmpinfo = screenshot.GetInfo()
    bmpstr = screenshot.GetBitmapBits(True)
    
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )
    
    # Cleanup
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(desktop, desktop_dc)
    win32gui.DeleteObject(screenshot.GetHandle())
    
    return img

def find_scrcpy_window_rect():
    """Find scrcpy window and get its screen coordinates"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if any(keyword in title.lower() for keyword in ['kindle', 'scrcpy']):
                rect = win32gui.GetWindowRect(hwnd)
                windows.append((hwnd, title, rect))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        hwnd, title, rect = windows[0]
        print(f"Found scrcpy window: {title}")
        print(f"Window position: {rect}")
        return rect
    
    return None

def full_screen_capture_test():
    """Test capturing full desktop and cropping to scrcpy window"""
    print("🖥️ Full Desktop Capture Test")
    print("=" * 50)
    
    # Find scrcpy window
    window_rect = find_scrcpy_window_rect()
    if not window_rect:
        print("❌ No scrcpy window found!")
        return
    
    # Capture full desktop
    print("\n📸 Capturing full desktop...")
    full_image = capture_full_desktop()
    
    # Save full desktop (for debugging)
    full_image.save("full_desktop.png")
    print(f"Full desktop saved: full_desktop.png ({full_image.size})")
    
    # Crop to scrcpy window area
    left, top, right, bottom = window_rect
    print(f"\n✂️ Cropping to scrcpy window area: ({left}, {top}, {right}, {bottom})")
    
    cropped_image = full_image.crop((left, top, right, bottom))
    
    # Save cropped image
    cropped_image.save("cropped_scrcpy.png")
    print(f"Cropped scrcpy area saved: cropped_scrcpy.png ({cropped_image.size})")
    
    # Analyze the cropped image
    img_array = np.array(cropped_image)
    print(f"\n📊 Image analysis:")
    print(f"  Size: {cropped_image.size}")
    print(f"  Array shape: {img_array.shape}")
    print(f"  Mean brightness: {img_array.mean():.2f}")
    print(f"  File size: {len(open('cropped_scrcpy.png', 'rb').read())} bytes")
    
    return cropped_image

if __name__ == "__main__":
    full_screen_capture_test()