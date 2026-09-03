#!/usr/bin/env python3
"""
Patches bidet-installation-houston/index.html in place.

Run from your site folder:   python3 patch-bidet-page.py

Six edits. The embedded product images are never touched.
"""
import io, os, sys, shutil

PATH = os.path.join("bidet-installation-houston", "index.html")

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
    if not os.path.exists(PATH):
        sys.exit("Can't find %s — run this from the folder that holds index.html "
                 "and the bidet-installation-houston folder." % PATH)

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
