# THEBRIANWARNER.com — Version 1.0 Deployment Runbook

**Status: PREPARED · NOT DEPLOYED · HOLDING FOR QB1 AUTHORIZATION**
Prepared by Claude, Friday October 9, 2026. Nothing in this kit has been uploaded, published, or changed on the live site, hosting, domain, or DNS.

---

## What we know about the field (verified vs. not)

| Item | Status | Evidence |
|---|---|---|
| Domain points to hosting | **Verified today** | `thebrianwarner.com` and `www.thebrianwarner.com` both resolve to `66.96.149.24` (Network Solutions / Web.com hosting range). |
| DNS / A-record work | Recorded complete (Oct 2026) | Ecosystem record: "DNS/A-record work complete; deployment at File Manager / public_html stage." |
| Upload method | Recorded | Oct 9 Claude build report: "deployment is a manual Network Solutions upload to public_html." |
| What the live site shows right now | **Not verified** | The site blocks automated fetching and this workspace's network can't reach it. Brian checks it by eye at step 1. |
| Hosting type (Linux/Apache vs. other) | Not verified | Seen once logged in. Doesn't change the V1 plan: one static `index.html` works on any web host. |
| GitHub / automatic publishing | Not set up | Not needed for V1 (QB1 ruling Oct 9). |

**The plain-language version:** the domain is already pointed at Network Solutions. V1.0 is one file — `index.html`. Going live means putting that one file into the `public_html` folder on Network Solutions. No DNS change, no purchase, no new service.

---

## What QB1 needs to do (the only steps that need Brian)

1. **Sign in to Network Solutions** on the desktop (Brian types his own password and handles any 2-factor code — Claude never asks for or sees credentials).
2. **Say the word:** "Authorized: publish V1.0 to THEBRIANWARNER.com." Until then, Claude holds.
3. **Answer the five open calls** listed in the preflight report (contact inbox, Ladder, Sept 28 base, BDUB v. BDUB visibility, Equipment Room). Only the contact inbox blocks a clean launch; the others can ride as-is.

## How the upload runs (desktop session, after authorization)

Claude can do this two ways from the desktop app — both need Brian signed in:
- **Built-in browser / Chrome:** Claude opens Network Solutions → Hosting → File Manager in a browser where Brian is already signed in, and performs the steps below while Brian watches.
- **Brian drives, Claude calls the plays:** Brian clicks; Claude reads the screen and calls each step.

Whether the desktop session has the browser tools is checked at kickoff — this cloud session cannot see Brian's computer, so it has **not** been verified yet.

### The play, step by step
1. **Look first.** Open https://thebrianwarner.com and https://www.thebrianwarner.com. Screenshot what's there (placeholder page, old site, or error). That's the "before" film.
2. **File Manager → `public_html`.** List what's in the folder. Do not delete anything.
3. **Back it up.** If an `index.html` (or `index.htm`, `index.php`, `default.html`) already exists, download it, then rename it in place to `index-before-v1-2026-10-09.html`. If a host default page like `index.htm` or `default.html` exists, rename it too — hosts pick those ahead of or alongside `index.html`.
4. **Upload** `public_html/index.html` from this kit into `public_html`.
5. **Confirm the file.** File size should be **145,900 bytes**. (SHA-256 is in `CHECKSUMS.txt` if File Manager shows it.)
6. **Verify live** on phone and desktop: home loads with the stadium, a flip card flips, Menu opens, the bottom dock works, Media shows four shows, Coaching shows the Million Dollar Opportunity workshop block, no "preview · not live" ribbon. Check `http://`, `https://`, with and without `www`.
7. **Log it** in the AI Reconciliation Log with the before/after screenshots.

### If something goes wrong (rollback, under 2 minutes)
- Delete or rename the new `index.html`, then rename `index-before-v1-2026-10-09.html` back to its original name. The site is exactly as it was.
- If the page loads but looks broken: hard-refresh (caches), then check that the file uploaded completely (size matches).
- If `https://` shows a certificate warning: that's an SSL setting on the hosting account, not the website file. It needs Brian's decision because it can be a paid add-on — **stop and ask**.

## Things that are out of bounds without a separate QB1 call
Changing DNS, nameservers, or domain settings · buying or renewing anything (SSL, hosting upgrades, email) · turning on payments, booking, or sign-in · deleting files on the host · connecting GitHub or auto-publishing.
