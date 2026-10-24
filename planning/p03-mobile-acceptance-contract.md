# P03 — Mobile Command Device: first acceptance contract

Source: Notion P03 development checkpoint (2026-10-24), QB1 Mobile Dashboard, AI Reconciliation Log. This is a test specification, not a claim of implementation.

## Parent and component boundary
P03 is the private, iPhone-first ecosystem command center. Smart-Notes is a source-capture component. Public Stadium website is a separate surface. Do not treat any of these as interchangeable.

## Pilot scenario: source preservation across sessions
1. On iPhone, enter a private P03 session and identify active room, user, and current CWT.
2. Submit a deliberately non-confidential test CWT containing punctuation, line breaks, speaker labels, and a date that must not be reinterpreted.
3. Return a receipt containing unique record ID, original text byte length, SHA-256 digest, UTC capture timestamp, destination, and save status. Show PENDING or ERROR if confirmation fails; never simulate success.
4. Close the browser/session and reopen; retrieve by record ID from persistent storage. Repeat from a second authorized device.
5. Compare retrieved UTF-8 bytes and SHA-256 digest with the submitted original. The record must match exactly, including speaker labels and line breaks.
6. Display source separately from any derived chronology or MAGIC candidates. Derived text must never overwrite source.
7. Log every write, verification, failure, and approved revision in the chronological Build Ledger.

## Security gate
No real defense-case material in the pilot. Require authenticated access, transport encryption, server-side access controls, protected storage, backups/recovery, and an explicit recording consent mechanism before confidential workflows are considered. No always-on microphone.

## Stage gates
CWT capture -> verified persistence -> retrieval/readback -> MAGIC (source-linked) -> HEISMAN (review) -> BUILD (separate QB1 approval). HIKE routes authorized actions; it is not an automatic device trigger.

## Pass/fail
PASS only if an actual iPhone submission persists, a session restart and another authorized device retrieve the identical bytes, and audit evidence is retained. Otherwise NOT VERIFIED.

## Existing evidence and gaps
Notion P03 checkpoint says no executable P03 mobile app was verified in inspected GitHub repositories. Smart-Notes local Python prototype and draft PR #3 do not satisfy this P03 acceptance test. Existing QB1 Mobile Dashboard is a Notion page, not proof of a deployed app.

## Next engineering investigation
Locate any existing private mobile prototype, hosting, and Claude website source before selecting implementation home; avoid duplicate code. Document source of truth, authentication provider, hosting, and storage before building private network access.
