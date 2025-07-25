# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website for the JustBe Himalaya Buddhist Temple project (`himalaya.justbetemple.org`). The site is hosted on GitHub Pages and provides information about a fundraising campaign for establishing a Buddhist temple and base camp in the Himalayas.

## Technology Stack

- **Frontend**: Single-page HTML5 application with embedded CSS and JavaScript
- **Styling**: Tailwind CSS (via CDN) with custom CSS for animations and hero backgrounds
- **Fonts**: Google Fonts (Noto Serif KR, Noto Sans KR) for Korean typography
- **Hosting**: GitHub Pages
- **No build process**: This is a static site with no compilation or bundling required

## Project Structure

```
maya-web/
├── index.html          # Main and only HTML file containing the entire application
├── resource/img/       # Image assets directory
│   └── maya.jpeg      # Local image asset
├── package.json       # Empty JSON object (unused)
├── README.md          # Korean project documentation
└── CNAME             # GitHub Pages domain configuration
```

## Development Approach

Since this is a single-file static website:

1. **All code is in `index.html`**: HTML structure, CSS styles (in `<style>` tag), and JavaScript (in `<script>` tag) are all contained in one file
2. **No separate CSS/JS files**: Styles and scripts are embedded directly in the HTML
3. **External dependencies**: Uses CDN links for Tailwind CSS and Google Fonts
4. **No build step required**: The site can be served directly by opening `index.html` in a browser

## Key Features Implemented

- **Responsive design** with mobile-first approach using Tailwind CSS
- **Scroll animations** with intersection observer for progressive content reveal  
- **Progress bar animation** for donation tracking
- **Account number copy functionality** for easy donations
- **Korean typography** optimized with Noto fonts
- **Hero section** with parallax background effect
- **Donation tracking** with visual progress indicators

## Content Management

The site contains Korean content about:
- Buddhist temple fundraising campaign
- Himalaya pilgrimage project details  
- Donation information and progress tracking
- Contact information and bank account details

## Local Development

To work on this project locally:
1. Simply open `index.html` in a web browser
2. No server setup or build process required
3. Edit the HTML file directly for any changes
4. Refresh browser to see changes

## External Resources

- Uses Unsplash images via CDN for backgrounds
- External image hosting for the Maitreya Buddha statue photo
- Tailwind CSS and Google Fonts loaded from CDNs