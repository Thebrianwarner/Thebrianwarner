"""Build THEBRIANWARNER.com Version 1.0 candidate from the Oct 9 Stadium build.

Reproducible: reads the preserved Oct 9 artifact copy, applies a fixed list of
targeted edits (each must match the expected number of times or the build stops),
and writes site/public_html/index.html. Nothing here touches the live site.

Usage: python3 -I tools/build_v1.py <repo_root>
"""
import sys, pathlib, hashlib

root = pathlib.Path(sys.argv[1])
src = (root / "original/index-oct9-artifact.html").read_text(encoding="utf-8")

# ---- 1. Strip the Claude-artifact preview wrapper and build a real document ----
body_start = src.index("<body>") + len("<body>")
inner = src[body_start:]
ribbon = '<div class="preview-ribbon" role="note">Stadium preview · Oct 9 build · not live</div>\n'
assert inner.count(ribbon) == 1, "preview ribbon not found exactly once"
head_part, body_part = inner.split(ribbon)
assert body_part.rstrip().endswith("</body></html>")
body_part = body_part.rstrip()[: -len("</body></html>")]
head_part = head_part.replace("<title>THEBRIANWARNER Stadium</title>",
                              "<title>THEBRIANWARNER™ | Welcome to the Stadium</title>", 1)

doc = (
    '<!doctype html>\n<html lang="en" class="no-js">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="THEBRIANWARNER™. An operating system for pressure. '
    'Teaching by proximity through championship conversation.">\n'
    '<!-- THEBRIANWARNER.com Version 1.0 candidate. Built from the Oct 9, 2026 Stadium build. '
    'See UPDATE-GUIDE.md before editing. -->\n'
    + head_part.strip() + "\n</head>\n<body>\n" + body_part.strip() + "\n</body>\n</html>\n"
)

# ---- 2. Targeted fixes. (old, new, expected count) ----
EDITS = [
    # Million Dollar Opportunity is a workshop/product, not a media show (QB1, Sept 19 + Oct 9)
    ('<span><b>5</b> shows</span>', '<span><b>4</b> shows</span>', 1),
    ('<p>Five shows live Inside the Booth.', '<p>Four shows live Inside the Booth.', 1),
    ('<li>Million Dollar Opportunity · Sixty Seconds Go</li>', '<li>Sixty Seconds Go</li>', 1),
    ('<p class="lead">Five shows. One continuous', '<p class="lead">Four shows. One continuous', 1),
    ('<article class="show"><span class="room-name">Inside the Booth</span><h3>Million Dollar Opportunity</h3>'
     '<p>Episodes and show details coming to this page.</p></article>', '', 1),

    # "Live Cast" retired as listener-facing term (QB1, Sept 18/19)
    ('Live Cast &amp; mentoring podcast', 'Mentoring podcast', 3),

    # "Championship Ladder" is not a QB1-established feature (Oct 9 directive): hold it off the field,
    # code kept intact so QB1 can restore it by removing the hidden attribute.
    ('<section class="band" id="ladder" aria-labelledby="ladder-h">',
     '<!-- HELD FOR QB1: "Championship Ladder" not an approved feature (Oct 9). Remove hidden to restore. -->\n'
     '<section class="band" id="ladder" aria-labelledby="ladder-h" hidden data-hold="qb1">', 1),
    ('<p class="lead">The mentoring operation at the top of the ladder. Where',
     '<p class="lead">The flagship mentoring operation. Where', 1),
    ('    <h2>Climb the ladder.</h2>\n', '', 1),
    ('<p class="lead">Most people start with the shows or one Championship Conversation, then try the coaching at Saturday School.</p>',
     '<p class="lead">Start with the shows or one Championship Conversation, then try the coaching at Saturday School.</p>', 1),
    ('<a class="btn arrow" href="#ladder" data-home-anchor>See the Championship Ladder</a>',
     '<a class="btn arrow" href="#championship-conversation">Championship Conversation</a>', 1),

    # No claims of active service where nothing is running yet
    ('<h1>Saturday School is in session.</h1>', '<h1>Saturday School.</h1>', 1),
    ('>Save my seat</a>', '>Get on the list</a>', 2),
    ('<h4>Field Pass</h4><p>Premium membership: coaching, courses, Mini Camp, downloads, workbooks and exclusive episodes.</p>',
     '<h4>Field Pass</h4><p>Premium membership: coaching, courses, Mini Camp, downloads, workbooks and exclusive episodes.</p>'
     '<span class="status status-soon">Not open yet</span>', 1),
    ('<div class="btn-row"><a class="btn btn-gold arrow" href="#connect">Request training</a></div>\n</div></section>',
     '<div class="btn-row"><span class="status status-dev">In development</span>'
     '<a class="btn btn-gold arrow" href="#connect">Request training</a></div>\n</div></section>', 1),
    ('<option value="team-store">Team Store order</option>', '<option value="team-store">Team Store</option>', 1),
    ('msg.value = "Team Store request: " + q.get("product") + "\\nSize:\\nQuantity:\\nShip to (city/state):\\n";',
     'msg.value = "Team Store interest: " + q.get("product") + "\\n";', 1),

    # Million Dollar Opportunity destination in the institutional booking layer (facts from QB1 Sept 19 ruling only)
    ('<option value="speaking">Speaking / Keynote</option>',
     '<option value="speaking">Speaking / Keynote</option>\n'
     '        <option value="million-dollar-opportunity">Million Dollar Opportunity workshop</option>', 1),
    ('    <div class="btn-row"><a class="btn arrow" href="#connect">Book Brian</a></div>\n  </div>\n</div></section>\n',
     '    <div class="btn-row"><a class="btn arrow" href="#connect">Book Brian</a></div>\n  </div>\n</div></section>\n\n'
     '<!-- CONTENT: Million Dollar Opportunity. Workshop/product, not media (QB1 Sept 19). Copy beyond these facts = SOURCE NEEDED. -->\n'
     '<section class="band" id="million-dollar-opportunity"><div class="wrap stack">\n'
     '  <p class="eyebrow"><b>WORKSHOP</b> · Million Dollar Opportunity</p>\n'
     '  <h2>Million Dollar Opportunity.</h2>\n'
     '  <p class="lead">A workshop Brian delivers for schools and institutions. First up: Mississippi junior and community colleges and Mississippi high schools.</p>\n'
     '  <div class="btn-row"><span class="status status-dev">Workshop details coming</span>'
     '<a class="btn arrow" href="#connect">Ask about the workshop</a></div>\n'
     '</div></section>\n', 1),

    # Layout: 1px sideways scroll on 320px phones (pre-existing in Oct 9 build)
    ('.steps li { background: var(--night); padding: 1.25rem 1.4rem; display: grid; grid-template-columns: 4.5rem 1fr; gap: 1rem; }',
     '.steps li { background: var(--night); padding: 1.25rem 1.4rem; display: grid; grid-template-columns: 4.5rem minmax(0, 1fr); gap: 1rem; min-width: 0; }\n'
     '.steps { grid-template-columns: minmax(0, 1fr); }', 1),

    # One obvious place to set the contact inbox
    ('<form id="connect-form" class="form" data-email="" novalidate>',
     '<!-- SETTING: contact inbox. Put QB1-approved address in data-email. Blank = form shows "inbox not set". -->\n'
     '  <form id="connect-form" class="form" data-email="" novalidate>', 1),
]

for old, new, n in EDITS:
    c = doc.count(old)
    assert c == n, f"expected {n} match(es), found {c}: {old[:80]!r}"
    doc = doc.replace(old, new)

assert "Live Cast" not in doc
assert "preview-ribbon\" role" not in doc
out = root / "site/public_html/index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(doc, encoding="utf-8")
print("wrote", out, len(doc.encode()), "bytes sha256", hashlib.sha256(doc.encode()).hexdigest())
