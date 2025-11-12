"""
Chapters 21-24 Batch Capture - Pages 515 to 617 (103 pages)
Large batch capture for multiple chapters
"""
from direct_adb_capture import DirectADBCapture
import time
from pathlib import Path

def capture_chapters_21_24():
    """Capture chapters 21-24: pages 515 through 617 (103 pages)"""
    capture = DirectADBCapture()
    
    # Create dedicated subfolder for chapters 21-24
    chapter_folder = capture.output_folder / "CHAPTERS_21-24"
    chapter_folder.mkdir(exist_ok=True)
    
    # Update the capture object to use the chapter folder
    original_folder = capture.output_folder
    capture.output_folder = chapter_folder
    
    print("📚 CHAPTERS 21-24 BATCH CAPTURE")
    print("=" * 60)
    print("Capturing pages 515 through 617")
    print(f"Total pages: 103 pages")
    print(f"Chapters: 21, 22, 23, 24")
    print(f"Output folder: {chapter_folder.absolute()}")
    
    start_page = 515
    end_page = 617
    total_pages = end_page - start_page + 1  # 103 pages
    delay = 2.5  # seconds between pages
    
    print(f"Page turn delay: {delay} seconds")
    print(f"Estimated time: ~{(total_pages * (delay + 1)) / 60:.1f} minutes")
    
    # Safety confirmation for large batch
    print(f"\n⚠️  LARGE BATCH WARNING:")
    print(f"   • This will take approximately {(total_pages * delay) / 60:.0f} minutes")
    print(f"   • Make sure your device stays connected")
    print(f"   • Keep your device plugged in")
    print(f"   • Disable auto-sleep/screen timeout")
    
    input(f"\nMake sure Kindle is currently showing page 515.\nPress Enter when ready to capture {total_pages} pages...")
    
    success_count = 0
    failed_pages = []
    start_time = time.time()
    
    for i in range(total_pages):
        current_page = start_page + i
        elapsed = time.time() - start_time
        estimated_remaining = (elapsed / max(i, 1)) * (total_pages - i - 1) if i > 0 else 0
        
        print(f"\n[{i+1}/{total_pages}] Page {current_page}")
        print(f"  Progress: {(i+1)/total_pages*100:.1f}% | Elapsed: {elapsed/60:.1f}min | Remaining: ~{estimated_remaining/60:.1f}min")
        
        filename = f"page_{current_page:04d}.png"
        
        if capture.take_screenshot(filename):
            success_count += 1
        else:
            failed_pages.append(current_page)
            print(f"  ❌ Failed to capture page {current_page}")
        
        # Turn page (except for last one)
        if i < total_pages - 1:
            next_page = current_page + 1
            
            if capture.turn_page():
                # Show brief progress every 10 pages
                if (i + 1) % 10 == 0:
                    print(f"  ✅ Completed {i+1}/{total_pages} pages ({(i+1)/total_pages*100:.0f}%)")
                
                time.sleep(delay)
            else:
                print(f"  ⚠️ Page turn failed from {current_page} to {next_page}")
                choice = input("Continue anyway? (y/N): ")
                if choice.lower() != 'y':
                    break
    
    total_time = time.time() - start_time
    
    # Results summary
    print("\n" + "=" * 80)
    print("📊 CHAPTERS 21-24 CAPTURE RESULTS")
    print("=" * 80)
    print(f"Page range: {start_page} - {end_page}")
    print(f"Pages attempted: {total_pages}")
    print(f"Successfully captured: {success_count}")
    print(f"Failed: {len(failed_pages)}")
    print(f"Success rate: {success_count/total_pages*100:.1f}%")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Average per page: {total_time/total_pages:.1f} seconds")
    
    if failed_pages:
        print(f"\nFailed pages: {failed_pages[:10]}{'...' if len(failed_pages) > 10 else ''}")
    
    print(f"\nOutput location: {chapter_folder.absolute()}")
    
    if success_count > 0:
        file_size_mb = sum(f.stat().st_size for f in chapter_folder.glob("*.png")) / (1024*1024)
        print(f"\n🎉 SUCCESS! {success_count} chapter pages captured!")
        print(f"   Total size: {file_size_mb:.1f} MB at full 1440x3120 resolution")
        print("   Ready for OCR processing.")
    
    # Restore original folder
    capture.output_folder = original_folder
    
    return success_count, failed_pages

def quick_chapter_test():
    """Test capture of just 2-3 pages to verify setup before full batch"""
    capture = DirectADBCapture()
    
    print("🧪 CHAPTER CAPTURE TEST")
    print("=" * 40)
    print("Testing capture of 3 pages to verify setup")
    
    input("Make sure Kindle is on page 515. Press Enter to test...")
    
    test_pages = [515, 516, 517]
    success = 0
    
    for i, page in enumerate(test_pages):
        print(f"\n[{i+1}/3] Testing page {page}")
        
        filename = f"test_page_{page}.png"
        
        if capture.take_screenshot(filename):
            success += 1
        
        if i < len(test_pages) - 1:  # Not the last page
            capture.turn_page()
            time.sleep(2)
    
    print(f"\nTest result: {success}/{len(test_pages)} pages captured successfully")
    
    if success == len(test_pages):
        print("✅ Test passed! Ready for full chapter capture.")
        return True
    else:
        print("❌ Test issues detected. Fix before full capture.")
        return False

if __name__ == "__main__":
    print("📚 Chapters 21-24 Capture Preparation")
    print("=" * 50)
    print("Options:")
    print("1. Quick test (3 pages) - Recommended first")
    print("2. Full capture (103 pages)")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == "1":
        if quick_chapter_test():
            run_full = input("\nRun full capture now? (y/N): ")
            if run_full.lower() == 'y':
                capture_chapters_21_24()
    elif choice == "2":
        capture_chapters_21_24()
    else:
        print("Invalid choice. Run again with 1 or 2.")