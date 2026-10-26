# Claude Stadium V1.0 — source package (handoff branch `claude-stadium-v1`)

**Status: SOURCE HANDOFF ONLY · NOT DEPLOYED · NOT MERGED · NOT QB1-APPROVED FOR PUBLICATION**

Authorized by QB1 (Brian Warner), Oct 26, 2026, as recorded in the Notion AI Reconciliation Log:
"QB1 authorized unified Stadium; Claude GitHub source handoff". This branch preserves Claude's
Oct 9 Stadium work beside ChatGPT's `build/stadium-functional-homepage`. It does not change that
branch or `main`, and it does not deploy anything.

## What's here

| Path | What it is | Provenance |
|---|---|---|
| `original/index-oct9-artifact.html` | **Original Oct 9 Stadium build**, exactly as published in Claude artifact https://claude.ai/artifact/CiVPUWs2VznrStcVeHjcLh (includes the "preview · not live" ribbon). Untouched. | Claude, Oct 9, 2026 |
| `site/public_html/index.html` | **V1.0 candidate** — the original plus the Oct 9 10:50 AM fixes listed in `CHANGELOG-v1.0.md`. This is the file that would be uploaded to Network Solutions `public_html` on QB1 authorization. | Claude, Oct 9, 2026, 10:50 AM CDT |
| `tools/build_v1.py` | Reproducible build: original → V1.0. Every edit must match exactly or it stops. `python3 -I claude-stadium-v1/tools/build_v1.py claude-stadium-v1` | Claude, Oct 9 |
| `tools/test_v1.py` | Headless Chromium device tests (7 viewports × 12 routes + content checks). Needs `playwright`. `python3 claude-stadium-v1/tools/test_v1.py claude-stadium-v1` | Claude, Oct 9 |
| `reports/test-results.json`, `reports/screenshots/` | Oct 9 test run: 38 checks, 0 failed. | Claude, Oct 9 |
| `reports/rerun-2026-10-26/` | Same tests re-run Oct 26 on the unchanged V1.0 file: 38 checks, 0 failed. | Claude, Oct 26 |
| `DEPLOY-RUNBOOK.md` | Network Solutions backup → upload → verify → rollback steps. Held at QB1 gate. | Claude, Oct 9 |
| `UPDATE-GUIDE.md` | How to change photos, video, text and flip cards without rebuilding. | Claude, Oct 9 |
| `CHANGELOG-v1.0.md` | Every change from original to V1.0, and why. | Claude, Oct 9 |
| `CHECKSUMS.txt` | Oct 9 checksums (as delivered). | Claude, Oct 9 |
| `package/THEBRIANWARNER-V1.0-deploy-kit.zip` | The exact zip delivered in the Oct 9 Claude chat (byte-for-byte). Everything above except `package/`, `lineage/`, `reports/rerun-2026-10-26/`, this README and `MANIFEST-SHA256.txt` comes out of this zip unchanged. | Claude, Oct 9 |
| `package/THEBRIANWARNER-V1.0-index.html` | Same file as `site/public_html/index.html`, under the name it was delivered with. | Claude, Oct 9 |
| `lineage/` | Earlier Claude prototypes, as published in their artifacts, for history only: Sept 17 first prototype (H1gSD4FYnehdnQziv2s1QN), Sept 19 Prototype v2 (SYHdet1FornHewW3scwekV), Sept 28 THEBRIANWARNER.com base (LsqqjUEYwSJPi9GNZbqNk1). Not part of V1.0. | Claude, Sept 2026 |
| `MANIFEST-SHA256.txt` | SHA-256 of every file on this branch folder. | Claude, Oct 26 |

## Key hashes
- V1.0 candidate `site/public_html/index.html`: `975c8830d3eb3f552f9081ace8a9ed65357807d7f5102474d0ec2dc027939003` (145,900 bytes)
- Original `original/index-oct9-artifact.html`: `05ffa14592e59604d70512bd9532a85da6a53fb40ce25cdae28af79eba43815d`
- Deploy kit zip: `afd4f0589bba3f207bd32b3974675b54d13e18efe31ad1ea8bf1ea4906bb7e96`

## Known gaps
- The separate Oct 9 4:18 AM deploy file (SHA-256 `a50a3984…a155`, cited in the Oct 9 build report) is **not** in this package; that file lives only in the earlier Claude chat.
- Design assets: none exist as separate files. The stadium scene, icons and shirt mockups are drawn in code inside the HTML. No photographs or video have been supplied.
- The Oct 9 build-report doc is a Claude Docs artifact (https://claude.ai/artifact/EQGRdJRbCcQFg9QFDj6mpB); its content is not exportable as a file here.
- Not tested: physical iPhone/Android, Safari, real Google Fonts, the live host.

## What is approved vs. proposed
See the Notion AI Reconciliation Log entries of Oct 9 (build report, 10:50 AM preflight) and Oct 26
(Claude reconciliation). All AI-introduced design and copy listed there remains **proposed, not approved**.
Integration with ChatGPT's build, merging, and deployment all require separate QB1 authorization.
