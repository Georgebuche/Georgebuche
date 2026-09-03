# AI Search Visibility — Playbook for George's Sites

**Created:** September 3, 2026
**Owner:** George Onwubuche
**Scope:** piecesbyheart.com, 247aitech.com, homehusbandstx.com, postfanatics.com, wadewatson.com, gussla.com

---

## 0. The one-paragraph version

Getting cited by ChatGPT, Claude, Perplexity and Google AI Overviews is **two jobs, not one.**
Job A is making your pages readable by a crawler that does not run JavaScript and is not
logged in. Job B is being *talked about somewhere else* — Reddit, YouTube, Google Business
Profile, Yelp, BBB, local press. Job A is a prerequisite; Job B is where the citations
actually come from. Most of your sites currently fail Job A for structural reasons, and
none of them have started Job B.

---

## 1. Where each site actually stands

Pulled from the Hostinger account on Sept 3, 2026. I could not fetch the sites from this
session (egress blocked), so the "risk" column is inferred from platform type — verify with
the commands in Section 6.

| Domain | Platform | State | Primary AI-visibility risk |
|---|---|---|---|
| **piecesbyheart.com** | Shopify (`utycgb-x2`) + a retired WordPress still on Hostinger | Domain **not connected in Shopify** | **Invisible.** Nothing to crawl. See §2. |
| **247aitech.com** | Hostinger Horizons | Live | JS-rendered shell — crawlers may see an empty page |
| **postfanatics.com** | Hostinger Horizons | Live | Same |
| **wadewatson.com** | Hostinger Horizons | Live | Same |
| **homehusbandstx.com** | Hostinger, type `other` | Live | Local business — needs the **listings** path, not the on-page path |
| **gussla.com** | Domain registered, **no website in the hosting account** | Parked | Nothing exists |

Two of the six are not sites yet. Fix that before optimizing anything.

---

## 2. Pieces by Heart — do not start here

AI search optimization for piecesbyheart.com right now is wasted effort. Per the handoff
(§8, trap 4), the domain was never added in Shopify → Settings → Domains, so the storefront
is unreachable. A crawler that cannot resolve your store cannot cite it. The store also has
zero products.

**Prerequisites before any of this playbook applies:** publish the Custom Photo Puzzle,
connect the domain in Shopify admin. Those are already open items 1 and 4 in the handoff.

**One thing worth fixing now, though:** the stray `AAAA @` record still pointing at
`2a02:4780:b:748:0:3880:2618:5`. Several AI crawlers run on IPv6-capable infrastructure.
Any of them that prefer IPv6 will land on the **retired WordPress install**, index that as
"what piecesbyheart.com is," and cache it. That is worse than being invisible — it is being
visible as the wrong thing. The handoff already recommends deleting this record and lists it
as pending your approval. This is the argument for approving it.

---

## 3. Job A — be readable by a machine

### 3.1 The JavaScript problem (your biggest issue)

Googlebot renders JavaScript. **Most AI crawlers do not.** GPTBot, ClaudeBot, PerplexityBot
and OAI-SearchBot fetch raw HTML and read what is in it. If your text arrives via a JS bundle
after page load, they see an empty container.

Hostinger's own Horizons documentation says a published project is "ready to be indexed by
search engines **that support JavaScript-rendered content**." That caveat is the whole
problem — it is a precise description of Googlebot and a precise description of what AI
crawlers are not.

This affects **247aitech.com, postfanatics.com and wadewatson.com.**

Test it yourself (§6.1). If the raw HTML has no headings and no body copy, you have three
options, in order of preference:

1. **Use Horizons' SEO settings to put real content in the served HTML** — title, meta
   description, and any per-page text fields it exposes. This is the cheap fix and may be
   enough for simple one-page sites.
2. **Rebuild the ones that matter as static HTML.** For a marketing site of 3–8 pages this is
   a day of work and permanently solves crawlability, speed, and portability. Hostinger
   serves static files fine — `homehusbandstx.com` is already a non-Horizons site on the
   same account.
3. **Prerendering** (Prerender.io and similar) — serves crawlers a snapshot. Adds a monthly
   cost and a dependency. Only worth it if you have many pages.

For a portfolio this size, option 2 on your one or two highest-value sites beats option 3
everywhere.

### 3.2 Don't block the crawlers

Two separate gates, and passing one does not pass the other:

**Gate 1 — robots.txt.** Know the difference between *training* crawlers and *search/retrieval*
crawlers. Blocking training does not protect you and does cost you nothing; blocking retrieval
removes you from citations entirely.

| User-agent | What it does | Recommendation |
|---|---|---|
| `OAI-SearchBot` | Indexes for ChatGPT search results | **Allow** — this is the citation path |
| `ChatGPT-User` | Live fetch when a user's question needs your page | **Allow** |
| `GPTBot` | OpenAI model training | Your call — no citation impact |
| `Claude-SearchBot` / `Claude-User` | Claude retrieval and live fetch | **Allow** |
| `ClaudeBot` | Anthropic crawling | Allow |
| `PerplexityBot` / `Perplexity-User` | Perplexity index and live fetch | **Allow** |
| `Googlebot` | Feeds Google Search *and* AI Overviews | **Allow — never block** |
| `Google-Extended` | Gemini grounding / training | Allowing helps Gemini; blocking does **not** remove you from AI Overviews |
| `Bingbot` | Bing index — ChatGPT leans on Bing for business/local answers | **Allow — matters more than people think** |
| `Applebot` / `Applebot-Extended` | Apple Intelligence / Siri | Allow |

Default posture: allow everything. You are trying to be found, not trying to protect a
content moat.

**Gate 2 — host-level bot protection.** This is the one that silently breaks things.
Hostinger's WAF/bot filtering and Shopify's bot protection can return 403 to an AI crawler
even when your robots.txt says "Allow." A permissive robots.txt is not proof you are
reachable. Verify by fetching with the crawler's user-agent and checking the status code
(§6.2).

### 3.3 Structured data (JSON-LD)

Machine-readable facts. It is not magic, but it is how an assistant states your price, hours,
and phone number with confidence instead of hedging.

- **Every site:** `Organization` — name, url, logo, sameAs (links to your social profiles),
  contactPoint.
- **homehusbandstx.com:** `LocalBusiness` — exact name, address, phone, geo, `areaServed`
  (Tomball and the surrounding towns you actually serve), `openingHours`, `priceRange`.
- **piecesbyheart.com:** `Product` with `offers` (price, currency, availability) and
  `AggregateRating` once you have reviews. Most Shopify themes emit Product and Breadcrumb
  markup already — check yours rather than adding a duplicate. Add `Organization` and
  `FAQPage` yourself.
- **Anywhere you answer questions:** `FAQPage`.

Validate at [validator.schema.org](https://validator.schema.org/) and Google's Rich Results
Test.

### 3.4 Write in a shape that extracts cleanly

AI Overviews pull heavily from opening content. The pattern that gets extracted:

- **H2 phrased as the question a person actually asks** — "How much does a custom photo puzzle
  cost?" not "Pricing."
- **The answer in the first two or three sentences**, complete and standalone. Assume it will
  be lifted out of context, because it will be.
- **Then** the elaboration, the story, the persuasion.
- Specific numbers, named places, dated facts. "$39 for the 110-piece, 10×8″" is quotable.
  "Affordable pricing" is not.
- One clear topic per page. Pages that try to cover everything get cited for nothing.

### 3.5 Freshness

Perplexity in particular weights recency hard — content under 30 days old draws
substantially more citations. Put visible dates on pages, and update your two or three most
important pages on a real schedule rather than publishing a lot once and going quiet.

### 3.6 llms.txt — skip it

Short version: it does not work yet. Adoption sits around 10% of sites, but of roughly 500
million AI bot visits measured over 90 days, **408** requested `/llms.txt`. Google has said
publicly it does not support it and has no plans to. Anthropic and Perplexity do consult it
in some retrieval flows, so it is not worthless — just not a lever.

Horizons generates one automatically. Fine. Do not spend an hour on it, and do not let a
vendor sell you an "llms.txt strategy."

---

## 4. Job B — off-site is where citations come from

This is the part people skip, and it is the larger half.

The concentration is extreme. Across ChatGPT, Claude, Gemini, Perplexity and AI Overviews, a
handful of sources — Wikipedia, Reddit, YouTube, LinkedIn, Forbes — account for roughly
two-thirds of all citations. Wikipedia alone is near half of ChatGPT's sources. And only
about 38% of AI Overview citations now come from pages ranking in Google's top 10, down from
76% in mid-2025. **Ranking on page one is no longer the path.** Being discussed is.

What that means concretely for a small operator:

- **Reddit.** Participate as yourself in the subreddits where your buyers already are
  (r/gifts, r/HomeImprovement, r/smallbusiness, local Houston/Tomball subs). Answer questions
  genuinely. Do not drop links — that gets removed and does nothing. Getting *named* in a
  thread is the asset.
- **YouTube.** A two-minute "here's the puzzle arriving and being assembled" video is both a
  citation source and your missing listing photography.
- **Get mentioned in third-party writing.** Local press, niche gift/POD roundups, industry
  blogs, podcast appearances. One mention in a source AI already trusts outperforms fifty
  pages on your own site.
- **Consistency across sources.** Assistants check for agreement between independent sources
  before naming a business. Your name, address and phone must be **byte-identical**
  everywhere.

### 4.1 HomeHusbands TX specifically — this is a listings game

For local service businesses the on-page work barely moves the needle. AI assistants answer
"handyman near Tomball TX" from listings and reviews, not from your homepage.

Only about 1.2% of business locations get recommended by ChatGPT versus 35.9% appearing in
Google's local 3-pack — local AI visibility is roughly 30× harder, and almost entirely won on
these:

1. **Google Business Profile** — complete, every field, service list, service area, photos,
   Q&A section filled in yourself.
2. **Bing Places** — ChatGPT's local answers lean on Bing. Most competitors skip this. Do it.
3. **Yelp**, **Better Business Bureau**, **Apple Maps Connect**, **Foursquare** — ChatGPT
   pulls business recommendations from exactly these.
4. **Reviews on more than one platform.** A 4.3★ average across three platforms beats 5.0★ on
   one. Ask every customer, name the platform.
5. **NAP identical everywhere.** `1-281-624-6402` on one listing and `(281) 624-6402` on
   another is fine for humans and reduces model confidence. Pick one format and enforce it.

---

## 5. What to actually do, in order

**Now, this week:**
1. Approve deleting the stray `AAAA` record on piecesbyheart.com (§2). Small, real, prevents
   the dead WordPress site being indexed as your store.
2. Run the §6 audit on 247aitech.com, postfanatics.com, wadewatson.com and homehusbandstx.com.
   Ten minutes. It tells you whether you have a JS problem, a robots problem, or a bot-blocking
   problem — those need different fixes and you should not guess.
3. **HomeHusbands: claim Google Business Profile and Bing Places.** Highest return of anything
   on this page, costs nothing, no code.

**Next, once the audit is back:**
4. Fix whichever gate is failing on the Horizons sites — content into served HTML, or a static
   rebuild of the one site that matters most commercially.
5. Add `Organization` JSON-LD everywhere; `LocalBusiness` on HomeHusbands.
6. Rewrite the top page of each live site to the answer-first shape in §3.4.

**After Pieces by Heart launches (not before):**
7. Connect the domain in Shopify, confirm the store returns real HTML to a crawler.
8. Product schema check, FAQ page ("How do I upload my photo?", "What size puzzle should I
   pick?", "How long does shipping take?") — these are literally the questions buyers type
   into ChatGPT.
9. YouTube unboxing/assembly video using the physical sample from handoff open item 3.

**Ongoing:**
10. Reddit and YouTube presence. Slow, compounding, and the actual source of citations.
11. Monthly check (§6.3).

**Decide about gussla.com.** It is a renewing domain with nothing on it. Either build
something or let it lapse — an empty domain has no visibility to improve.

---

## 6. Audit commands — run these from your own machine

My session cannot reach your domains; yours can.

### 6.1 Is your content in the raw HTML?

```bash
for d in 247aitech.com postfanatics.com wadewatson.com homehusbandstx.com; do
  echo "=== $d"
  curl -sL "https://$d/" -o /tmp/$d.html
  echo "bytes:    $(wc -c < /tmp/$d.html)"
  echo "h1/h2:    $(grep -oic '<h[12]' /tmp/$d.html)"
  echo "json-ld:  $(grep -c 'application/ld+json' /tmp/$d.html)"
  echo "title:    $(grep -oim1 '<title>[^<]*' /tmp/$d.html)"
  echo "text len: $(sed -e 's/<script[^>]*>.*<\/script>//g' /tmp/$d.html | sed -e 's/<[^>]*>//g' | tr -s ' \n' ' ' | wc -c)"
done
```

**Reading it:** fewer than ~2 headings and under ~1500 characters of text means the page is a
JavaScript shell. AI crawlers see nothing. That is the §3.1 problem.

### 6.2 Are the AI crawlers actually being served?

```bash
for ua in "GPTBot/1.2" "OAI-SearchBot/1.0" "ClaudeBot/1.0" "PerplexityBot/1.0" "Mozilla/5.0 (compatible; bingbot/2.0)"; do
  for d in 247aitech.com homehusbandstx.com; do
    printf "%-45s %-22s %s\n" "$ua" "$d" "$(curl -s -A "$ua" -o /dev/null -w '%{http_code}' -L "https://$d/")"
  done
done
```

**Reading it:** anything that is not `200` — especially `403` or `429` — means host-level bot
protection is blocking that crawler regardless of robots.txt. That is the §3.2 Gate 2 problem,
and it is invisible from a normal browser.

Also just read each robots.txt: `curl -s https://247aitech.com/robots.txt`

### 6.3 Monthly visibility check

There is no reliable rank tracker for AI answers. The honest method is to ask, and write it
down.

Keep a fixed list of ten buyer-shaped prompts and run them in ChatGPT, Claude, Perplexity and
Google AI Mode on the same day each month:

- "best custom photo puzzle to make from my own picture"
- "where can I get a jigsaw puzzle printed from a photo"
- "handyman services in Tomball TX"
- "reliable home repair near Tomball Texas"
- …six more matched to 247AITech / Post Fanatics / Wade Watson

Record: were you named, were you linked, what got cited instead. The competitors that *do*
appear are your roadmap — look at what those pages have that yours do not.

Server-side, grep your Hostinger access logs for crawler visits — this is the ground truth on
whether anyone is reading you at all:

```bash
grep -Ei 'GPTBot|OAI-SearchBot|ClaudeBot|Claude-User|PerplexityBot|Google-Extended|Applebot' access.log | awk '{print $1, $12}' | sort | uniq -c | sort -rn | head -20
```

---

## 7. What not to spend money on

- **"GEO / AEO optimization" retainers.** The work is in this document. It is listings,
  crawlable HTML, schema, and off-site presence.
- **llms.txt services.** See §3.6.
- **AI-visibility rank-tracking SaaS**, at your stage. §6.3 costs nothing and tells you the
  same thing when you have six sites, not six hundred.
- **Bulk AI-written content.** Volume without distinctiveness does not get cited. One page
  that answers a real question precisely beats forty that answer nothing.
- **Prerendering subscriptions** before you have confirmed via §6.1 that you actually have a
  rendering problem on a site with enough pages to justify it.

---

## Sources

- [How to Get Cited by AI Search Engines — GEO Playbook, Frase](https://www.frase.io/blog/how-to-get-cited-by-ai-search-engines-the-complete-geo-playbook)
- [AI Platform Citation Patterns 2026](https://www.gptmelo.com/resources/ai-platform-citation-patterns-2026)
- [AI Platform Citation Source Index 2026](https://everything-pr.com/ai-platform-citation-source-index-2026)
- [llms.txt in 2026: Hype, Data, and What to Do Instead](https://www.wikibusines.net/blog/llms-txt-ai-crawler-guide)
- [State of llms.txt 2026](https://presenc.ai/research/state-of-llms-txt-2026)
- [Robots.txt & AI Crawlers in 2026](https://dataimpulse.com/blog/robots-txt-ai-crawlers/)
- [Hostinger Horizons: How to Index Your Web App](https://www.hostinger.com/support/10946162-hostinger-horizons-how-to-index-your-web-app/)
- [Hostinger Horizons: SEO Settings](https://www.hostinger.com/support/10771376-hostinger-horizons-seo-settings/)
- [How to Optimize SPAs for Crawling and Indexing, Prerender.io](https://prerender.io/blog/how-to-optimize-single-page-applications-spas-for-crawling-and-indexing/)
- [How Local Businesses Show Up in ChatGPT and AI Search (2026)](https://twentyonesolutions.com/resources/local-businesses-show-up-in-chatgpt-ai-search-guide)
- [AI Search Visibility for Local Service Businesses, PushLeads](https://pushleads.com/ai-search-visibility-for-local-service-businesses-why-your-google-page-one-rankings-mean-nothing-if-chatgpt-has-never-heard-of-you/)
- [How AI Uses Reviews and Listings to Recommend Local Businesses](https://greenbananaseo.com/how-ai-uses-reviews-and-listings-to-recommend-local-businesses-article-and-video-59/)
