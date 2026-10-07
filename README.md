# aaroncoyner.com

Personal site, served by GitHub Pages at https://aaroncoyner.com. It is plain HTML, CSS and JS with no build step.

## Layout

- `index.html`: the page (bio, experience, publications, contact)
- `style.css`: styles; the palette is in `:root`
- `assets/`: headshot
- `data/publications.json`: publication list, generated (don't edit by hand)
- `scripts/update_publications.py`: pulls publications from PubMed
- `.github/workflows/update-publications.yml`: runs the script every Monday and commits changes
- `CNAME`: custom domain (managed by GitHub Pages)

## Updating

- **Text and roles:** edit `index.html` and push.
- **Publications:** automatic. To refresh now, go to Actions → "Update publications" → Run workflow.
  If a paper by a different "Coyner AS" appears, add its PMID to `EXCLUDE_PMIDS` in the script.
- **CV:** replace `cv.pdf` in the repo root.

## Previewing locally

`fetch()` doesn't work from `file://`, so serve the folder:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.
