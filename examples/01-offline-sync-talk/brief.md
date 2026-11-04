# Brief: Offline sync tech talk

**Input style:** a full slide-by-slide outline with bullets.

- **Type:** technical talk at a developer meetup (about 10 minutes)
- **Audience:** web and mobile developers
- **Product:** "Driftnote", a fictional note-taking app
- **Slides:** exactly 5

## Slide 1: Title
- "Write anywhere, sync later"
- Subtitle: How Driftnote keeps offline edits safe
- Speaker line: Driftnote engineering team · Developer meetup talk

## Slide 2: The problem
- You edit a note on a train with no signal
- Your laptop changed the same note an hour earlier
- When both reconnect, "last write wins" silently throws one edit away
- Message: offline is normal, so losing edits is a design bug, not bad luck

## Slide 3: Our approach (a 4-step flow)
- Save every change locally first
- Record each change as a small operation in a log
- Send the log when the device reconnects
- Merge operations on every device in the same order
- Message: the device never waits for the server

## Slide 4: Merging two edits
- Show the phone edit and the laptop edit side by side, then the merged note
- Include a short code snippet (about 6–8 lines of Python) showing operations sorted by `(timestamp, device_id)` and applied in order
- Point: same inputs give the same result on every device

## Slide 5: Status and what's next
- Shipped: local-first storage, operation log
- In testing: merging edits inside the same paragraph
- Planned: attachments, shared notebooks
- Close with "Questions?" and an invitation to try the beta

Don't invent user numbers, performance figures or benchmark results.
