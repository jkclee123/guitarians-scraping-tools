#!/usr/bin/env python3
"""
url_to_pdf.py

Fetches Guitarians chord print pages and saves them as PDFs using Playwright.
Usage: uv run url_to_pdf.py -i <input_file> -o <output_directory> [-clicks <number>]
"""
import argparse
from pathlib import Path
from urllib.parse import unquote
import re
from playwright.sync_api import sync_playwright

def parse_chord_url(url):
    """Extract artist and song name from Guitarians chord URL."""
    # Extract the artist-song part after the ID
    pattern = r"/chord(?:/print)?/(\d+)/(.+?)(?:\?|$)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"Invalid chord URL format: {url}")

    # Decode the URL-encoded artist-song part
    artist_song = unquote(match.group(2))

    # Split artist and song name
    if '-' in artist_song:
        parts = artist_song.split('-', 1)
        artist = parts[0].strip()
        song_name = parts[1].strip()
    else:
        artist = "Unknown"
        song_name = artist_song.strip()

    return artist, song_name


def sanitize_filename(name):
    """Sanitize filename by removing/replacing invalid characters."""
    # Replace invalid filename characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Remove leading/trailing whitespace and dots
    name = name.strip(' .')
    # Limit length to prevent filesystem issues
    if len(name) > 100:
        name = name[:97] + "..."
    return name


def print_chord(url, output_path, clicks):
    """Fetch chord page and save as PDF at the specified path using Playwright's PDF generation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('body')
        page.wait_for_selector('li.twoinoneBtn')
        page.click('li.twoinoneBtn')
        page.wait_for_selector('li.fontLargerBtn')
        # page.click('li.fontSmallerBtn')
        for _ in range(clicks):
            page.click('li.fontLargerBtn')
        page.pdf(path=str(output_path))
        browser.close()


def preprocess_url(raw_url):
    """Ensure URL has /print/ segment and append default targetCapo parameter."""
    # Strip any existing query parameters
    base = raw_url
    # Insert 'print/' after '/chord/' if missing
    if '/chord/print/' not in base:
        base = base.replace('/chord/', '/chord/print/', 1)
    # Append default capo parameter
    return base


def process_urls_from_file(input_file, output_dir, clicks):
    """Process all URLs from the given file and save as PDFs to output directory."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into lines and filter out empty lines
    urls = [line.strip() for line in content.split('\n') if line.strip()]

    if not urls:
        raise ValueError(f"No URLs found in {input_file}")

    print(f"Found {len(urls)} URLs to process from {input_file}")

    # Process each URL
    for i, url in enumerate(urls, 1):
        try:
            print(f"Processing URL {i}/{len(urls)}: {url}")

            # Preprocess raw URL to ensure correct print path and query
            processed_url = preprocess_url(url)

            # Extract artist and song name for filename
            artist, song_name = parse_chord_url(processed_url)

            # Sanitize names for filename
            safe_artist = sanitize_filename(artist)
            safe_song = sanitize_filename(song_name)

            # Create filename
            filename = f"{safe_song}.pdf"
            output_path = output_dir / filename

            # Handle duplicate filenames by adding a counter
            counter = 1
            while output_path.exists():
                name_without_ext = output_path.stem
                output_path = output_path.parent / f"{name_without_ext}_{counter}.pdf"
                counter += 1

            # Generate PDF
            print_chord(processed_url, output_path, clicks)
            print(f"Saved PDF to {output_path}")

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            continue

    print(f"Processed {len(urls)} URLs. PDFs saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Guitarians chord print pages and save as PDFs")
    parser.add_argument("-i", "--input", required=True, help="Input text file containing chord URLs (one per line)")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save PDF files")
    parser.add_argument("-clicks", "--clicks", type=int, default=0, help="Number of times to click the font larger button (default: 0)")

    args = parser.parse_args()
    input_file = args.input
    output_dir = Path(args.output)
    clicks = args.clicks

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Validate output is a directory
    if not output_dir.is_dir():
        raise ValueError(f"Output path must be a directory: {output_dir}")

    process_urls_from_file(input_file, output_dir, clicks)