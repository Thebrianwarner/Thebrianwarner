# V1.0 candidate — changes from the Oct 9 Stadium build

Base: Oct 9, 2026 Claude Stadium build (artifact CiVPUWs2VznrStcVeHjcLh), preserved unchanged in `original/`.
Every change below is applied by `tools/build_v1.py`; each must match exactly or the build stops.

## Deploy hygiene
- Removed the "Stadium preview · Oct 9 build · not live" ribbon.
- Rebuilt as a proper standalone web page (doctype, language, charset, viewport, description, title) instead of the Claude preview wrapper.

## Mislabeling fixed (authorized by the Oct 9 10:35 AM QB1 ruling: "fix material mislabeling")
- Million Dollar Opportunity removed from the media roster (Gate 05, Media page). Show count 5 → 4.
- Million Dollar Opportunity added as a workshop block on Coaching (institutional booking layer), plus a Connect topic. Facts only from the Sept 19 QB1 ruling; everything else marked "Workshop details coming."
- "Live Cast & mentoring podcast" → "Mentoring podcast."

## Held for QB1 (not deleted)
- Championship Ladder section hidden (`hidden data-hold="qb1"`). QB1 said Oct 9 it is not his established feature. One attribute brings it back.
- Program page: "at the top of the ladder" → "The flagship mentoring operation"; ladder heading/button replaced with a Championship Conversation button.

## No claims of services that aren't running
- Saturday School: "is in session" → "Saturday School." · "Save my seat" → "Get on the list."
- Field Pass step marked "Not open yet." Investigator Training hero marked "In development."
- Connect: "Team Store order" → "Team Store"; Team Store prefill no longer asks for size/quantity/shipping.
- Program page: "Most people start with…" → "Start with…" (no customer base yet to describe).

## Layout
- Fixed 1px sideways scroll on 320px-wide phones (Coaching steps list).

## Update readiness
- Marked comments for the contact inbox setting, the MDO block, and the held Ladder.
