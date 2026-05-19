# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a static personal portfolio website for Ameya Wagh, hosted on GitHub Pages. The site showcases robotics and self-driving car projects, publications, skills, and professional experience.

## Architecture

### Core Structure
- **Single-page application**: Main content in `index.html` with section-based navigation using anchor links
- **Project pages**: Separate HTML files in `projects/` directory (sdc.html, robocon.html, ml.html, whrl.html)
- **Template**: Built on HTML5 UP's "Prologue" template with significant customizations

### Key Components
- **Navigation**: Fixed sidebar with smooth scrolling to sections (`#top`, `#about`, `#skills`, `#portfolio`, `#publications`)
- **Dynamic content**: JavaScript-driven text rendering in `assets/js/about_me.js`
- **Styling**: Multiple CSS files for modular theming:
  - `main.css`: Base template styles
  - `aboutme.css`: Experience/education sections
  - `skills.css`: Skill bar visualizations
  - `publications.css`: Publication listings
  - `codeconsole.css`: Console-style text rendering

### JavaScript Architecture
- **jQuery-based**: Uses jQuery for DOM manipulation and scroll effects
- **Plugins**:
  - `jquery.scrolly.min.js`: Smooth scrolling
  - `jquery.scrollzer.min.js`: Section tracking for navigation
  - `skel.min.js`: Responsive layout framework
- **Custom scripts**:
  - `about_me.js`: Defines and renders about me text content
  - `typed.js`: Terminal-style typing effects (in node_modules)

### Asset Organization
```
assets/
  css/        # All stylesheets
  js/         # JavaScript files including jQuery plugins
  fonts/      # Custom fonts
  sass/       # Source SASS files (if customizing CSS)
images/       # Project images and GIFs
projects/     # Individual project showcase pages
font-awesome-4.7.0/  # Icon library
```

## Development Workflow

### Local Development
Since this is a static site, simply open `index.html` in a browser. For a local server:
```bash
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Making Changes

**Updating content**:
- Personal info: Edit `index.html` directly in the relevant sections
- About me text: Modify the array in `assets/js/about_me.js:1-6`
- Projects: Edit project HTML files in `projects/` or add new sections to `index.html`
- Skills: Update skill bars and labels in the `#skills` section of `index.html`

**Styling**:
- For template-wide changes: Edit `assets/css/main.css` or source SASS files
- For component-specific styles: Edit the corresponding CSS file (aboutme.css, skills.css, etc.)

**Adding new projects**:
1. Create new HTML file in `projects/` directory
2. Use existing project HTML as template (e.g., `projects/sdc.html`)
3. Update relative paths for assets (`../assets/`, `../images/`)
4. Add link in portfolio section of `index.html`

### GitHub Pages Deployment
This repository uses the `master` branch for GitHub Pages. The current working branch is `redesign`.

To deploy changes:
1. Make changes in `redesign` branch
2. Test locally
3. Merge to `master` branch
4. Push to GitHub - site auto-deploys to `https://ameyawagh.github.io`

### Important Paths
- **Main page**: `index.html`
- **Project pages**: `projects/*.html`
- **Custom JavaScript**: `assets/js/about_me.js`, `assets/js/console_text.js`, `assets/js/terminalType.js`
- **Icons**: `font-awesome-4.7.0/css/font-awesome.min.css`

## Technical Notes

### Responsive Design
- Mobile-first grid system using skel.min.js
- Breakpoints defined in main.css
- Use classes like `4u 12u$(mobile)` for responsive columns

### Browser Compatibility
- IE8/IE9 compatibility via conditional comments and polyfills
- Modern browsers fully supported

### Dependencies
- jQuery 3.2.1 (loaded from CDN and local fallback)
- Bootstrap 3.3.7 (loaded from CDN for modal components)
- Font Awesome 4.7.0 (local)
- Typed.js library in node_modules (terminal typing effects)

### Modal System
Uses W3.CSS modal system (not Bootstrap modals) for project descriptions in portfolio section.

## Common Patterns

### Adding a new section
1. Create `<section id="newsection" class="[one|two|three|four|five]">` in `index.html`
2. Add navigation link in `#nav` with matching href
3. Create corresponding CSS file if needed (e.g., `assets/css/newsection.css`)
4. Link CSS in `<head>` section

### Social links
Located in two places:
- Sidebar bottom: `#header .bottom .icons`
- Main page: Various sections (currently commented out in contact section)

### Image assets
- GIFs for project demos in `images/`
- Avatar/profile images in `images/`
- Referenced with relative paths from HTML files
