# ColaXpress — build & maintenance

The site under `public_html/` is **generated** by a small dependency-free build
system. Do not hand-edit the chrome (header / nav / footer / `<head>` boilerplate)
in `public_html/` directly — those changes will be overwritten on the next build.
Edit the source, then rebuild.

## Layout

```
src/
  _data/site.json     # nav, footer links, brand + legal strings, css/js versions
  _partials/          # head.html, header.html, footer.html  (shared chrome templates)
  pages/<path>.html   # one source per page: per-page <head> SEO/JSON-LD + <main> only
build.py              # composes src/ -> public_html/   (Python 3 stdlib, no deps)
extract.py            # one-time migration that produced src/pages from the old site
verify_rebuild.py     # proves a rebuild is structurally identical to the current site
public_html/          # BUILD OUTPUT — this is what you FTP-upload to the server
```

`public_html/` also holds static assets (CSS, JS, images, favicons, `sitemap.xml`,
`robots.txt`). The build **never** touches those — only the `*.html` pages.

## Common tasks (each is now a ONE-place edit)

- **Change the nav / footer links** → edit `src/_data/site.json` → `python3 build.py`
- **Change the footer text / legal disclaimer** → `src/_data/site.json` → rebuild
- **Bump the CSS or JS cache version** → `css_ver` / `js_ver` in `site.json` → rebuild
- **Change shared header/footer markup** → edit the relevant `src/_partials/*.html` → rebuild
- **Edit a page's content or SEO** → edit that file in `src/pages/` (only its `<head>`
  per-page tags + `<main>` live there) → rebuild
- **Add a new page** → create `src/pages/<dir>/<slug>.html` following the marker
  format below → rebuild. Nav/footer/head are applied automatically.

### Page source format (`src/pages/...`)
```
<!--ACTIVE:Grow System-->          (nav item to highlight; empty for none)
<!--BEGIN-HEAD-->
  ...per-page <meta>/<link canonical>/og/twitter/<title>/JSON-LD, verbatim...
<!--END-HEAD-->
<!--BEGIN-MAIN-->
  <main> ...page content... </main>
<!--END-MAIN-->
```

## Build & verify

```
python3 build.py                  # regenerate public_html/
python3 build.py --out /tmp/dist  # build to a scratch dir instead
python3 verify_rebuild.py /tmp/dist   # assert /tmp/dist is structurally identical to public_html
```

`verify_rebuild.py` gates: `<head>` equal as a set, `<body>` equal in order,
every JSON-LD block semantically equal, and all title/description/canonical/OG/
Twitter tags equal. Any difference fails.

## Deploy

The site is deployed by **manual FTP upload** of `public_html/` (no CDN). After a
rebuild, upload the changed files and hard-refresh. Because the cache version
lives in `site.json`, a chrome change can be shipped by re-uploading the affected
HTML (and `style.css` when it changed).

## Rollback

The pre-build-system snapshot is tagged `pre-phase4`:
```
git checkout pre-phase4 -- public_html/   # restore the exact previous output
```
