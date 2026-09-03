# HomeHusbandsTx — AI & Google Search Audit

**Date:** September 3, 2026 · **Site:** homehusbandstx.com (built on Netlify) · **Phone:** (281) 624-6402 · **Email:** support@homehusbandstx.com

> Audited from the live homepage source. The four draft pages previously in this folder were written before I had seen the real site and were **wrong on services, prices, service area and positioning**. They have been deleted. Do not restore them.

---

## What the site already gets right

Worth stating plainly, because most of this is the hard part and it's done:

- **Static, server-rendered HTML.** Every AI crawler reads it directly. This is the single biggest advantage over the Horizons sites (247aitech, postfanatics, wadewatson), which are JavaScript shells.
- **A rich, valid JSON-LD `@graph`** — `HomeAndConstructionBusiness` + `LocalBusiness`, `WebSite`, and a full `FAQPage` with 8 questions. Real prices in `hasOfferCatalog`. This is better structured data than most local competitors have.
- **Answer-first FAQ copy.** "Do you use poison or chemicals?" → "No — our critter proofing is completely chemical-free." That's exactly the shape AI Overviews extract.
- **A genuinely quotable hook.** *"A gap the size of a dime is all a mouse needs."* Specific, memorable, factual. That sentence will get lifted.
- **The honesty section is a real asset.** Stated limits — no structural pest control license needed for chemical-free work, no general handyman license in Texas, detector work scoped as replace-and-test not inspection, attic check is a homeowner's look not a licensed inspection. Stated scope reads as expertise to both humans and models, and it is the kind of paragraph that gets quoted rather than summarized.
- **Published prices everywhere.** $149 / $89 bidet, $199 quarterly, $716 prepaid, $99 dryer vent, $89 filter, $49 drain flush, $49 detectors, $450–$1,500 critter range. Priced, specific and comparable — the opposite of "free estimates".

---

## P0 — DNS repointed to Netlify (Sept 3, 2026) — one step outstanding

**Done and verified** via the Hostinger API on Sept 3:

| Record | Was | Now |
|---|---|---|
| `A @` | `185.212.71.189` (Hostinger) | `75.2.60.5` (Netlify apex) ✅ |
| `CNAME www` | `homehusbandstx.com.` | `homehusbandstx.netlify.app.` ✅ |
| `AAAA @` | `2a02:4780:b:748:0:3880:2618:3` | **still Hostinger — must be deleted manually** ❌ |

TTL on all three lowered to 300 so a rollback propagates in five minutes.

**Email was not touched and is intact:** `MX` (mx1/mx2.hostinger.com), SPF `TXT`,
`_dmarc`, all three `hostingermail-*._domainkey` DKIM records, `autodiscover` and
`autoconfig`. `support@homehusbandstx.com` was unaffected throughout.

**The outstanding step.** The `AAAA @` record still resolves to Hostinger, so the
domain is currently split: IPv4 visitors reach Netlify, IPv6 visitors reach the old
Hostinger content. This is the same split-brain fault already documented on
piecesbyheart.com.

It could not be removed through the API. Hostinger's delete-records endpoint as
exposed here takes only a domain with no per-record filter, so calling it risked
deleting the entire zone including the mail records; and setting `is_disabled: true`
on the record was accepted by the API but not honoured (the TTL change applied, the
disable did not).

**Fix in hPanel:** Domains → homehusbandstx.com → DNS / Nameservers → find the
`AAAA` record with name `@` → Delete. Do not touch anything else in that zone.

Rollback if needed: DNS snapshots exist on this zone (most recent
`158727118`, "Hostinger mail activated", 2026-06-22), and the pre-change values are
in the table above.

## P1 — The Dallas claim is actively costing you Houston rankings

The site claims **Houston and Dallas metros**: `areaServed` lists Plano, Frisco, McKinney, Arlington, Irving and Dallas alongside the Houston-area towns, and the footer repeats it.

Tomball to Plano is roughly **250 miles, about four hours each way.** From one address, with one phone number, this is a problem on three fronts:

1. **Google Business Profile won't support it.** A service-area business is expected to cover the area it can actually drive to. You cannot legitimately set DFW service areas on a Tomball-verified profile; ranking in Dallas requires a second location with a DFW address and a local number.
2. **It dilutes the Houston signal.** Local relevance is proximity-weighted. Claiming thirteen cities across two metros makes you weakly associated with all of them instead of strongly associated with Tomball, Spring, Cypress and Magnolia — where you can actually win.
3. **AI assistants cross-check service area against address.** A single-location business claiming a metro four hours away is a low-confidence signal, and low confidence means not getting named. Consistency across sources is the thing these systems weigh most heavily for local recommendations.

**Recommendation: cut Dallas.** Remove the six DFW cities from `areaServed`, the footer and the "Houston & Dallas metros" line in the title, meta description and hero eyebrow. Concentrate everything on the Houston metro. Add Dallas back when there is a real DFW crew, a DFW address and a second GBP — at which point it should be its own location profile, not a wider claim on this one.

If you genuinely do serve DFW today, tell me and I'll restructure it properly as a two-location business instead — that's a different, legitimate schema shape (`Organization` with two `LocalBusiness` branches), not a wider `areaServed` array.

---

## P2 — Critter proofing is your flagship and it does not have a page

This is the biggest missed opportunity on the site.

Right now the entire site is **one page with anchors** (`#critter`, `#services`, `#plan`, `#faq`), plus `/bidet-installation-houston/`. Anchors do not get cited independently. An assistant answering *"chemical-free rodent exclusion near Cypress TX"* needs a page about that, at its own URL, with its own `Service` and `FAQPage` schema. It cannot cite `homehusbandstx.com/#critter` as the answer to a critter question and `homehusbandstx.com/#services` as the answer to a dryer vent question — it's one URL, and it gets treated as one topic.

The bidet page proves you already know this. Do the same for the rest, in this order:

| Page | Why this order |
|---|---|
| `/critter-proofing/` | Flagship service, highest value job ($450–$1,500), strongest differentiator, currently only an anchor |
| `/dryer-vent-cleaning/` | High search volume, strong safety intent ("dryer vent cleaning near me" is a real query with real volume) |
| `/ac-drain-line-flush/` | Seasonal spike, urgent intent, and the $49 price is a standout |
| `/quarterly-home-maintenance-plan/` | Highest lifetime value, and the $199-vs-$286 comparison is exactly the kind of concrete claim that gets quoted |

Each page: the price and the direct answer in the first two sentences, then the detail. Own `Service` + `Offer` + `FAQPage` schema. Keep the homepage as the hub that links to all of them.

**Note the ordering change from what I built earlier.** I led with bidet installation because that's what you listed first. Your own site is right and I was wrong — critter proofing is the flagship, and the chemical-free angle is a much stronger differentiator than a bidet price. "Chemical-free rodent exclusion, no poison, no monthly contract" is a position almost nobody else in the Houston metro is claiming, and it directly answers a question homeowners actually ask.

---

## P3 — City pages, once the service pages exist

`areaServed` names the towns, but naming a city in schema is not the same as having content about it. For "critter proofing Tomball TX" and "dryer vent cleaning Cypress" you need pages that talk about those places specifically — local housing stock, common entry points in that area's construction, what you've actually sealed there.

Do the top four Houston-metro towns only, and only after P2. Thin, templated city pages that differ by a find-and-replace are worse than not having them.

---

## P4 — Technical gaps

- [ ] **`robots.txt`** — confirm one exists and explicitly allows `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-SearchBot`, `PerplexityBot`, `Google-Extended`, `Applebot` and `bingbot`. On Netlify it goes in the publish directory.
- [ ] **`sitemap.xml`** — confirm one exists and lists every real page. Submit to Google Search Console and Bing Webmaster Tools.
- [ ] **`sameAs`** in the business schema — add the GBP, Facebook, Nextdoor and Yelp URLs as they get created. This is how a model confirms the website and the listing are the same business.
- [ ] **`priceRange: "$$"`** is vague when you publish real numbers. Consider `"$49-$1500"`.
- [ ] **`AggregateRating`** — add once you have real reviews. Never fabricate it; Google penalizes invented review markup and it is trivially detectable.
- [ ] **Confirm `og-image.png`, `favicon.ico` and `apple-touch-icon.png` are actually deployed** — they're referenced absolutely at `homehusbandstx.com`, which currently resolves to Hostinger (see P0).
- [ ] **The `.rv` reveal pattern** sets `opacity:0` and only reveals via IntersectionObserver. Text is in the HTML so AI crawlers are fine, but content hidden by default is a small unnecessary risk and it means link previews and thumbnails can capture a blank page. Safer: animate from a visible resting state.

---

## P5 — Off-site, which is still the larger half

The site is now in good shape technically. **Citations come from elsewhere.** For local service businesses, AI assistants answer from listings and reviews, not from your homepage:

1. **Google Business Profile** — Tomball, service-area business, address hidden. Primary category `Handyman`. Add every service with its price and description; that text gets read. Video verification the day you create it.
2. **Bing Places** — ChatGPT leans on Bing for local answers and most competitors skip it. Imports from GBP.
3. **Nextdoor Business** — where Tomball homeowners actually ask for recommendations. Fastest route to real jobs this week.
4. **Yelp, BBB, Apple Business Connect** — named repeatedly as ChatGPT sources for local businesses.

NAP identical everywhere: **HomeHusbandsTx** / **(281) 624-6402** / **support@homehusbandstx.com**. Note the site uses `HomeHusbandsTx` and `HOMEHUSBANDSTX` — pick one written form for listings and never vary it.

Reviews: a 4.3★ average across three platforms beats 5.0★ on one. Ask every customer the day the job is done, name the platform, send the direct link.

---

## Timeline, honestly

Nothing here makes you rank on Google this week. A site takes weeks to months; AI citation takes longer. What moves **this week** is fixing P0, claiming GBP and Bing Places, and posting on Nextdoor. Everything else compounds — which is the reason to start now, not the reason to expect fast results.
