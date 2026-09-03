# HomeHusbandsTX — SEO Audit & Action Plan

**Version:** 1
**Prepared:** September 3, 2026
**Owner:** George Onwubuche (Tomball, TX)
**Domain:** homehusbandstx.com (Hostinger registrar, active, expires 2027-06-22)
**Purpose:** Diagnose why the site has no search presence and give a ranked, executable plan to fix it.

---

## 1. Headline finding

**The site currently has no measurable organic search presence.** A `site:homehusbandstx.com`
query returns nothing, and a branded search for "Home Husbands TX" surfaces competitors
(Mr. Handyman, Handyman Connection, Rent A Husband) but never this business.

This is **not** a "tune the title tags" problem. Nothing is ranking because — as far as the
public index is concerned — the site is not there. The work below is ordered accordingly:
indexation and local presence first, on-page refinement second, content last.

**Also important:** for a home-services business in the Houston metro, the Google Business
Profile drives more booked jobs than the website does. The map pack sits above the organic
results for every "handyman near me" style query. Section 4 is the highest-revenue section
in this document; do it even if nothing else gets done.

---

## 2. What was verified, and what wasn't

Verified directly against the Hostinger account and public search results:

| Fact | Source |
|---|---|
| Domain active, registered 2026-06-22, expires 2027-06-22 | Hostinger domain list |
| Live site is served from **Netlify**, not Hostinger | DNS zone (below) |
| A Hostinger hosting account still exists for the domain | Hostinger website list (`u947922456`) |
| Apex has a **conflicting IPv6 record** | DNS zone (below) |
| Zero indexed pages, zero branded results | `site:` and brand searches |

**Not verified — the site's own HTML could not be read from this environment.** Outbound
requests to `homehusbandstx.com` and `homehusbandstx.netlify.app` are refused by the network
egress proxy (HTTP 403, organization policy). The Hostinger file API also returns 500/422 for
this domain, consistent with the real site living on Netlify and the Hostinger document root
being empty or absent.

So the following are **unassessed** and need a pass once access exists: current title tags and
meta descriptions, heading structure, word count, image alt text, page speed / Core Web
Vitals, existing schema markup, and whether a `robots.txt` or `sitemap.xml` is present at all.
Sections 5 and 6 give the templates to apply; they were written to be correct regardless of
what is currently there.

---

## 3. Technical foundation — fix first

### 3.1 The apex IPv6 record is pointing at the wrong server ⚠️ HIGH

Current apex records:

```
A     @   75.2.60.5                              → Netlify
AAAA  @   2a02:4780:b:748:0:3880:2618:3          → Hostinger shared hosting
CNAME www homehusbandstx.netlify.app.            → Netlify
```

The IPv4 apex goes to Netlify. The IPv6 apex goes to Hostinger. These are two different
servers serving one hostname.

Why this matters for SEO specifically: Google crawls dual-stack and **prefers IPv6 when a
AAAA record exists**. If Googlebot resolves `homehusbandstx.com` over IPv6, it is talking to
the Hostinger box, not the Netlify site — where it will get an empty document root, a parking
page, or a TLS certificate that does not cover this domain. Any of those is sufficient on its
own to keep the site out of the index, and it would explain the total absence of results in
Section 1.

**Fix: delete the `AAAA @` record.** Netlify does not publish stable AAAA addresses for apex
domains, so there is no correct IPv6 value to substitute — removing it makes every client
fall back to the IPv4 record, which is correct. Nothing about email is affected: MX, SPF,
DKIM and DMARC are separate records and stay untouched.

This is the same class of bug already documented on piecesbyheart.com, which carries a stray
`AAAA @` at `2a02:4780:b:748:0:3880:2618:5` — the adjacent address in the same Hostinger
block. Both domains were pointed away from Hostinger and both kept the orphaned IPv6 record.

> **Status: approved by George, attempted, blocked by a tooling limit. Needs 30 seconds in
> hPanel.**
>
> Three safe routes were tried through the Hostinger connector, and the record is still live:
>
> | Attempt | Result |
> |---|---|
> | Update the `AAAA` RRset with an empty record list | Rejected, HTTP 422 |
> | Set the record to `is_disabled: true` | Accepted, but not honoured — record unchanged |
> | Resubmit the full zone minus the `AAAA`, `overwrite=true` | No-op — `overwrite` is per-RRset, so unlisted records survive |
>
> The connector's delete endpoint exposes only a `domain` parameter and no record filter, so
> calling it would target the entire zone — including the MX, SPF and DKIM records carrying
> `@homehusbandstx.com` email. That was not attempted.
>
> **The zone was verified intact after every attempt. Nothing was changed or lost.**
>
> **Do this manually instead — hPanel → Domains → homehusbandstx.com → DNS / Nameservers.**
> Find the row of type `AAAA`, name `@`, pointing at `2a02:4780:b:748:0:3880:2618:3`, and
> delete that row only. Leave `A @ 75.2.60.5` exactly as it is. Propagation is 5 minutes at
> the current 300s TTL, and a DNS snapshot from earlier today exists as a restore point if
> anything looks wrong.

### 3.2 Pick one canonical hostname

Both `homehusbandstx.com` and `www.homehusbandstx.com` currently resolve. If both serve the
site with a 200, every page exists at two URLs and whatever authority the site earns is split
between them.

Choose one — apex (`homehusbandstx.com`) is the better default here since it is shorter, it
is what will be printed on a truck magnet or a business card, and Netlify handles it fine.
Then 301 the other to it. On Netlify, set the apex as the primary domain in
**Site settings → Domain management**; Netlify issues the redirect automatically. Verify
afterward that `www` returns `301`, not `200`.

### 3.3 robots.txt

Serve at `/robots.txt`. Paste-ready:

```
User-agent: *
Allow: /

Sitemap: https://homehusbandstx.com/sitemap.xml
```

The thing to actually check is that a stray `Disallow: /` is not already being served — that
single line would fully explain zero indexation, and it is a common leftover from a staging
deploy. Check this before assuming anything else in Section 3 is the cause.

### 3.4 sitemap.xml

Serve at `/sitemap.xml`. One `<url>` block per real page:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://homehusbandstx.com/</loc><priority>1.0</priority></url>
  <url><loc>https://homehusbandstx.com/services/</loc><priority>0.8</priority></url>
  <url><loc>https://homehusbandstx.com/about/</loc><priority>0.5</priority></url>
  <url><loc>https://homehusbandstx.com/contact/</loc><priority>0.8</priority></url>
</urlset>
```

Do not list URLs that 301 or 404 — a sitemap full of redirects is a negative quality signal.

### 3.5 Get the site into the index

None of the above matters until Google is told the site exists.

1. **Google Search Console** — add a *Domain* property (`homehusbandstx.com`), which covers
   apex, www and every subdomain in one. Verify with a DNS TXT record at Hostinger.
2. Submit the sitemap.
3. Use **URL Inspection → Request Indexing** on the homepage. This is the fastest path from
   "invisible" to "in the index" and often works within days.
4. Check **Pages → Why pages aren't indexed** after a week. That report will name the actual
   cause — "Discovered – currently not indexed", "Redirect error", "Server error (5xx)" — and
   a 5xx there would confirm the IPv6 diagnosis in 3.1.
5. **Bing Webmaster Tools** — import directly from Search Console, about two minutes. Bing
   also feeds ChatGPT and Copilot results, which increasingly matter for local intent.

---

## 4. Google Business Profile — the highest-ROI work

For "handyman near me", "handyman Tomball TX" and every similar query, Google shows a map
pack of three local businesses above the organic results. Entry to that pack is governed by
the Google Business Profile, not the website. A business with a strong profile and a thin
website consistently outbooks the reverse.

**Setup checklist:**

- **Claim and verify** the profile at business.google.com. Verification is by video or
  postcard and is the long pole — start it today, everything else can proceed in parallel.
- **Service-area business.** If the business runs out of a home, hide the street address and
  define a service area instead. Listing a residential address publicly is both a privacy
  problem and a ranking liability.
- **Primary category** is the single strongest ranking lever in the profile. Pick the one that
  matches the core money service exactly — `Handyman` for general repair work. Add secondary
  categories for anything genuinely offered.
- **Services list** — enumerate every service individually with a short description each.
  These become matchable terms.
- **Photos.** Real job photos, before/after pairs, the truck, the owner. Geotagging is a myth,
  but volume and recency are not. Add a few every month.
- **Hours**, including holiday hours. Add a booking or call link.
- **Q&A** — seed it by asking and answering the five questions customers actually ask
  (pricing, service area, licensing, emergency availability, payment methods).

**Reviews are the compounding asset.** Ask every single customer, in person, at the moment the
job is finished and they are happy — that is the only moment with a high conversion rate. Send
a short link by text. Respond to every review, positive and negative; response rate is itself
a signal and negative reviews handled well convert readers better than a wall of five stars.

**Citations — same NAP everywhere.** Write the business name, address and phone once, in one
exact string, and reuse it character-for-character. Inconsistent NAP is the most common reason
local rankings stall.

Priority order: Apple Business Connect, Bing Places, Facebook, Nextdoor (heavily used for home
services in Houston suburbs), Yelp, Angi, Thumbtack, HomeAdvisor, BBB, and the Tomball and
Houston-area chambers of commerce.

---

## 5. On-page templates

### 5.1 Title tags and meta descriptions

Titles: put the money keyword first, the city second, the brand last. Keep under ~60
characters so they don't truncate.

| Page | Title | Meta description |
|---|---|---|
| Home | `Handyman Services in Tomball & NW Houston \| Home Husbands TX` | `Trusted local handyman for repairs, installs and honest home fixes across Tomball, Spring and NW Houston. Free estimates — call (XXX) XXX-XXXX.` |
| Service | `[Service] in [City], TX \| Home Husbands TX` | `Professional [service] in [city]. Upfront pricing, clean work, done right the first time. Call for a free estimate.` |
| City | `Handyman in [City], TX \| Home Husbands TX` | `Local handyman serving [city] and nearby. Repairs, mounting, drywall, doors and more. Same-week appointments available.` |
| Contact | `Contact Home Husbands TX \| Free Estimates` | `Call, text or request a quote online. Serving [cities]. Fast response, no obligation.` |

Every page needs a **unique** title and description. Duplicates across pages are a common and
easily avoided drag.

### 5.2 Page structure

- Exactly one `<h1>` per page, containing the service and the city.
- Phone number in the header as a `tel:` link — on mobile that is the primary conversion, and
  a non-clickable phone number is a real revenue leak.
- A call to action above the fold, and again at the bottom.
- Descriptive `alt` text on every image.
- Real photos of real jobs. Stock photography reads as untrustworthy in this category and
  hurts conversion measurably.

### 5.3 Service and city pages

Local sites rank on the strength of one page per service, and one page per city, rather than
a single homepage that lists everything.

**The trap:** generating twenty near-identical city pages with the name swapped is a doorway
page pattern, and Google demotes it. If a city page cannot carry genuinely distinct content —
a real job done there, a neighborhood referenced, a local specific — do not create it. Three
substantial city pages beat twenty templated ones.

Start with the cities where work is actually taken: Tomball, Spring, Magnolia, Cypress, The
Woodlands, Klein.

### 5.4 Structured data

Add once, in the `<head>` of the homepage. Replace every bracketed value with the real one —
the phone and the geo coordinates in particular must match the Google Business Profile exactly.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Home Husbands TX",
  "url": "https://homehusbandstx.com",
  "telephone": "[+1-XXX-XXX-XXXX]",
  "email": "[info@homehusbandstx.com]",
  "priceRange": "$$",
  "image": "https://homehusbandstx.com/[logo.png]",
  "areaServed": [
    { "@type": "City", "name": "Tomball", "address": { "@type": "PostalAddress", "addressRegion": "TX" } },
    { "@type": "City", "name": "Spring",  "address": { "@type": "PostalAddress", "addressRegion": "TX" } },
    { "@type": "City", "name": "Magnolia","address": { "@type": "PostalAddress", "addressRegion": "TX" } },
    { "@type": "City", "name": "Cypress", "address": { "@type": "PostalAddress", "addressRegion": "TX" } }
  ],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "18:00"
  }],
  "sameAs": [
    "[https://www.facebook.com/...]",
    "[https://www.google.com/maps/place/...]"
  ]
}
</script>
```

Use `HomeAndConstructionBusiness` rather than the generic `LocalBusiness` — it is the more
specific type and describes this business correctly. If the address is not public, omit
`address` entirely rather than supplying a partial one. Validate at
`search.google.com/test/rich-results` before shipping.

---

## 6. Content — after the foundation is live

Content is last on purpose. Publishing articles onto a site that is not indexed and has no
Google Business Profile is wasted effort.

Once Sections 3 and 4 are done, the queries worth writing for are the ones with buying intent
or seasonal urgency, which in this market means:

- Texas freeze prep — pipe insulation, outdoor faucet covers. Publish in October, not January.
- Storm and hurricane season prep and post-storm repair. Publish in May.
- "How much does a handyman cost in Houston" — high volume, high intent, and a page that
  answers it honestly earns trust and links.
- Homeowner-vs-pro guides for the services actually sold. These rank and they pre-qualify
  callers.

One genuinely useful page per month beats a burst of thin ones.

---

## 7. Measurement

| Tool | What it answers | Cadence |
|---|---|---|
| Google Search Console | Is it indexed, what queries surface it, what is broken | Weekly at first |
| Google Business Profile Insights | Calls, direction requests, map views | Monthly |
| GA4 | Traffic and conversions | Monthly |
| Manual local search | Where the business sits in the map pack | Monthly |

The one metric that matters in month one is **indexed page count in Search Console**. Until it
is above zero, nothing else is measurable.

---

## 8. Execution order

**This week**
1. Delete the apex `AAAA` record — **manual, 30 seconds in hPanel** (Section 3.1)
2. Start Google Business Profile claim and verification (Section 4)
3. Verify Search Console, submit sitemap, request indexing (Section 3.5)
4. Confirm `robots.txt` is not blocking crawlers (Section 3.3)

**Next two weeks**
5. Set the canonical hostname and confirm the 301 (Section 3.2)
6. Complete the GBP profile — categories, services, photos, hours
7. Apply title tags, meta descriptions and schema (Section 5)
8. Build the top NAP citations (Section 4)

**Month two onward**
9. Service pages, then city pages where there is real content to put on them
10. Review generation as an ongoing habit, not a campaign
11. First seasonal content piece

---

## 9. Open questions

1. **Site access.** The Netlify site is not connected to either GitHub repo on this account,
   and outbound access to the domain is blocked from this environment. To apply Sections 3 and
   5 directly rather than handing over snippets: is the Netlify site deployed from a repo that
   can be added, or is it drag-and-drop? Pushing the source into a repo would also make every
   future change reviewable.
2. **Confirm the service list and service area.** The plan assumes general handyman and home
   repair across the Tomball / NW Houston corridor, inferred from the business name and
   location. The exact money services and the real list of cities drive every keyword target
   in Sections 5 and 6.
3. **NAP string.** The exact business name, public phone, and business email to use — needed
   before any citation or schema work, since the whole point is that it never varies.
4. **Google Business Profile status.** Does one already exist, claimed or unclaimed? An
   unclaimed auto-generated profile is common and changes the first step from "create" to
   "claim".
5. **Confirm the apex `AAAA` deletion once done** (Section 3.1) — approved, but the
   Hostinger connector cannot delete a single record, so it needs a manual click in hPanel.
   Worth re-requesting indexing in Search Console immediately afterward.
