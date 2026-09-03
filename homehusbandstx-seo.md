# HomehusbandsTx — SEO Audit & Action Plan

**Version:** 2 — supersedes v1 (Sept 3, 2026)
**Updated:** September 3, 2026
**Owner:** George Onwubuche (Tomball, TX)
**Domain:** homehusbandstx.com (Hostinger registrar, active, expires 2027-06-22)

**What changed in v2:** the real service list arrived, and it invalidates the v1 strategy.
This is not a general handyman business. It is three specific services, and that is a
materially better position than v1 assumed. Sections 4–7 are rewritten. Section 3 is unchanged
and still blocking.

---

## 1. Headline finding

**The site still has no measurable organic search presence.** `site:homehusbandstx.com` returns
nothing. Nothing ranks because, as far as the public index is concerned, the site is not there.

**But the competitive picture is much better than v1 assumed.** v1 planned around "handyman
Houston" — a franchise battleground against Mr. Handyman, Handyman Connection and Ace Handyman,
with budgets a small operator cannot match. Your actual services are not in that fight:

- **Bidet installation** has almost no local competition and near-100% transactional intent.
  It is the cheapest win available to you.
- **Critter proofing** is a real, seasonal, high-intent local category with modest competition.
- **Quarterly home maintenance** is recurring revenue, and its individual components have far
  more search demand than the plan itself does.

Stop thinking of this as "a handyman site that needs SEO". It is three niche service
businesses that each need a page, and one of them is nearly uncontested.

---

## 2. Status board

| Item | Status |
|---|---|
| Google Business Profile | ✅ Claimed |
| Bing Places | ✅ Linked |
| Domain active and healthy | ✅ Verified |
| Site served from Netlify | ✅ Verified — deployed by drag-and-drop, not from a repo |
| Apex `AAAA` record conflict | ❌ **Still live. Top priority.** (Section 3.1) |
| Google Search Console | ❌ Not confirmed set up |
| Indexed pages | ❌ Zero |
| Service pages | ❌ None — Section 5 defines them |
| GBP categories tuned to real services | ❌ Almost certainly wrong — Section 4 |
| NAP string | ✅ Defined — ⚠️ phone shared with Pieces by Heart, see 4.7 |

**Still not assessed:** the site's own HTML. Outbound access to `homehusbandstx.com` and the
Netlify origin is refused by this environment's egress proxy (HTTP 403, organisation policy).
So current title tags, headings, word count, alt text, page speed and existing schema remain
unseen. Everything below is written to be correct regardless of what is there now.

---

## 3. Technical foundation — unchanged from v1, still blocking

### 3.1 The apex IPv6 record points at the wrong server ⚠️ DO THIS FIRST

```
A     @    75.2.60.5                       → Netlify   (the real site)
AAAA  @    2a02:4780:b:748:0:3880:2618:3   → Hostinger (empty)
CNAME www  homehusbandstx.netlify.app.     → Netlify
```

Google crawls dual-stack and **prefers IPv6 when a AAAA record exists**. Googlebot is likely
resolving to the empty Hostinger box rather than your Netlify site. That alone is sufficient to
explain zero indexation.

**Fix:** hPanel → Domains → homehusbandstx.com → DNS. Delete the single row of type `AAAA`,
name `@`, value `2a02:4780:b:748:0:3880:2618:3`. Leave `A @ 75.2.60.5` alone. Email is
unaffected — MX, SPF, DKIM and DMARC are separate records. Propagation is ~5 minutes at the
current 300s TTL, and a DNS snapshot exists as a restore point.

> This was approved and attempted through the Hostinger connector. Three safe routes were
> tried — empty record list (rejected, 422), `is_disabled: true` (accepted but not honoured),
> and a full-zone resubmit minus the AAAA (no-op, since `overwrite` is per-RRset). The
> connector's delete endpoint exposes only a `domain` parameter with no record filter, so
> calling it would target the whole zone including your email records. Not attempted. **The
> zone was verified intact after every attempt.** It needs one manual click.

### 3.2 Canonical hostname

Both apex and `www` resolve. Set the apex as primary in Netlify → Domain management; Netlify
issues the 301. Confirm `www` returns `301`, not `200`.

### 3.3 robots.txt

```
User-agent: *
Allow: /

Sitemap: https://homehusbandstx.com/sitemap.xml
```

Check first that a stray `Disallow: /` is not already being served — that one line would
independently explain zero indexation, and it is a common leftover from a staging deploy.

### 3.4 Search Console — the missing piece

GBP and Bing Places are done; Search Console is the gap. Add a **Domain** property, verify by
DNS TXT at Hostinger, submit the sitemap, then URL Inspection → Request Indexing on the
homepage. After a week, read **Pages → Why pages aren't indexed** — a *Server error (5xx)*
there confirms the 3.1 diagnosis.

---

## 4. Google Business Profile — retune it for the real services

The profile is claimed, which means the hard part is done. But it was almost certainly set up
generically, and **the primary category is the single strongest ranking lever in local search.**
Getting it wrong costs more than anything else on this list.

### 4.1 Categories

**Primary: `Handyman`.** It is the broadest match to the quarterly maintenance plan and bidet
installation, and it is the category that customer searches for those jobs actually trigger. In
Tomball the handyman map pack is genuinely winnable — the franchise problem is a Houston-proper
problem, not a Tomball one.

**Secondaries, in priority order:**

| Category | Covers | Check first |
|---|---|---|
| `Pest control service` | Critter proofing | ⚠️ Licensing — see 4.2 |
| `Plumber` | Bidet installation | ⚠️ Licensing — see 4.2 |
| `Air duct cleaning service` | Dryer vent clearing | Fits cleanly |
| `Property maintenance` / `Building maintenance` | Quarterly plan | Pick whichever GBP offers |

Category names differ slightly by market and Google revises the list — pick the closest match
from what your dashboard actually offers rather than forcing these strings. Set the primary
once and leave it; churning it resets your standing.

### 4.2 ⚠️ Two licensing questions to settle before claiming categories

Not legal advice — but both are worth confirming before you put them on a public profile:

- **Plumbing.** Texas regulates plumbing through the Texas State Board of Plumbing Examiners.
  Attaching a bidet seat to an existing supply line via a T-valve is generally treated as an
  appliance install, not plumbing work. A full fixture install involving new supply or drain
  lines is a different matter. Claiming the `Plumber` category without a licence is a real
  exposure — verify where your work falls before selecting it.
- **Pest control.** Structural pest control in Texas is licensed by the Texas Department of
  Agriculture. Sealing entry points with no pesticide application and no animal handling
  generally sits outside that. Trapping or relocating wildlife is separate again and may need a
  Texas Parks & Wildlife permit. Confirm before selecting `Pest control service`.

If either is unresolved, leave the category off and rank that page organically instead. An
organic ranking is slower than the map pack but carries none of this risk.

### 4.3 Services list

Enter all three headline services, and **enter the six maintenance components individually**.
Each becomes a separately matchable term, and the components are what people actually search:

```
Critter proofing
Bidet installation
Quarterly home maintenance plan
  → AC filter change
  → AC condensate drain line flush
  → Dryer vent cleaning
  → Smoke detector testing and battery replacement
  → Garbage disposal reset and inspection
  → Attic inspection (insulation, moisture, pest signs)
```

### 4.4 Service area

List the six confirmed cities: **Houston, Tomball, Spring, The Woodlands, Sugar Land, Cypress.**
Google allows up to 20, but padding the list dilutes relevance rather than extending reach.
Note that the pin's location — not the list — drives map-pack placement (see 5.4).

### 4.5 Reviews

Ask every customer in person the moment the job is finished and they're happy. That is the only
moment with a high conversion rate; send the link by text while you're still there. Respond to
every review. **The quarterly plan is a review machine** — four touchpoints a year per customer
instead of one. Ask on the second visit, once they've seen you show up as promised.

### 4.6 NAP

Business name **HomehusbandsTx**. Whatever exact string is on the Google Business Profile is
canonical — copy it character-for-character everywhere else, including capitalisation.
Inconsistent NAP is the most common reason local rankings stall.

**The master NAP string — use this exact text everywhere:**

```
HomehusbandsTx
(281) 624-6402
support@homehusbandstx.com
https://homehusbandstx.com
```

Display format `(281) 624-6402`; schema and `tel:` links use `+12816246402`. Whatever string
sits on the Google Business Profile wins if it differs — go and match it rather than changing
the profile, since the profile is the entity Google trusts.

### 4.7 ⚠️ The phone number is shared with Pieces by Heart

`281-624-6402` is also recorded as the business phone for **piecesbyheart.com** (see
`piecesbyheart-handoff.md` §2). Two distinct businesses publishing one phone number is a real
local SEO problem, not a cosmetic one.

Google treats the phone number as a primary identity signal for a business entity. When the
same number appears under two different names, in two different categories, across directory
citations, Google's options are to merge the entities, distrust one, or suppress both. Local
listings have been demoted for exactly this.

**Right now the exposure is low** — Pieces by Heart has no Google Business Profile, hasn't
launched, and isn't cited anywhere. So nothing is being damaged today.

**It becomes a real problem the moment either of these happens:**
- Pieces by Heart publishes the number on its live site, or
- a Google Business Profile is ever created for Pieces by Heart with that number

**Recommendation: HomehusbandsTx keeps this number; Pieces by Heart gets a different one.**
HomehusbandsTx is the local business — it is the one that lives or dies by the map pack, and
the number is already tied to its profile. Pieces by Heart is e-commerce with a national
audience, no service area and no need for a local phone identity, so it is the cheaper side to
change — and it should change before launch rather than after citations exist.

**Do not put `281-624-6402` on the Pieces by Heart storefront or in any Pieces by Heart
directory listing.** That is a launch item for that project, not this one, and worth carrying
back into the Pieces by Heart handoff.

---

## 5. Site architecture and keyword map

### 5.1 The core insight

**The maintenance plan's components have far more search demand than the plan itself.**

Nobody wakes up and searches "quarterly home maintenance plan". They search "dryer vent
cleaning near me" because their clothes take two cycles to dry, or "AC drain line clogged"
because there's water on the floor. Those are urgent, high-volume, high-intent queries.

So: **rank for the component problems individually, then convert those callers onto the
quarterly plan.** The plan is the upsell, not the entry point. That single reframe is worth more
than every title tag in this document.

### 5.2 Page map

| Page | Primary target | Volume | Competition | Priority |
|---|---|---|---|---|
| `/bidet-installation/` | bidet installation houston / near me | Low | **Almost none** | **1st** |
| `/critter-proofing/` | rodent proofing, wildlife exclusion + city | Moderate | Low–moderate | **2nd** |
| `/dryer-vent-cleaning/` | dryer vent cleaning + city | **Good** | Moderate | **3rd** |
| `/ac-drain-line-flush/` | ac condensate drain line clogged / flush | Good, seasonal | Low | 4th |
| `/quarterly-home-maintenance/` | home maintenance plan houston | Low | Low | 5th |
| `/attic-inspection/` | attic inspection, attic insulation check | Moderate | Moderate | 6th |
| Home | brand + Greater Houston | — | — | Alongside |

**Build in that order.** Bidet first because it is the closest thing to a free win on this
list, and an early ranking gives the whole domain a signal to build on.

### 5.3 Two things to get right per page

**Critter proofing: keep the brand name, but carry the search terms.** "Critter proofing" is
warm and on-brand, and it is *not* what people type. They type *rat proofing house*, *rodent
exclusion*, *squirrel in attic*, *seal entry points*, *animal removal*. Use "critter proofing"
as the H1 and brand language, then make sure the body copy genuinely uses the terms people
search — naturally, in real sentences, not stuffed.

**Bidet installation is uncontested — take it metro-wide.** Almost no local competitor has a
page for this. The searcher has just bought a bidet, opened the box, and found they need a
T-valve and possibly a nearby GFCI outlet for a heated seat. That is a person who will call the
first credible result. One good page can own this term across all six cities.

### 5.4 City pages — later, and fewer than you'd think

Your six cities are not equally winnable:

| City | Competition | Realistic outcome | Build |
|---|---|---|---|
| **Tomball** | Low | Map pack + organic | First |
| **Spring** | Moderate | Map pack + organic | Second |
| **Cypress** | Moderate | Map pack + organic | Third |
| **The Woodlands** | Moderate–high | Organic; map pack possible | Fourth |
| **Sugar Land** | Moderate | **Organic only** | Fifth |
| **Houston** | Very high | Long-term, via submarkets | Last |

**Sugar Land cannot win the map pack.** It is ~45 miles southwest of Tomball, on the far side
of Houston. Local pack placement is driven by proximity between searcher and business pin, so a
northwest pin will essentially never surface there. Sugar Land is an organic-only target — and
check the drive time is economic before chasing small jobs across the metro.

**The service pages come first.** A ranking service page serving six cities beats six thin city
pages serving none. Generating near-identical city pages with the name swapped is a doorway
pattern and Google demotes it — if a city page can't carry genuinely distinct content, don't
create it.

**URL pattern:** `/critter-proofing/tomball-tx/` once you get there. Consistency matters more
than which pattern you choose; changing later costs redirects.

---

## 6. Page copy — paste-ready

Written for conversion, not for keyword density. Adjust the voice to match how you actually
talk to customers.

### 6.1 Bidet installation

**Title:** `Bidet Installation in Houston & Tomball, TX | HomehusbandsTx` *(58 chars)*
**Meta:** `Bought a bidet and need it installed right? We handle the T-valve, the fit and the leak test — usually in under an hour. Serving Houston, Tomball, Spring, The Woodlands, Sugar Land and Cypress.`
**H1:** `Bidet Installation, Done Right the First Time`

> You bought the bidet. Now there's a box on the bathroom floor, a bag of fittings, and an
> instruction sheet that assumes you own a basin wrench.
>
> We install bidet seats and attachments across the Houston area — usually in under an hour.
> We shut off the supply, fit the T-valve, mount and level the seat, and pressure-test every
> connection before we leave. No drips, no "keep an eye on it for a few days."
>
> **What we handle**
> - Bidet seats, attachments and standalone units
> - T-valve and supply line fitting
> - Levelling and secure mounting on standard and elongated bowls
> - Full leak test before we leave
> - Heated and electric models — we'll tell you honestly before we start whether your outlet
>   situation works, rather than after
>
> **Before you book:** electric and heated seats need a grounded outlet within reach of the
> cord. If your bathroom doesn't have one near the toilet, tell us when you call and we'll
> talk you through the options instead of turning up and shrugging.
>
> **[Call (281) 624-6402]** — or send a photo of your toilet and the box, and we'll confirm
> it's a straightforward job before anyone commits.

### 6.2 Critter proofing

**Title:** `Critter Proofing & Rodent Exclusion | Houston & Tomball, TX` *(58 chars)*
**Meta:** `Seal the ways in and the problem stops coming back. Full-home exclusion for rats, mice and squirrels across Houston, Tomball, Spring, The Woodlands, Sugar Land and Cypress.`
**H1:** `Critter Proofing — Seal the Ways In, Not Just the One You Found`

> Trapping the rat you heard last night doesn't fix anything. Another one uses the same gap
> next week. Rodent problems are entry-point problems, and until the entry points are sealed
> you're just managing symptoms.
>
> We do full-home exclusion: find every way in, seal it properly, and make it stay sealed.
>
> **Where they actually get in**
> - Roofline gaps, soffit returns and fascia joints
> - Dryer and bathroom vent terminations with failed or missing covers
> - Weep holes, foundation gaps and utility penetrations
> - Garage door corner seals — the single most common one we find
> - Attic gable vents and ridge vent edges
>
> **How we work.** We inspect the full exterior and the attic, show you the photos of what we
> found, and seal with materials rodents can't chew through — steel mesh, hardware cloth and
> sealant, not expanding foam on its own. Then we tell you what we saw in the attic:
> insulation condition, moisture, and any droppings or nesting.
>
> **Timing matters in Houston.** Rodents move indoors when nights start cooling — late October
> through December is when most people first hear something overhead. Sealing in September
> beats sealing in December.
>
> **[Call (281) 624-6402]** for an exterior and attic inspection.

### 6.3 Quarterly home maintenance

**Title:** `Quarterly Home Maintenance Plan | Houston & Tomball, TX` *(54 chars)*
**Meta:** `Four visits a year. AC drain line, dryer vent, smoke detectors, disposal and attic — checked before they become emergencies. Serving the greater Houston area.`
**H1:** `The Quarterly Home Maintenance Plan`

> Most home emergencies are maintenance that got skipped. A clogged AC condensate line floods a
> ceiling in August. A packed dryer vent is a fire risk long before it's an inconvenience. A
> smoke detector chirps at 3am because nobody changed the battery in two years.
>
> We come four times a year and handle the things that quietly go wrong.
>
> **Every visit**
> - **AC filter changed** — the right size, actually replaced, not just looked at
> - **AC condensate drain line flushed** — the number one cause of summer ceiling damage in
>   Houston
> - **Dryer vent cleared end to end** — not just the lint trap; the full run to the exterior
>   vent
> - **Smoke detectors tested, batteries replaced** — every unit, every visit
> - **Garbage disposal reset and checked**
> - **Attic inspected** — insulation condition, moisture, and any sign of pests
>
> **Why quarterly.** Houston runs the AC most of the year, humidity keeps condensate lines
> working hard, and attic problems are cheap to fix early and expensive to fix late. Four
> visits catches the seasonal stuff in the season it matters.
>
> **You get a written summary after every visit** — what we checked, what we found, what needs
> watching. No upsell theatre.
>
> **[Call (281) 624-6402]** to start the plan.

### 6.4 Remaining pages — headlines only

| Page | Title | H1 |
|---|---|---|
| Dryer vent | `Dryer Vent Cleaning in Houston & Tomball, TX \| HomehusbandsTx` | `Dryer Vent Cleaning — Cleared End to End` |
| AC drain line | `AC Drain Line Flush & Unclog \| Houston & Tomball, TX` | `Clogged AC Drain Line? We'll Flush It Today` |
| Attic inspection | `Attic Inspection — Insulation, Moisture & Pests \| Houston, TX` | `What's Actually Going On in Your Attic` |
| Home | `Home Maintenance & Repair in Greater Houston \| HomehusbandsTx` | `Critter Proofing, Bidet Installs and Quarterly Home Maintenance` |

Every page needs a unique title and meta. One `<h1>` per page. Phone number in the header as a
`tel:` link — on mobile that is the primary conversion, and a non-clickable number is a real
revenue leak. Real photos of real jobs; stock imagery measurably hurts conversion here.

---

## 7. Structured data

Paste in the homepage `<head>`. Replace bracketed values. Phone must match the GBP exactly.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "HomehusbandsTx",
  "url": "https://homehusbandstx.com",
  "telephone": "+1-281-624-6402",
  "email": "support@homehusbandstx.com",
  "priceRange": "$$",
  "image": "https://homehusbandstx.com/[logo.png]",
  "areaServed": [
    { "@type": "City", "name": "Houston",       "address": {"@type":"PostalAddress","addressRegion":"TX"} },
    { "@type": "City", "name": "Tomball",       "address": {"@type":"PostalAddress","addressRegion":"TX"} },
    { "@type": "City", "name": "Spring",        "address": {"@type":"PostalAddress","addressRegion":"TX"} },
    { "@type": "City", "name": "The Woodlands", "address": {"@type":"PostalAddress","addressRegion":"TX"} },
    { "@type": "City", "name": "Sugar Land",    "address": {"@type":"PostalAddress","addressRegion":"TX"} },
    { "@type": "City", "name": "Cypress",       "address": {"@type":"PostalAddress","addressRegion":"TX"} }
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Critter Proofing",
        "description": "Full-home rodent and wildlife exclusion — entry point sealing, roofline, vents and foundation gaps." } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Bidet Installation",
        "description": "Bidet seat and attachment installation including T-valve fitting and leak testing." } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Quarterly Home Maintenance",
        "description": "Four visits a year: AC filter change, condensate drain line flush, dryer vent clearing, smoke detector testing, garbage disposal check and attic inspection." } }
    ]
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "18:00"
  }],
  "sameAs": ["[Google Maps URL]", "[Facebook URL]"]
}
</script>
```

Use `HomeAndConstructionBusiness`, not the generic `LocalBusiness` — it is the more specific
type. If the address isn't public, omit `address` rather than supplying a partial one. Validate
at `search.google.com/test/rich-results` before shipping.

Add `FAQPage` schema to each service page once the copy is live — pricing, timing and
"do I need to be home" are the three questions worth marking up.

---

## 8. Seasonal calendar — Houston-specific

Publishing the right page in the wrong month wastes it. Ranking takes weeks, so publish ahead
of demand, not into it.

| Publish | Page / content | Why |
|---|---|---|
| **September** | Critter proofing | Rodents move indoors as nights cool, Oct–Dec |
| **October** | Freeze prep — pipe insulation, faucet covers | Ahead of the January freeze panic |
| **November** | Dryer vent cleaning | Heavier dryer use through winter |
| **April–May** | AC drain line flush | Ahead of the summer condensate season |
| **May** | Storm and hurricane prep | Season opens June 1 |
| **Year-round** | Bidet installation | No seasonality — publish first, it's the easiest win |

---

## 9. Measurement

| Tool | What it answers | Cadence |
|---|---|---|
| Google Search Console | Is it indexed, what queries surface it, what's broken | Weekly at first |
| GBP Insights | Calls, direction requests, map views | Monthly |
| GA4 | Traffic and conversions | Monthly |
| Manual local search | Map pack position, per city | Monthly |

Month one, the only metric that matters is **indexed page count**. Until it is above zero,
nothing else is measurable.

---

## 10. Execution order

**This week**
1. **Delete the apex `AAAA` record** (3.1) — one click, and the most likely single cause of
   zero indexation
2. **Search Console** — verify, submit sitemap, request indexing (3.4)
3. **Confirm `robots.txt` isn't blocking crawlers** (3.3)
4. **Retune the GBP categories and services list** (4.1, 4.3) — settle the two licensing
   questions in 4.2 first

**Next two weeks**
5. Canonical hostname and 301 (3.2)
6. Publish `/bidet-installation/` — the easiest win on the board (6.1)
7. Publish `/critter-proofing/` — in September, ahead of the season (6.2)
8. Homepage title, meta and schema (6.4, 7)
9. NAP citations: Apple Business Connect, Facebook, Nextdoor, Yelp, Angi, Thumbtack,
   HomeAdvisor, BBB, Tomball chamber

**Month two onward**
10. `/quarterly-home-maintenance/`, then dryer vent and AC drain line
11. Review generation as a habit — use the plan's four annual touchpoints
12. City pages, starting with Tomball, only where there's real content to put on them

---

## 11. Open items

1. **The apex `AAAA` deletion** (3.1) — approved, needs one manual click in hPanel. Re-request
   indexing in Search Console straight afterward.
2. ~~Phone number and business email~~ — **answered and applied throughout: (281) 624-6402,
   support@homehusbandstx.com.** One item remains: confirm the Google Business Profile carries
   this exact number, and that its name string matches character-for-character.
   **New, from 4.7: decide which venture keeps this number.** It is currently shared with
   Pieces by Heart.
3. **The two licensing questions** in 4.2, before selecting the `Plumber` or
   `Pest control service` GBP categories.
4. **Deployment.** Netlify is drag-and-drop, not connected to a repo. That means every change
   is manual, nothing is reviewable, and there's no rollback. **Recommend connecting Netlify to
   a GitHub repo** — Netlify then rebuilds on push, and the site becomes something that can be
   changed properly. If you want this, say so and the repo gets scaffolded; the site's current
   files would need exporting from Netlify first.
5. **Current site HTML** still unseen (egress-blocked). Either connect the repo per item 4, or
   paste the existing homepage `<head>` and I'll fold the changes into what's actually there
   rather than handing over generic blocks.
