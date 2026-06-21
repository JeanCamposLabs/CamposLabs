# EvenFee — launch checklist & agent runbook

Step-by-step list of what still needs a human (or another agent **with the right
credentials / tools**) to finish, plus how this site is built and deployed.

> This file lives under `docs/` and is **excluded from the published site**
> (see `.github/workflows/deploy.yml`), so it will not appear on evenfee.com.

---

## How the site is built & deployed (read first)

- **Static site, no build step.** Plain HTML + one CSS file (`assets/styles.css`)
  + ~50 lines of vanilla JS (`assets/main.js`). Edit files directly.
- **Deploy = push to `main`.** The GitHub Actions workflow
  `.github/workflows/deploy.yml` publishes to GitHub Pages on every push to `main`
  (and can be run manually from the Actions tab). The custom domain is `evenfee.com`
  (see `CNAME`).
- **To verify a deploy:** check the latest **"Deploy site to GitHub Pages"** run in
  the Actions tab is green, then load https://evenfee.com/.
- **Local preview:** `python3 -m http.server 8000` then open http://localhost:8000/.
- **Design tokens** (colours, spacing, radius) live in `:root` at the top of
  `assets/styles.css`. The brand palette is **navy/indigo (primary) + emerald
  (success) + teal (secondary, "scene teal" `--teal-300: #9fced3`** sampled from the
  hero mascot animation background).

---

## Remaining steps (in priority order)

### 1. Wire up the contact form  ·  _needs a Formspree account_  ·  **HIGH (conversions)**
Right now `index.html`'s contact form `action` is the placeholder
`https://formspree.io/f/YOUR_FORM_ID`. With JS on it falls back to opening the
visitor's email app (`mailto:`) — functional, but a real drop-off point.

**Do this:**
1. Create a free form at https://formspree.io and point it at a **monitored inbox**
   (e.g. `hello@evenfee.com`).
2. Copy the endpoint, e.g. `https://formspree.io/f/abcdwxyz`.
3. In `index.html`, replace `YOUR_FORM_ID` in the form's `action="…"` with your ID.
4. (No other change needed — `assets/main.js` already AJAX-submits and shows the inline
   "Thanks — your message is on its way!" state when a real endpoint is present, and
   falls back to a normal POST → `thanks.html` when JS is off. The honeypot field stays.)

**Acceptance:** submit the live form → message arrives in the inbox; the page shows the
inline success state without reloading.

> Alternative with no signup flow: [Web3Forms](https://web3forms.com) — set `action` to
> `https://api.web3forms.com/submit` and add a hidden `access_key` field.

### 2. Confirm the privacy-policy hosting sub-processor  ·  _needs a decision_  ·  **HIGH (legal)**
`privacy.html` (section 7, "Sharing & sub-processors") lists **Amazon Web Services
(AWS), EU region** as a placeholder, with a `TODO` comment. This is the host of your
**data-processing backend** (where SP-API data is stored) — it is *separate* from where
this marketing site is hosted (GitHub Pages).

**Do this:** confirm the real provider + region for the backend, update the table row in
`privacy.html`, and delete the `<!-- TODO … -->` comment above it. Then have a lawyer
review `privacy.html` and `terms.html` (they are solid drafts, not legal advice).

### 3. Regenerate the hero poster from the new video  ·  _needs ffmpeg_  ·  **MEDIUM**
The hero now plays **`assets/mascot-hero.mp4`** (the new clip you uploaded). Its `poster`
is still `assets/mascot.jpg` (the *previous* clip's final frame). Same mascot/teal scene,
so the load looks smooth — but for a pixel-perfect first frame, regenerate the poster:

```bash
# first frame as the poster
ffmpeg -i "assets/mascot-hero.mp4" -frames:v 1 -q:v 2 assets/mascot-hero.jpg
# then in index.html set: poster="assets/mascot-hero.jpg"
# and the <img> fallback inside the <video> to the same file
```
(Could not be done in the build environment used to ship this — no ffmpeg / no network.)

### 4. (Optional) Compress the new hero video  ·  _needs ffmpeg_  ·  **LOW**
`assets/mascot-hero.mp4` is ~1.85 MB (the previous `assets/mascot.mp4` was ~266 KB).
It autoplays muted, so lighter is better for first paint. Suggested:

```bash
ffmpeg -i "assets/mascot-hero.mp4" -vf "scale=1040:-2" -an \
  -c:v libx264 -crf 28 -preset slow -movflags +faststart assets/mascot-hero.min.mp4
# swap the <source> to the .min.mp4 if the quality holds up
```
**Note:** keep `assets/mascot.mp4` — it is intentionally retained ("this is also nice")
and can be reused elsewhere. It is no longer referenced by any page.

### 5. Final pre-launch verification  ·  **MEDIUM**
- [ ] Contact form delivers to a real inbox (step 1).
- [ ] Privacy sub-processor is accurate (step 2).
- [ ] HTTPS enforced on the custom domain (GitHub Pages → Settings → Pages).
- [ ] Re-read all copy against your **actual** data handling (read-only SP-API, no buyer
      PII, encrypted in transit & at rest, success-based pricing, deletion on revocation).
- [ ] `sitemap.xml` / `robots.txt` point at the final domain (already `evenfee.com`).

---

## What changed in the conversion/teal pass (for reference)
- First-person, outcome-specific CTAs site-wide ("Get my free fee audit").
- Persistent mobile sticky CTA (`assets/main.js` + `.mobile-cta` in CSS); hides over the
  contact form/footer; reduced-motion safe.
- Secondary **teal** brand colour woven in: hero ambient gradient + a teal aura behind the
  hero video, the trust strip, the Estimate section (`.section--teal`), and the estimator
  result card. Tokens: `--teal-050 … --teal-700` in `assets/styles.css :root`.
- Hero video swapped to `assets/mascot-hero.mp4`; `assets/mascot.mp4` kept.
- `og:image:alt` / `twitter:image:alt` added; unreferenced `assets/brand-v1/` excluded
  from the published artifact.
