# Porky Yorkie Measurement Builder maintenance handoff

Saved 2026-10-21. Repository: https://github.com/ThePorkyYorkie/-porky-yorkie-builder
Live builder: https://theporkyyorkie.github.io/-porky-yorkie-builder/
User-confirmed working application commit: 8cb55e8f902b727181ca7d3f6fdaa0d856e1cea2
Stable backup branch: backup/stable-2026-10-21

## Preserve the working system
Inspect current main and this guide before editing. Do not rebuild from an old chat, ZIP, or initial commit 75c3e897. Make a backup of the current verified commit before functional changes. Make narrow changes and preserve all other templates. Roll back with a new forward commit restoring a verified tree; do not force-reset main.

The app currently has 29 templates. index.html contains template definitions, fields, preview, calibration, title counter and export. branding.js contains the exact approved user-provided Yorkie logo and per-template LOGO_AREAS. BRANDING.md documents branding. Use the exact approved badge, never a generated substitute.

## Device-only settings
Saved positions, measurement sizes and custom uploaded masters are in the user's browser localStorage, not GitHub. This checkpoint cannot back up the user's iPhone data. Preserve STORAGE_PREFIX porkyYorkieBuilderV3_ and existing template keys and storageKey suffixes. Do not clear storage, rename keys or replace saved positions. A new browser, domain, or cleared website data can lose these settings.

Preserve existing coordinates and sizes when adding a missing field; merge only absent fields. Three-piece suit includes Vest Waist between Vest Pit to Pit and Vest Length. Two-piece suit includes Thigh Across between Rise and Inseam. The user spent hours calibrating existing templates.

## Rendering requirements
Keep SVG loading with explicit pixel width and height derived from viewBox before loading the Image. Without it, mobile SVG dimensions can collapse and show a giant cropped logo instead of the guide. Keep explicit destination dimensions for canvas drawImage. Existing guides are square: SVG guides 1248 by 1248 and raster masters 1254 by 1254.

Preview fonts must scale from the same fixed font size used by export. Do not introduce a mobile minimum font size that makes preview text look larger than the export. Item Name and Tagged Size remain fixed size. Measurement scaling is per-template.

The Item Name counter appears immediately below its input on every template. It measures rendered text width at the fixed font size using TITLE_LINE_BOUNDS and the current saved position. Letters have different widths, so there is no universal character limit. It reports characters, percentage and estimated remaining similar-width characters. It is advisory: no automatic shrinking, truncating or export blocking.

Export Finished PNG flattens the guide plus entered text into a square PNG, then opens the finished-image dialog. On iPhone the user can hold that finished image and Save to Photos; supported native sharing uses a separate user tap. Holding the original editor background alone saves the blank guide. Preserve the completed-image export and current inputs.

## Adding a clothing template
1. Inspect current main and create a stable checkpoint.
2. Obtain the full square master image, display name and required measurement fields.
3. Add a unique TEMPLATES key, ordered fields and source image. Preserve all existing keys and templates.
4. Add the new template's logo rectangle to LOGO_AREAS. Keep the exact official logo and verified SVG dimensions.
5. Add TITLE_LINE_BOUNDS measured from the new header. Check any template-specific image/base-size logic for the new master.
6. Add sensible default positions. If extending an existing template, merge only missing fields into saved positions.
7. Verify the correct full image, field order, dragging, sizes, title meter and square PNG with all entered text. Check existing saved settings survive.
8. Deploy a scoped change and verify the actual live version. Do not claim deployment success from a code write alone.

## Known status
User confirmed the title-space counter works as desired. Dropdown is alphabetically sorted. Measurement-size slider currently remains visible; showing it only in Position Adjust Mode was requested earlier but deferred. Do not treat that as completed or change it without renewed scope.

The stable branch preserves application code and repository assets, not device-only calibration. This documentation change does not change application behavior.
