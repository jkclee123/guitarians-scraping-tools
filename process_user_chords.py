#!/usr/bin/env python3
"""
process_user_chords.py

Orchestrates the complete workflow to scrape, process, and merge user chord PDFs.
Usage: uv run process_user_chords.py <user_id> [-clicks <number>]
"""
import argparse
import sys
from pathlib import Path

from scrape_user_chords import scrape_user_chords
from unicode_fix import fix_unicode_in_file
from url_to_pdf import process_urls_from_file
from merge_pdfs import merge_pdfs_from_list, find_pdfs_in_directory


def main():
    parser = argparse.ArgumentParser(
        description='Orchestrate the complete workflow to scrape, process, and merge user chord PDFs.'
    )
    parser.add_argument(
        'user_id',
        help='User ID to process (e.g., 320385)'
    )
    parser.add_argument(
        '-clicks', '--clicks',
        type=int,
        default=0,
        help='Number of times to click the font larger button when generating PDFs (default: 0)'
    )
    
    args = parser.parse_args()
    user_id = args.user_id
    clicks = args.clicks
    
    # Determine file paths
    script_dir = Path(__file__).parent
    txt_file = script_dir / f"{user_id}.txt"
    pdf_dir = script_dir / "pdfs" / user_id
    merged_pdf = script_dir / "pdfs" / f"{user_id}_merged.pdf"
    
    # Step 1: Scrape user chords
    print(f"\n{'='*60}")
    print(f"Step: Scraping chord links for user {user_id}")
    print(f"{'='*60}\n")
    
    try:
        scrape_user_chords(user_id)
        print(f"\n✓ Successfully completed: Scraping chord links for user {user_id}\n")
    except Exception as e:
        print(f"\n❌ Error: Scraping chord links for user {user_id} failed: {e}")
        sys.exit(1)
    
    # Check if txt file was created
    if not txt_file.exists():
        print(f"❌ Error: Expected file {txt_file} was not created")
        sys.exit(1)
    
    # Step 2: Fix Unicode in the txt file
    print(f"\n{'='*60}")
    print(f"Step: Fixing Unicode characters in {txt_file}")
    print(f"{'='*60}\n")
    
    try:
        fix_unicode_in_file(txt_file)
        print(f"\n✓ Successfully completed: Fixing Unicode characters in {txt_file}\n")
    except SystemExit as e:
        # fix_unicode_in_file uses sys.exit(), so we catch SystemExit
        if e.code != 0:
            print(f"\n❌ Error: Fixing Unicode characters failed")
            sys.exit(e.code)
    except Exception as e:
        print(f"\n❌ Error: Fixing Unicode characters failed: {e}")
        sys.exit(1)
    
    # Step 3: Generate PDFs from URLs
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Step: Generating PDFs from chord URLs (clicks={clicks})")
    print(f"{'='*60}\n")
    
    try:
        process_urls_from_file(str(txt_file), pdf_dir, clicks)
        print(f"\n✓ Successfully completed: Generating PDFs from chord URLs\n")
    except Exception as e:
        print(f"\n❌ Error: Generating PDFs failed: {e}")
        sys.exit(1)
    
    # Check if any PDFs were created
    pdf_files = list(pdf_dir.glob('*.pdf'))
    if not pdf_files:
        print(f"❌ Error: No PDF files were created in {pdf_dir}")
        sys.exit(1)
    
    # Step 4: Merge PDFs
    print(f"\n{'='*60}")
    print(f"Step: Merging PDFs into {merged_pdf}")
    print(f"{'='*60}\n")
    
    try:
        pdf_file_paths = find_pdfs_in_directory(str(pdf_dir))
        if not pdf_file_paths:
            print(f"❌ Error: No PDF files found in {pdf_dir}")
            sys.exit(1)
        
        success, total_pages, processed_files = merge_pdfs_from_list(pdf_file_paths, str(merged_pdf))
        
        if not success:
            print(f"\n❌ Error: Merging PDFs failed")
            sys.exit(1)
        
        print(f"\n✓ Successfully completed: Merging PDFs into {merged_pdf}\n")
    except Exception as e:
        print(f"\n❌ Error: Merging PDFs failed: {e}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("🎉 Workflow completed successfully!")
    print(f"{'='*60}")
    print(f"📄 Merged PDF: {merged_pdf}")
    print(f"📁 Individual PDFs: {pdf_dir}")
    print(f"📝 Chord URLs: {txt_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

