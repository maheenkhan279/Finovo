# FINOVO Logo Integration Guide

## Overview

The FINOVO logo has been integrated into the navbar/header of the application. The logo is displayed consistently across all pages and serves as a clickable link to the homepage.

## Logo Location

**Path**: `static/images/finovo_logo.png`

The logo file should be placed in the `static/images/` directory.

## Implementation Details

### HTML Structure

The logo is integrated in `templates/base.html`:

```html
<div class="logo">
    <a href="{{ url_for('home') }}" class="logo-link" title="FINOVO - Financial Education Platform">
        <img src="{{ url_for('static', filename='images/finovo_logo.png') }}" 
             alt="FINOVO Logo" 
             class="logo-image"
             onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='block';">
        <h1 class="logo-text">Finovo</h1>
    </a>
</div>
```

### Features

✅ **Clickable Logo** - Links to homepage (`/`)
✅ **Fallback Text** - Shows "Finovo" text if image fails to load
✅ **Responsive Design** - Adapts to mobile screens
✅ **Proper Styling** - Maintains aspect ratio and professional appearance
✅ **Hover Effect** - Subtle opacity change on hover

### CSS Styling

The logo is styled in `static/css/styles.css`:

- **Height**: 45px (desktop), 35px (mobile)
- **Max Width**: 200px (desktop), 150px (mobile)
- **Aspect Ratio**: Maintained automatically
- **Alignment**: Vertically centered with navbar items

### Responsive Behavior

- **Desktop**: Logo height 45px, max-width 200px
- **Mobile** (< 768px): Logo height 35px, max-width 150px
- Text fallback scales proportionally

## Logo Requirements

### File Format
- **Recommended**: PNG with transparent background
- **Alternative**: SVG (scalable, better quality)
- **File Name**: `finovo_logo.png` (or update path if different)

### Image Specifications
- **Aspect Ratio**: Any (will be maintained)
- **Background**: Transparent preferred
- **Colors**: Should match FINOVO brand colors (blue theme)
- **Size**: Optimized for web (under 100KB recommended)

## Setup Instructions

1. **Export Logo from PDF**
   - Open the PDF logo file
   - Export as PNG (or SVG)
   - Ensure transparent background if possible
   - Optimize for web use

2. **Place Logo File**
   - Save as `finovo_logo.png`
   - Place in `static/images/` directory
   - Verify file path: `static/images/finovo_logo.png`

3. **Test Integration**
   - Start Flask app: `python app.py`
   - Navigate to homepage
   - Verify logo appears in navbar
   - Click logo to verify it links to home
   - Test on mobile/responsive view

## Fallback Behavior

If the logo image fails to load:
- Image is hidden automatically
- Text "Finovo" appears in its place
- Styling matches original text logo
- No broken image icons

## Customization

### Change Logo Size

Edit `static/css/styles.css`:

```css
.logo-image {
    height: 50px; /* Adjust height */
    max-width: 250px; /* Adjust max width */
}
```

### Change Logo Position

The logo is in the left side of the navbar. To adjust:

```css
.logo {
    margin-right: 2rem; /* Add spacing */
}
```

### Use Different File Format

If using SVG or different filename, update `templates/base.html`:

```html
<img src="{{ url_for('static', filename='images/finovo_logo.svg') }}" ...>
```

## Testing Checklist

- [ ] Logo file exists at `static/images/finovo_logo.png`
- [ ] Logo displays correctly in navbar
- [ ] Logo is clickable and links to home
- [ ] Logo maintains aspect ratio
- [ ] Logo scales properly on mobile
- [ ] Fallback text appears if image fails
- [ ] Logo doesn't break navbar layout
- [ ] Logo matches FINOVO brand colors

## Troubleshooting

### Logo Not Appearing
1. Check file path: `static/images/finovo_logo.png`
2. Verify file name matches exactly (case-sensitive)
3. Check browser console for 404 errors
4. Ensure Flask static file serving is working

### Logo Too Large/Small
- Adjust `height` in `.logo-image` CSS
- Adjust `max-width` if needed

### Logo Breaking Layout
- Check navbar flexbox alignment
- Verify logo container has proper spacing
- Test on different screen sizes

### Fallback Not Working
- Check JavaScript is enabled
- Verify `onerror` handler is present
- Check browser console for errors

## Notes

- Logo uses Flask's `url_for('static', ...)` for proper path handling
- Logo is accessible (alt text provided)
- Logo maintains professional appearance
- No external dependencies required
- Works with existing FINOVO styling

