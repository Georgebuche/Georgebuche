# Pieces by Heart — Project Handoff

**Version:** 2 — supersedes the Sept 2 handoff
**Updated:** September 3, 2026
**Owner:** George Onwubuche (Tomball, TX)
**Purpose:** Bring a fresh assistant fully up to speed on piecesbyheart.com without re-deriving history or reopening settled decisions.

---

## 1. Read this first

1. **The store is still empty.** Zero products, zero customers, no custom collections. Infrastructure is wired; nothing was ever published.
2. **The one thing that unblocks everything** is publishing the Custom Photo Puzzle from Customily to Shopify. Listings, email, promos and marketing all depend on it existing.
3. **Section 6 decisions are closed.** Do not reopen them.
4. **Pricing and variants are now finalized** (Section 4). They changed on Sept 3 — the old 120/252/500 plan was wrong.

**Live working documents:**
- Customily publish runbook — https://claude.ai/code/artifact/ba341327-38b7-40e2-90ba-b9b449ead77e
- Printify-native evaluation (CLOSED, do not action) — https://claude.ai/code/artifact/487281ac-2fde-4597-9761-a1d95bb9a85f

---

## 2. Business overview

**Pieces by Heart** sells custom photo jigsaw puzzles — customer uploads a photo, it prints as a puzzle and ships. Fully automated print-on-demand, no manual fulfillment steps.

- **Domain:** piecesbyheart.com (registered at Hostinger, active, expires 2027-05-19)
- **Business email:** info@piecesbyheart.com — standalone Hostinger mailbox, not Google
- **Phone:** 1-281-624-6402
- **Audience waiting:** 256+ email subscribers, growing. This is why launch speed matters.

George runs other ventures (HomeHusbandsTx, 247AITECH, Unitson Insurance, Gussla). Keep assets and accounts separate.

---

## 3. Architecture

```
Customer uploads photo on piecesbyheart.com (Shopify)
        ↓
Customily renders preview + builds the print file
        ↓
Printify receives it via API → produces → ships
        ↓
Tracking syncs back to Shopify
```

| Layer | Tool | Status |
|---|---|---|
| Storefront | Shopify — `utycgb-x2.myshopify.com` | Live, empty |
| Payments | Shopify Payments | Activated July, unverified since |
| Personalization | Customily | Installed, integrated, **required** |
| Fulfillment | Printify | Connected |
| Domain / DNS / email | Hostinger | Pointed at Shopify |
| Email marketing | Shopify Email | Not set up |

**DNS at Hostinger (correct as of Sept 3, leave alone):**
- `A @` → `23.227.38.65` (Shopify)
- `CNAME www` → `shops.myshopify.com`
- MX / SPF / DKIM / DMARC → Hostinger, untouched (mailbox still handles info@)

**Outstanding DNS issue:** an `AAAA @` record still points to `2a02:4780:b:748:0:3880:2618:5` (Hostinger). This sends IPv6 visitors to the retired WordPress install. Recommended: delete it. Not yet approved.

**Printify note:** the connected store shows as "My Shopify Store" — Printify's default label, not a misconfiguration.

**Customily note:** integration lives at Settings → Integrations → provider Printify → Personal Access Token → select store → Enable → Save. Token generated from the Printify Dev Dashboard (profile menu → Connections → Generate → all scopes). Customily's UI drifts from its own docs; their live chat is the fastest way to find a moved button.

---

## 4. The product — FINALIZED Sept 3

**"Custom Photo Puzzle"** — Customily design on the Printify **Jigsaw Puzzle with Tin** base, full-frame image placeholder as the photo-upload layer. One design covers all sizes.

**Variants — confirmed against the live catalogue:**

| Variant | Size | Printify base | **Retail** | Role |
|---|---|---|---|---|
| 110 pcs | 10″ × 8″ | $18.00 | **$39** | entry |
| 500 pcs | 21″ × 15.5″ | $25.96 | **$59** | volume seller |
| 2000 pcs | 40″ × 28″ | $40.97 | **$99** | anchor |

The old 120 / 252 / 500 plan was planning fiction — none of those exist in the catalogue.

**Shipping: $7 flat. Model — free over $59, $7 below.**

| Variant | Shipping | Net kept | Margin |
|---|---|---|---|
| 110 pcs (alone) | customer pays $7 | $19.57 | 50.2% |
| 500 pcs | free | $24.03 | 40.7% |
| 2000 pcs | free | $47.86 | 48.3% |

Net of Shopify Payments on Basic (2.9% + $0.30). The $59 threshold sits deliberately on the volume seller: from the $39 puzzle, $20 more removes a $7 charge, so the real gap is $13. Two small puzzles ($78) also clear it.

Set in Shopify: Settings → Shipping and delivery → $7 flat US rate + free rate conditional on $59 minimum.

*Alternative if you prefer unconditional free shipping:* raise entry to $44, giving 39.6% / 40.7% / 48.3%.

**Printify Premium — later, not now.** 20% off base ($14.40 / $20.77 / $32.78), margins rise to 59–64%. Costs $39/mo or $299/yr. Break-even ≈ 8 orders/month monthly, 5 annual. Launch free, switch once consistently past that.

**⚠️ THE BLOCKER:** the product was **never published to Shopify.** The July 17 session paused at the publish step. Store has zero products. Follow the runbook linked in Section 1.

---

## 5. Brand identity

| Element | Value |
|---|---|
| Display font | Cormorant Garamond |
| Body font | Jost |
| Terracotta (accent) | `#C4633F` |
| Cream (background) | `#F6F1E7` |
| Deep brown (text) | `#3B3128` |
| Hero line | "Make memories come together piece by piece" |

Tone: warm, sentimental, handcrafted, keepsake-oriented.

Existing imagery: `gift-joy.jpg`, `self-treat.jpg`, `keepsake.jpg` (under 260KB each). A puzzle-effect script exists from early work — Python/PIL, supersampled overlay, embossed cut lines on a 13×7 grid.

---

## 6. Settled decisions — do not reopen

- **Shopify, not WooCommerce.** WooCommerce was tried and abandoned.
- **Shopify's transaction costs are accepted.**
- **Printify is the fulfillment provider.**
- **Full automation. No manual fulfillment steps.**
- **Shopify Payments**, not Stripe/Square/WooPayments.
- **Subscriber email via Shopify Email + CSV import.** No Klaviyo, no Mailchimp.
- **Customily is required and stays** *(settled Sept 3)*. Verified directly: the Printify jigsaw base has **no image personalization layer** — only six sizes by piece count. Printify alone cannot accept a customer photo on this product. Customily is the only thing bridging customer upload → print file → Printify without a human. Do not re-propose dropping it or using Printify's Personalization Hub.

---

## 7. Retired / dead — do not revive

- WordPress on Hostinger (Hello Elementor + Elementor), WooCommerce + WooPayments. **Still physically present on the Hostinger server and still running WooCommerce cron daily.** It is dead weight; deleting it is George's call, not yet decided.
- The Elementor homepage build
- JotForm order collection + Stripe test-mode payments
- Customily's $49/month WooCommerce plan

---

## 8. Traps that have already cost time

1. **The Shopify connector defaults to the wrong store.** It authorizes **247AITech** (`nvrry6-4b.myshopify.com`), not Pieces by Heart (`utycgb-x2`). This caused a wrong diagnosis on Sept 3. Confirm the store before any read or write.
2. **Printify has two personalization modes with similar names.** The plain "Enable personalization" toggle is *manual* — the buyer types a request and you build the design by hand. That is the dead flow. Irrelevant now that Customily is settled, but do not get lured by it.
3. **Do not touch DNS to "fix" the site.** On Sept 3 the DNS was briefly repointed from Shopify to the retired WordPress install on a wrong diagnosis, then reverted. The A record and www CNAME pointing at Shopify are correct and intentional.
4. **The site being unreachable is not a DNS problem.** It is because piecesbyheart.com is not yet added as a domain in the Shopify admin (Settings → Domains). Held deliberately until there is a product to sell.

---

## 9. Open items — launch sequence

1. **Publish the Custom Photo Puzzle from Customily** — the blocker. Runbook in Section 1.
2. **Verify the chain end to end** — test order must reach Printify with the print file already generated, no manual step. This is what proves automation.
3. **Order a physical sample** — there are no real listing photos, and mockups convert worse.
4. **Connect piecesbyheart.com in Shopify admin** — Settings → Domains, once there is a product.
5. **Delete the stray AAAA record** — pending George's approval.
6. **Finalize listing copy** — conversion-focused description, listing images.
7. **Launch email** — CSV import of the 256+ list into Shopify Email. Confirm opt-in consent at import.
8. **Promo code + marketing assets** — discount code, graphics/copy for Instagram, TikTok, Pinterest.

**Unanswered questions for George:**
- The "new ideas" he wanted to fold into the launch plan — never captured.
- Where the 256-subscriber CSV lives, and whether opt-in consent is documented.
- What Customily actually costs on the Shopify plan (the $49 figure was the retired WooCommerce plan).

---

## 10. Still unverified

- [ ] Customily account status — design intact? plan lapsed while parked?
- [ ] Printify connection health — token still valid?
- [ ] Theme and homepage content — what does the storefront render?
- [ ] Store policies (refund, privacy, terms, shipping) and shipping zones
- [ ] Shopify Payments still live
- [ ] Whether a Printify sample was ever ordered

---

## 11. Revisit after launch, not before

**Teeinblue** is a credible Customily alternative — API-integrated with Printify, automated fulfillment. Starter $19/mo (1.8% transaction fee from the 51st monthly order), $49/mo (free transactions first 100), Growth $59/mo (1.4%). Cheaper than Customily below roughly 75–80 orders/month; more expensive above.

Do not switch before launch. The design is already built in Customily and the token is wired; swapping means rebuilding the product and re-validating the whole chain. Revisit with a month of real order data.

Printify maintains the authoritative list of compatible personalization tools:
https://help.printify.com/hc/en-us/articles/28903864184593-Which-third-party-tools-support-personalization-with-Printify

---

## 12. How George likes to work

- **Deliver complete, paste-ready artifacts** — whole files, never fragments to assemble.
- **Iterative loop:** he deploys, tests live, reports specific issues back.
- **Flag judgment calls explicitly**; explain reasoning rather than changing things silently.
- **Don't re-ask settled questions.**
- **Build fully before flipping the switch.** A domain was once pointed at an empty install mid-build and caused real disruption.
- **Brief and directive.** Prefers initiative and options over a wall of clarifying questions.

---

## 13. Chronology

| Date | What happened |
|---|---|
| **Jun 3, 2026** | Domain claimed, Hostinger signup. Early Printify setup, JotForm form, Stripe test mode, manual fulfillment plan. |
| **Jul 15, 2026** | WordPress + Elementor build. WooCommerce + WooPayments. Customily signup on the WooCommerce plan. |
| **Jul 17, 2026** | Pivot to Shopify. Second store created, Shopify Payments activated, DNS repointed, Printify + Customily installed and wired. "Custom Photo Puzzle" design built and saved. **Paused before publishing.** |
| **Aug 11, 2026** | Launch planning. Sequence agreed. Subscriber list confirmed at 256+. Parked. |
| **Sep 2, 2026** | Handoff v1 prepared. Confirmed store empty. |
| **Sep 3, 2026** | Site reported offline. Root cause: domain never connected in Shopify admin. DNS briefly mis-repointed to retired WordPress and reverted. Printify-native personalization evaluated and ruled out. **Customily confirmed required. Variants corrected to 110/500/2000. Pricing finalized at $39/$59/$99 with a $59 free-shipping threshold.** Product still not published. |
