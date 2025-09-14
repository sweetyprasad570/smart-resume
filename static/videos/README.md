# Video Background Files

This directory should contain video files for the homepage background.

## Required Video File:
- `background.mp4` - Main background video with lightning/gradient effects

## Video Specifications:
- Format: MP4 (H.264 codec)
- Resolution: 1920x1080 (or higher for better quality)
- Duration: 10-30 seconds (will loop)
- File size: Keep under 5MB for optimal performance
- Content: Lightning effects, gradient animations, or abstract motion graphics
- Audio: Muted (no sound required)

## Recommended Video Sources:
1. Create custom video using Adobe After Effects or similar
2. Use stock video sites (Pexels, Pixabay) for free background videos
3. Generate AI video with tools like RunwayML or Kaiber
4. Use CSS animations as fallback (already implemented)

## Current Implementation:
- Video will auto-play, muted, in loop
- Falls back to animated gradient background if video fails to load
- Responsive design with performance optimizations
- Accessibility support for reduced motion preferences

## Performance Tips:
- Use compressed video formats
- Optimize for mobile devices
- Test loading times on different connections
- Consider using multiple video formats for better browser support
