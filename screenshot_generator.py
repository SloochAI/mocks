#!/usr/bin/env python3
"""
Script to generate screenshots of all HTML mockups in the mockups folder.
Saves screenshots as PNG files in the images folder.
"""

import os
import asyncio
import sys
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright


def setup_playwright():
    """Setup Playwright for NixOS"""
    try:
        import playwright
        print("Playwright is installed")
    except ImportError:
        print("Installing Playwright...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "playwright"])

    # Install browsers
    try:
        print("Installing/updating Playwright browsers...")
        subprocess.check_call(
            [sys.executable, "-m", "playwright", "install", "chromium"])
        print("Playwright setup complete!")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Browser installation failed: {e}")
        print("You may need to install browsers manually or use nix-shell")


async def take_screenshot(html_file_path, output_path, viewport_width=1920, viewport_height=1080):
    """Take a screenshot of an HTML file."""
    async with async_playwright() as p:
        # Try to use system Chromium first, fall back to Playwright's browser
        chromium_path = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH')

        launch_options = {
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-web-security',
                '--allow-running-insecure-content',
                '--disable-features=VizDisplayCompositor',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--virtual-time-budget=5000'
            ]
        }

        if chromium_path and os.path.exists(chromium_path):
            launch_options['executable_path'] = chromium_path
            print(f"Using system Chromium: {chromium_path}")
        else:
            print("Using Playwright's Chromium")

        browser = await p.chromium.launch(**launch_options)
        page = await browser.new_page()

        # Set viewport size
        await page.set_viewport_size({"width": viewport_width, "height": viewport_height})

        # Load the HTML file
        file_url = f"file://{html_file_path}"
        await page.goto(file_url, wait_until='load')

        # Wait for the page to load completely and any potential animations
        await page.wait_for_timeout(2000)

        # Take screenshot
        await page.screenshot(path=output_path, full_page=True)

        await browser.close()


async def generate_all_screenshots():
    """Generate screenshots for all HTML files in the mockups folder."""
    script_dir = Path(__file__).parent
    mockups_dir = script_dir / "mockups"
    images_dir = script_dir / "images"

    # Ensure images directory exists
    images_dir.mkdir(exist_ok=True)

    # Get all HTML files
    html_files = list(mockups_dir.glob("*.html"))

    if not html_files:
        print("No HTML files found in mockups directory!")
        return

    print(f"Found {len(html_files)} HTML files to process...")

    # Process each HTML file
    for html_file in html_files:
        output_filename = html_file.stem + ".png"
        output_path = images_dir / output_filename

        print(f"Taking screenshot of {html_file.name}...")

        try:
            await take_screenshot(str(html_file.absolute()), str(output_path))
            print(f"✓ Screenshot saved: {output_filename}")
        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {str(e)}")

    print(f"\nScreenshots saved in: {images_dir.absolute()}")


async def main():
    """Main function to set up and run screenshot generation"""
    print("Setting up screenshot generator for NixOS...")
    setup_playwright()

    print("\nStarting screenshot generation...")
    await generate_all_screenshots()

if __name__ == "__main__":
    asyncio.run(main())
