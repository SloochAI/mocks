# Screenshot Generator for HTML Mockups

https://sloochai.github.io/mocks/

This project generates screenshots of all HTML mockups using Playwright.

## Setup for NixOS

1. Enter the Nix shell environment:

```bash
nix-shell .
```

2. Install Playwright browsers (if needed):

```bash
playwright install chromium
```

3. Run the screenshot generator:

```bash
python screenshot_generator.py
```

## What it does

- Finds all `.html` files in the `mockups/` folder
- Takes full-page screenshots of each mockup
- Saves screenshots as `.png` files in the `images/` folder
- Uses a 1920x1080 viewport for consistent screenshots

## Output

Screenshots will be saved in the `images/` folder with the same name as the HTML file but with `.png` extension:

- `mockups/login.html` → `images/login.png`
- `mockups/dashboard.html` → `images/dashboard.png`
- etc.

## Troubleshooting

If you encounter browser issues, make sure you're running from within the nix-shell environment, as it provides all necessary system dependencies for Playwright.
