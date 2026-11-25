# Ming Chen - personal website

Research and engineering portfolio: four research case studies, an engineering training study, professional experience and supervised collaborations, publications, research notes, an About page, and a downloadable CV.

This portable copy is configured for `https://mingchen-github.github.io/`. The existing hosted site is independent of this deployment copy.

## Deploy

Follow `DEPLOY_GITHUB_PAGES.md`. A complete build-and-deploy workflow is included at `.github/workflows/deploy.yml`.

Normal builds need only Python 3 and its standard library:

```sh
python3 scripts/build.py
python3 scripts/check.py
```

The generated website is in `dist/`. The source PDF and image assets are already included.

## Edit

- `src/content.json`: identity, contact links, current role, experience, collaborations, teaching, recognition, research interests, project descriptions, and publication data.
- `scripts/build.py`: page templates, research notes, and page layouts.
- `src/styles.css`: typography, colors, responsive layouts, and print styles.
- `src/app.js`: navigation, filters, diagram controls, and citation copying.
- `scripts/make_assets.py`: optional PDF CV and social image regeneration, requiring reportlab, Pillow, and DejaVu fonts. Check its concise PDF summaries when changing CV text.

To use a custom domain:

```sh
python3 scripts/set_site_url.py https://example.com
```

Then commit and push; the workflow rebuilds the website automatically. Replace `example.com` with your registered domain and also configure GitHub Pages and DNS as described in the deployment guide.

## Local preview

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. The website's root-relative links require a user-site deployment or a custom domain at the site root. A repository-subdirectory Pages URL would need a base-path adjustment.

The exported package contains the public website, not the private job-application repository, Git history, or the original hosting configuration.
