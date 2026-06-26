# EvenFee — project map for agents

Static marketing site for **EvenFee**, a service that helps Amazon FBA sellers
recover fulfillment/storage fees they were overcharged due to incorrect product
dimension/weight measurements. The site backs a Selling Partner API (SP-API)
Solution Provider application, so copy must stay truthful and professional — **no
fabricated testimonials, customer counts, logos, or ratings**.

## Mental model (read this first)

- **Framework-free static site. There is NO build step.** What's in the repo is
  what ships. HTML + one CSS file + one JS file, all hand-authored.
- **The site is LIVE** at https://evenfee.com (GitHub Pages). Treat every change as
  production. A broken asset path or moved page = a broken live page / dead link.
- **No dependencies, no package.json, no node_modules.** Don't add a bundler,
  framework, or runtime library — it would break the "just upload the files" model
  and the site's no-tracker privacy stance.

## Layout

```
.
├── index.html                    # Home: hero, problem, how-it-works, benefits, security, pricing, FAQ, contact
├── resources.html                # Resource hub linking the article pages
├── fba-size-tier-overcharges.html    # Article / SEO landing page
├── fba-reimbursement-basics.html     # Article / SEO landing page
├── privacy.html                  # Privacy Policy (SP-API data, no buyer PII, GDPR) — the canonical legal page
├── terms.html                    # Terms of Service
├── thanks.html                   # Post-contact-form thank-you (JS-off fallback target)
├── 404.html                      # Branded not-found page
│
├── assets/                       # ALL deployed static assets live here, flat (see "Asset paths" below)
│   ├── styles.css                # Every style. Design tokens in :root at the top.
│   ├── main.js                   # Progressive enhancement only (mobile nav, sticky header, contact form, footer year)
│   ├── favicon-32.png            # Favicon
│   ├── apple-touch-icon.png      # iOS home-screen icon
│   ├── icon-192.png / icon-512.png   # PWA manifest icons
│   ├── og-image.png              # 1200×630 social share card
│   ├── logo-mark.png             # Brand mark used in headers/footers
│   ├── mascot.jpg                # Poster frame for the hero mascot video
│   ├── mascot-hero.mp4           # Hero mascot animation (index.html)
│   ├── mascot-avatar.png         # Mascot avatar in the hero tool header
│   ├── dimension-measurement.mp4 # Measurement demo video (Problem section, index.html)
│   └── fonts/                    # Self-hosted Bitcount Grid Double woff2 (no Google Fonts)
│
├── site.webmanifest              # PWA manifest
├── robots.txt                    # Allows all; points to sitemap
├── sitemap.xml                   # Canonical page list — UPDATE when adding/removing/renaming a page
├── CNAME                         # Custom domain (evenfee.com) for GitHub Pages
├── .nojekyll                     # Serve files as-is (no Jekyll processing)
│
├── configure.sh                  # One-command rebrand: name / email / URL across all files (dev-only, not deployed)
├── scripts/generate-assets.py    # Regenerate favicon/icons/OG image (dev-only, not deployed)
├── docs/launch-checklist.md      # Pre-launch checklist (dev-only, not deployed)
├── README.md                     # Human-facing setup/deploy guide (dev-only, not deployed)
└── .github/workflows/deploy.yml  # GitHub Pages deploy (see "Deploy")
```

## Where to make common changes

| Task | File |
|------|------|
| Home page copy / sections | `index.html` — sections are commented (`<!-- ===== Hero ===== -->`) |
| Colors, spacing, radius, shadows | `:root` tokens at the top of `assets/styles.css` |
| Any styling | `assets/styles.css` (single file, no preprocessor) |
| Interactive behavior | `assets/main.js` (vanilla JS, must degrade gracefully without JS) |
| Legal text | `privacy.html`, `terms.html` (standalone documents) |
| Add/rename/remove a page | the `.html` file **and** `sitemap.xml`; check inter-page nav links |
| Brand name / email / URL everywhere | run `./configure.sh "Name" "email" "https://url"` (no trailing slash) |
| Regenerate icons/OG image | edit constants in `scripts/generate-assets.py`, then run it |

## Asset paths (important — don't break cache-busting)

Reference assets with **relative paths** exactly like `assets/styles.css`,
`href="assets/icon-512.png"`, `src="assets/mascot-hero.mp4"`, `poster="assets/mascot.jpg"`.

The deploy workflow rewrites every `src`/`href`/`poster="assets/…"` to append a
`?v=<commit-sha>` cache-buster. Rules that follow from this:
- **Keep `assets/` flat and reference it relatively.** A leading-slash path
  (`/assets/…`) or an absolute URL will NOT get cache-busted and can break on a
  project sub-path. Relative paths also let the site work from both the apex domain
  and a `/repo/` sub-path.
- Don't hand-add `?v=` query strings — the deploy adds them.

## Deploy

- **Push to `main` → `.github/workflows/deploy.yml` runs → GitHub Pages publishes.**
  Also triggerable manually from the Actions tab.
- The workflow copies the repo into `_site/`, **excluding dev-only paths**:
  `.git`, `.github`, `_site`, `scripts`, `configure.sh`, `README.md`, `CLAUDE.md`,
  `docs`. Anything else in the repo root ships. (Add new dev-only files to that
  exclude list so they don't go live.)
- It then stamps the 8-char commit SHA into `build.txt`, injects
  `<meta name="app-build">` into every page, and appends `?v=<sha>` to asset URLs.
  `assets/main.js` polls `build.txt` and auto-refreshes clients when a new build is live.

## Working conventions

- **Branch + PR.** Develop on a feature branch (current: `claude/confident-euler-ka2g39`),
  push, open a PR to `main`, merge. Don't push straight to `main`.
- **Preview locally** with no build: `python3 -m http.server 8000` then open
  http://localhost:8000/.
- **Accessibility & motion:** preserve skip link, focus styles, ARIA, and
  `prefers-reduced-motion` handling when editing markup/CSS/JS.
- **Placeholders before launch:** `EvenFee`, `hello@evenfee.com`, the contact form's
  `YOUR_FORM_ID` (Formspree), and the AWS sub-processor in `privacy.html` are
  placeholders. See `docs/launch-checklist.md` and the README before go-live.
