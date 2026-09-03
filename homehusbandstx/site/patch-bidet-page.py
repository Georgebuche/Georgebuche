#!/usr/bin/env python3
"""
Patches bidet-installation-houston/index.html in place.

Run from your site folder:   python3 patch-bidet-page.py

Six edits. The embedded product images are never touched.
"""
import io, os, sys, shutil, glob

# The page may live either as a folder with an index.html inside, or as a
# single .html file at the root that Netlify's Pretty URLs serves at the same
# address. Check the usual spots, then fall back to searching for it.
CANDIDATES = [
    os.path.join("bidet-installation-houston", "index.html"),
    "bidet-installation-houston.html",
    os.path.join("bidet-installation-houston", "bidet-installation-houston.html"),
]

def find_page():
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
    for path in glob.glob("**/*.html", recursive=True):
        try:
            with io.open(path, encoding="utf-8") as f:
                head = f.read(4000)
        except (UnicodeDecodeError, OSError):
            continue
        if "bidet-installation-houston/" in head and "NEO 120" in head:
            return path
    return None

EDITS = [
    # 1. Remove the "Licensed, insured" claim — Texas issues no general handyman
    #    licence, and your own homepage says so. The two contradict each other.
    ('no trip fee, no surprises. Licensed, insured, and usually booked within the week.',
     'no trip fee, no surprises. Flat rate, and usually booked within the week.'),

    # 2 & 3. Dallas metro removed.
    ('professional install across the Houston &amp; Dallas metros',
     'professional install across the Houston metro'),
    ('<div class="area">Houston &amp; Dallas metros</div>',
     '<div class="area">Houston metro</div>'),

    # 4. Netlify needs these attributes to register the form at build time.
    ("<form id='bookingForm' method='POST' name='install-request' novalidate>",
     '<form id="bookingForm" method="POST" name="install-request" '
     'data-netlify="true" netlify-honeypot="bot-field" novalidate>'),

    # 5. Remove the unattributed 5-star / 16,400 review block. Presented on your
    #    service page it reads as reviews of HomeHusbandsTx. See the notes.
    ('''      <div class="rating">
        <span class="stars">★★★★★</span>
        <span class="count">(16,400 reviews)</span>
      </div>

''', ''),

    # 6. Logo linked to a #top anchor that does not exist on this page.
    ('<a class="logo" href="#top" aria-label="HomeHusbandsTX home">',
     '<a class="logo" href="/" aria-label="HomeHusbandsTX home">'),
]

def main():
    PATH = find_page()
    if PATH is None:
        sys.exit(
            "Can't find the bidet page. Run this from your site folder — the one\n"
            "holding index.html. Looked for:\n  " + "\n  ".join(CANDIDATES) +
            "\nIf it is somewhere else, tell me the exact filename and I'll adjust."
        )
    print("Patching %s" % PATH)

    with io.open(PATH, encoding="utf-8") as f:
        html = f.read()

    shutil.copy(PATH, PATH + ".backup")

    applied, missing = 0, []
    for i, (old, new) in enumerate(EDITS, 1):
        if old in html:
            html = html.replace(old, new, 1)
            applied += 1
        else:
            missing.append(i)

    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print("Applied %d of %d edits." % (applied, len(EDITS)))
    if missing:
        print("Edits not found (already applied, or the text differs): %s"
              % ", ".join(str(m) for m in missing))
    print("Original saved as %s.backup" % PATH)

    remaining = sum(html.lower().count(w) for w in
                    ("dallas", "plano", "frisco", "mckinney", "arlington", "irving"))
    print("DFW references remaining: %d" % remaining)

if __name__ == "__main__":
    main()
