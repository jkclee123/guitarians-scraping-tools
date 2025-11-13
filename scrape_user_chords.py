#!/usr/bin/env python3
"""
scrape_user_chords.py

Scrapes all chord links from a Guitarians user profile page.
Usage: uv run scrape_user_chords.py <user_id>
"""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def scrape_user_chords(user_id):
    """Scrape all chord links from a user's Guitarians profile page."""
    base_url = "https://zh-hk.guitarians.com"
    user_url = f"{base_url}/user/{user_id}"
    
    print(f"Fetching chord links from {user_url}...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # Set a realistic user agent to avoid bot detection
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        # Navigate to the page with increased timeout and more lenient wait strategy
        try:
            page.goto(user_url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Warning: Navigation timeout or error: {e}")
            print("Attempting to continue with current page state...")
        
        # Wait for the content to load (adjust selector based on actual page structure)
        # Try waiting for common elements that might be present
        try:
            page.wait_for_selector('body', timeout=10000)
            # Wait a bit more for dynamic content to load
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Warning: Timeout waiting for page content: {e}")
        
        # Get the page content
        content = page.content()
        
        # Close the browser
        browser.close()
    
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all links that contain "/chord/" in their href
    chord_links = set()
    all_links = soup.find_all('a', href=True)
    
    for link in all_links:
        href = link.get('href', '')
        # Check if the link is a chord link
        if '/chord/' in href:
            # Convert relative URLs to absolute URLs
            full_url = urljoin(base_url, href)
            # Remove any fragment identifiers
            parsed = urlparse(full_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                clean_url += f"?{parsed.query}"
            chord_links.add(clean_url)
    
    # Sort links for consistent output
    sorted_links = sorted(chord_links)
    
    if not sorted_links:
        print(f"Warning: No chord links found on {user_url}")
        print("The page might be empty, require authentication, or have a different structure.")
        return
    
    # Write chord links to file
    output_file = Path(f"{user_id}.txt")
    output_file.write_text('\n'.join(sorted_links), encoding='utf-8')
    print(f"\nSuccessfully wrote {len(sorted_links)} chord links to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrape chord links from a Guitarians user profile page.'
    )
    parser.add_argument(
        'user_id',
        help='User ID to scrape chord links from (e.g., 320385)'
    )
    
    args = parser.parse_args()
    scrape_user_chords(args.user_id)


