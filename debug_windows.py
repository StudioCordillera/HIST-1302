"""
Debug window finder - show all visible windows
"""
import win32gui

def list_windows():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Only show windows with titles
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    print("All visible windows:")
    print("-" * 60)
    for hwnd, title in sorted(windows, key=lambda x: x[1].lower()):
        print(f"{hwnd}: {title}")
    
    # Look for potential scrcpy windows
    print("\nPotential capture targets:")
    print("-" * 60)
    keywords = ['scrcpy', 'phone', 'android', 'mirror', 'kindle', 'samsung']
    for hwnd, title in windows:
        title_lower = title.lower()
        for keyword in keywords:
            if keyword in title_lower:
                print(f"✓ {hwnd}: {title}")
                break

if __name__ == "__main__":
    list_windows()