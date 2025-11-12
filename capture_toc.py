"""
TOC Batch Capture - Capture Table of Contents pages iii through xiv
Specialized version for your specific TOC range
"""
from direct_adb_capture import DirectADBCapture
import time

def capture_toc_pages():
    """Capture TOC pages iii through xiv (12 pages)"""
    capture = DirectADBCapture()
    
    print("📖 TOC Batch Capture")
    print("=" * 50)
    print("Will capture 12 pages: iii, iv, v, vi, vii, viii, ix, x, xi, xii, xiii, xiv")
    print(f"Output folder: {capture.output_folder.absolute()}")
    
    # Roman numeral page names for filenames
    page_names = ['iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv']
    total_pages = len(page_names)
    delay = 2.5  # seconds between pages
    
    print(f"Page turn delay: {delay} seconds")
    
    input(f"\n⚠️ Make sure Kindle is currently showing page 'iii' (Brief Contents).\nPress Enter when ready to capture {total_pages} pages...")
    
    success_count = 0
    failed_pages = []
    
    for i, page_name in enumerate(page_names):
        print(f"\n[{i+1}/{total_pages}] Capturing page '{page_name}'")
        
        filename = f"toc_page_{page_name}.png"
        
        if capture.take_screenshot(filename):
            success_count += 1
            print(f"  ✅ Saved as: {filename}")
        else:
            failed_pages.append(page_name)
            print(f"  ❌ Failed to capture page '{page_name}'")
        
        # Turn page (except for last one)
        if i < total_pages - 1:
            next_page = page_names[i + 1]
            print(f"  📄 Turning to page '{next_page}'...")
            
            if capture.turn_page():
                print(f"  ⏱️ Waiting {delay}s for page '{next_page}' to load...")
                time.sleep(delay)
            else:
                print(f"  ⚠️ Page turn failed from '{page_name}' to '{next_page}'")
                choice = input("Continue anyway? (y/N): ")
                if choice.lower() != 'y':
                    break
    
    # Results summary
    print("\n" + "=" * 60)
    print("📊 TOC CAPTURE RESULTS")
    print("=" * 60)
    print(f"Pages attempted: {total_pages}")
    print(f"Successfully captured: {success_count}")
    print(f"Failed: {len(failed_pages)}")
    
    if failed_pages:
        print(f"Failed pages: {', '.join(failed_pages)}")
    
    print(f"\nOutput location: {capture.output_folder.absolute()}")
    
    if success_count > 0:
        print(f"\n🎉 SUCCESS! {success_count} TOC pages captured at full 1440x3120 resolution!")
        print("   Ready for OCR processing.")
    
    return success_count, failed_pages

if __name__ == "__main__":
    capture_toc_pages()