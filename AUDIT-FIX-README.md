# Sumum Traders — SEO audit fix bundle

This bundle is a drop-in replacement for the contents of `sumum-traders/sumum-traders.github.io` repository as of the audit date. Apply by overwriting every file in the repository root with the matching file from this bundle, then committing.

## What changed

**34 files** modified across the site. Total: ~1,200 line-changes.

### 1. Fixes that resolve the validator findings

| Finding | Resolution |
|---|---|
| WARNING: `geo` not valid on `Organization` | `@type` changed to `["Organization", "LocalBusiness"]` on every page (33 blocks) |
| ERROR on `WebPage` (Speakable selector) | Verified `<section id="tldr">` already exists on AEO page; selectors now resolve |
| Date inconsistency on site vs GBP/MCA | All 31 occurrences of `17 December 2015` → `17 July 2015`; JSON-LD `foundingDate` `2015-12-17` → `2015-07-17` |

### 2. Coordinate correction (~880 m drift)

All 80+ occurrences of `13.313, 77.145` (and variants `13.313;77.145`, `13.313 N, 77.145 E`, `query=13.313,77.145`, `13.313 degrees north and/or 77.145 degrees east`) → `13.30792, 77.15118`.

### 3. Hours correction (matches GBP, not the previous narrower window)

All occurrences of `9 AM to 7 PM` (in any phrasing) → `6 AM to 9 PM`. Schema `openingHoursSpecification` now declares `06:00–21:00` Mon–Sat.

### 4. Address upgrade

`Kyathsandra, Tumakuru, Karnataka 572104` → `NH 48 Junction, Ring Road, Kyathsandra, Tumakuru, Karnataka 572104` in footers and JSON-LD `streetAddress`.

### 5. Schema enrichment (every Organization JSON-LD block)

New fields added on top of existing structure:

- `@type`: `["Organization", "LocalBusiness"]`
- `@id`: `https://sumum-traders.github.io/#org` (canonical entity ID)
- `alternateName`: `SUMUM TRADERS`
- `telephone`: `+918050568880`
- `priceRange`: `₹₹`
- `image`: site OG image
- `hasMap`: `https://maps.google.com/?cid=11458553334017366557`
- `openingHoursSpecification`: Mon–Sat 06:00–21:00
- `sameAs`: GMaps short link, GMaps CID URL, g.page short URL, WhatsApp link
- `contactPoint`: two ContactPoints — sales (primary phone) and customer service (secondary phone)
- `address.streetAddress`: full street address with NH 48 Junction landmark
- `description`: factual one-line description
- `geo`: corrected coordinates

Existing fields preserved: `name`, `legalName`, `identifier`, `email`, `url`, `logo`, `founder`, `areaServed`.

### 6. Footer rewrite (32 pages)

Old two-line footer with email only → four-line footer with full address, two phones (`tel:` links), email, WhatsApp, and Google Maps link. Designated-partner line preserved with corrected date.

### 7. HTML lang correction

`<html lang="en">` → `<html lang="en-IN">` on all 31 HTML pages, matching the existing `og:locale="en_IN"`.

### 8. og:type correction (AEO page only)

`/llm-aeo-south-india.html`: `og:type="article"` → `og:type="website"`. Article type is correct on `/blog/*` and `/technical-*` pages and is left untouched there.

### 9. llms.txt updates

- Address line updated with NH 48 Junction
- New lines added under `## Identity`: Phone, WhatsApp, Google Maps
- Operating hours corrected to 6 AM to 9 PM

## What was NOT changed (intentional)

- `https://sumum-traders.github.io/` URLs throughout — these remain on the current host. Flip to `https://sumum.co.in/` in a separate commit during the domain migration.
- `og:type="article"` on blog and technical pages — these are correct.
- `sitemap.xml` — no URL changes needed; lastmod can be bumped optionally.
- `robots.txt` — no change required.
- Existing canonical tags, OG cards, Twitter cards, Dublin Core meta, breadcrumb schema, FAQ schema, WebPage schema — all preserved.

## How to deploy

### Option A — github.com web UI (easiest, no tools)

1. Go to `https://github.com/sumum-traders/sumum-traders.github.io`
2. Click `Add file` → `Upload files`
3. Drag every file from this bundle (except this README) onto the upload area
4. GitHub will detect them as updates to existing files
5. Commit message: `SEO audit: correct date/coords/hours; upgrade Organization to LocalBusiness; add phones`
6. Click `Commit changes`
7. GitHub Pages rebuilds in 1–2 minutes

### Option B — github.dev (browser VS Code)

1. On the repo page, press `.` (period) — full VS Code opens in browser
2. In the left sidebar, drag this entire folder over the file tree
3. VS Code shows the diff in the Source Control panel
4. Review, write commit message, commit & push

### Option C — git CLI

```bash
cd /path/to/your/local/clone
# Copy all files from this bundle into the repo root, overwriting
git add -A
git status   # review the diff
git commit -m "SEO audit: correct date/coords/hours; upgrade Organization to LocalBusiness; add phones"
git push
```

## Post-deploy verification

Wait ~2 minutes after push, then run:

| Test | URL | Pass criteria |
|---|---|---|
| Rich Results Test (home) | `https://search.google.com/test/rich-results?url=https://sumum-traders.github.io/` | LocalBusiness recognised, 0 errors |
| Rich Results Test (AEO) | `https://search.google.com/test/rich-results?url=https://sumum-traders.github.io/llm-aeo-south-india.html` | 0 errors, 0 warnings on Organization, WebPage, BreadcrumbList, FAQPage |
| Schema.org validator (AEO) | `https://validator.schema.org/?url=https://sumum-traders.github.io/llm-aeo-south-india.html` | 0 errors, 0 warnings |
| Visual spot-check | Footer of any page | Two phone numbers, WhatsApp, Map link, NH 48 Junction in address, "17 July 2015" |

If any test still flags errors, paste the validator output and we will diagnose.

## Next commit (separate, post-DNS)

After DNS for `sumum.co.in` resolves and HTTPS is live:

1. Create `CNAME` file at repo root containing the single line `sumum.co.in`
2. Find/replace `https://sumum-traders.github.io` → `https://sumum.co.in` across all `.html`, `sitemap.xml`, `llms.txt`, JSON-LD
3. Commit
4. Flip GBP "Website" field from the github.io URL to `https://sumum.co.in/`
5. Add the new domain as a property in Google Search Console; submit the sitemap
