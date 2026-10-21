# Instructions for future maintainers

Read MAINTENANCE.md and BRANDING.md before editing this builder.
Inspect the current branch and deployed version first. Preserve the working app and make a backup branch before functional changes.
Never clear or migrate user localStorage casually: existing template keys, storage namespace, saved positions and measurement sizes must survive.
Use the exact approved logo from branding.js; preserve explicit SVG dimensions.
Limit work to the requested template or behavior and verify completed PNG export and existing calibration.
Do not claim access to the user's phone settings or claim a backup of them unless an actual settings export was obtained.
