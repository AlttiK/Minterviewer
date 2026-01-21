PLACEHOLDER FOR CHROME EXTENSION ICON

To create icons for the Chrome extension:

Method 1 - Use Python script:
  cd backend
  pip install Pillow
  python generate_icons.py

Method 2 - Use online converter:
  1. Go to https://cloudconvert.com/svg-to-png
  2. Upload icon128.svg from this folder
  3. Convert to 16x16, 48x48, and 128x128
  4. Save as icon16.png, icon48.png, icon128.png

Method 3 - Use any image editor:
  Create simple blue square images with 🎯 emoji:
  - icon16.png (16x16 pixels)
  - icon48.png (48x48 pixels)
  - icon128.png (128x128 pixels)

The extension will still work without icons, but Chrome will show a default placeholder.

Note: This file should be replaced with actual PNG images.
