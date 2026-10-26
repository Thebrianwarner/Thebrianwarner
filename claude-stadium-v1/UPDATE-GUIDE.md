# How to update THEBRIANWARNER.com after V1.0

The site is one file: `public_html/index.html`. Every page (Stadium, Story, Championship Conversation, The Program, Media, Coaching, Team Store, Equipment Room, Saturday School, Investigators, Connect) lives inside it as its own section, so an update is: change the section → re-upload the one file. Nothing has to be rebuilt.

## The safe loop (Version 1.1, 1.2, 1.3 …)
1. Brian decides what changes and where it lives (flip card, Players' Lounge, Coach's Office, Media, Team Store …).
2. Claude edits the file, tests it on phone/foldable/desktop, and sends a preview.
3. QB1 approves.
4. Back up the live `index.html` in File Manager (rename it `index-before-vX.Y.html`), upload the new one, verify, log it.

## Where things are in the file
Each page starts with `<main class="pv-page" data-page="NAME">`. Search for the page name.

| To change… | Search the file for… |
|---|---|
| A Stadium gate flip card | `id="g-cc"` (Championship Conversation), `g-oiac`, `g-cps`, `g-ss`, `g-booth`, `g-store`, `g-inv`, `g-wb`, `g-eq` |
| A Team Store shirt card | the shirt name, e.g. `FIRST IN / FIRST OUT` |
| A status label | `status-live` (Available now), `status-dev` (In development), `status-soon` (Coming soon), `status-lock` (Participants only) |
| The contact inbox | `SETTING: contact inbox` → put the approved address in `data-email=""` |
| Million Dollar Opportunity block | `CONTENT: Million Dollar Opportunity` |
| The held Championship Ladder | `HELD FOR QB1` → remove `hidden` to bring it back |

### Adding a new flip card
Copy one whole gate card (from its opening `<li` to its closing `</li>`), paste it next to the others, change the `id`, gate number, room, name, status, back-face text and link. Text only from approved source; anything missing says "coming" rather than being written for Brian.

### Adding photographs or video
1. Brian supplies the original. The original is kept untouched in the archive; a web-sized copy (JPG/WebP, about 1600px wide, under ~400 KB) goes up.
2. Upload the web copy to `public_html/assets/images/` (create the folder the first time).
3. In the page, add `<img src="assets/images/FILENAME.jpg" alt="what's in the photo" loading="lazy">` where it belongs.
4. Video: upload to YouTube (unlisted or public, Brian's call) and embed, rather than putting large video files on the host.

### Changing text
Find the sentence, replace it, keep Brian's words as given. Keep the ™ marks: THEBRIANWARNER™, THE CHAMPIONSHIP CONVERSATION™, Operation: I Am a Champion™, Championship Performance System™.

## Rebuilding this exact V1.0 from the Oct 9 build
`python3 -I tools/build_v1.py .` — reads `original/index-oct9-artifact.html` (the preserved Oct 9 build), applies every V1 fix listed in the script, and writes `site/public_html/index.html`. `python3 tools/test_v1.py .` re-runs the device tests.

## Later, not V1
The conversational publishing flow (tap +, attach photo, classify, approve, auto-place on the live site), GitHub version control, and phone/watch controls are future versions. They build on this same loop — the approval step never goes away.
