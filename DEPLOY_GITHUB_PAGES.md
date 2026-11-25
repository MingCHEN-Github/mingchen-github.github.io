# Deploy Ming Chen's personal website

Prepared 25 November 2026. GitHub Action release tags were checked against the official actions repositories. The exported website was built and checked locally; the workflow has not yet run in your GitHub account.

## Recommended arrangement

- Website source: a separate GitHub repository named `mingchen-github.github.io`, owned by `MingCHEN-Github`.
- Hosting: GitHub Pages.
- First address: `https://mingchen-github.github.io/`.
- Optional long-term address: a personally registered domain pointing to the same GitHub Pages site.

A domain is your website's address. Hosting serves the website files. A custom domain can be used with GitHub Pages; you do not need a separate paid web-hosting plan for this static site.

## 1. Create the website repository

1. Sign in to GitHub and select **New repository**.
2. Owner: **MingCHEN-Github**.
3. Repository name: **mingchen-github.github.io**.
4. Choose **Public** for the simplest free Pages setup.
5. Add a README when creating it and use **main** as the default branch.
6. Keep the existing **JobApplication** repository private and separate.

GitHub Pages also supports private source repositories on eligible paid GitHub plans. A private source repository does not make an ordinary personal Pages website private.

## 2. Enable Pages

In the new website repository:

**Settings > Pages > Build and deployment > Source > GitHub Actions**.

This package provides its own workflow. It builds the Python templates and deploys **dist/**. Do not select a Jekyll theme for this workflow.

## 3. Copy the package and push

Download `MingChen_Website_GitHub_Pages.zip` and place it on the Ubuntu machine where you manage the website. Extract it to a working directory. It contains a folder named `ming-chen-website`.

For example, with the ZIP at `~/MingChen_Website_GitHub_Pages.zip`:

```sh
mkdir -p ~/websites
unzip ~/MingChen_Website_GitHub_Pages.zip -d ~/websites
cd ~/websites
git clone git@github.com:MingCHEN-Github/mingchen-github.github.io.git
cd mingchen-github.github.io
cp -a ../ming-chen-website/. .
git add .
git commit -m "Add personal research and engineering website"
git push origin main
```

These commands use SSH authentication already configured for GitHub. If you use HTTPS authentication, clone with:

```sh
git clone https://github.com/MingCHEN-Github/mingchen-github.github.io.git
```

The copy command includes `.github/`, which contains the deployment workflow. Ensure `src/`, `scripts/`, and `.github/` are directly inside the repository rather than another enclosing `ming-chen-website/` directory.

## 4. Check the deployment

1. Open the repository's **Actions** tab.
2. Open **Deploy personal website**.
3. Confirm both **build** and **deploy** succeeded.
4. Open the published URL shown in **Settings > Pages** or the workflow environment.

Expected user-site URL: `https://mingchen-github.github.io/`. It is not active merely because the package has been prepared.

If the first run occurred before Pages was enabled, set Source to GitHub Actions and use **Actions > Deploy personal website > Run workflow**, selecting main.

## 5. Updating the website

Edit `src/content.json` for structured content. Page wording and layouts are in `scripts/build.py`.

```sh
python3 scripts/build.py
python3 scripts/check.py
git add .
git commit -m "Update website content"
git push origin main
```

Each push to main rebuilds and deploys the site. Regenerate the PDF separately when its content changes; ordinary builds copy the included PDF asset.

## 6. Register a personal domain, if wanted

A domain is optional. You can deploy on github.io first and connect it later.

Choose a memorable name that works across research and engineering roles. Compare the **renewal** price as well as the first-year registration price. Cloudflare Registrar and Porkbun are two providers you can compare. Domain availability has not been checked in this package.

The examples below use **example.com**, a placeholder. Substitute the domain you actually own. Your registrar does not need to be your website host.

## 7. Verify domain ownership

1. Open your personal **GitHub Settings > Pages** (profile settings, not the repository).
2. Choose **Add a domain**.
3. Enter your registered domain.
4. Copy the exact DNS **TXT name and value** GitHub displays into the DNS zone managed by your registrar or DNS provider.
5. Return to GitHub and complete verification. Retain that TXT record.

Do not guess the verification value; it is account-specific.

## 8. Connect the domain

First set the domain in **website repository > Settings > Pages > Custom domain**, for example `example.com`, and save it. Then configure the routing records in the domain's DNS settings:

| Type | Name/host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | mingchen-github.github.io |

`@` means the bare domain, such as example.com. The CNAME target is a hostname: no https:// prefix and no repository path.

GitHub also publishes optional IPv6 records in its current documentation. If you add IPv6, use the current GitHub Pages values rather than keeping records from a previous host.

Set only the records for the website hostnames; keep any existing email records such as MX records. Initial DNS setup is easiest without an additional HTTP proxy in front of GitHub.

With both apex and www configured, GitHub redirects to the domain selected in repository Pages settings. DNS propagation and availability of the HTTPS checkbox can take up to 24 hours.

For the included GitHub Actions deployment, a repository CNAME file is not required; the custom domain is configured in the GitHub Pages settings. The DNS CNAME record above is a separate concept.

## 9. Update metadata and enable HTTPS

Set the origin used by the website metadata and sitemap:

```sh
python3 scripts/set_site_url.py https://example.com
python3 scripts/build.py
python3 scripts/check.py
git add src/content.json dist
git commit -m "Use personal domain"
git push origin main
```

Return to **Settings > Pages** and enable **Enforce HTTPS** when it becomes available. Verify the homepage, About, Experience, Publications, and CV download using the new address. The website remains a static site served by GitHub Pages.

## Alternative: Cloudflare Pages with private source

Cloudflare Pages supports public and private GitHub repositories and automatic deployment from Git pushes.

1. For Cloudflare-only hosting, remove `.github/workflows/deploy.yml` from the exported copy, then push the remaining website package to a separate GitHub repository; it can be private. Cloudflare will handle deployment instead of the GitHub Pages workflow.
2. In Cloudflare: **Workers & Pages > Create application > Pages > Connect to Git**.
3. Select that repository.
4. Use these build settings:

| Setting | Value |
|---|---|
| Framework preset | None |
| Production branch | main |
| Build command | python3 scripts/build.py && python3 scripts/check.py |
| Build output directory | dist |

The included `.python-version` requests Python 3.12. The normal build uses no third-party Python packages. Once Cloudflare gives you the actual pages.dev URL, update `site_url` to that HTTPS origin and push. You can then add a registered domain through the Cloudflare Pages project's **Custom domains** setup.

## Useful official references

- GitHub Pages overview: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- Custom workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- Custom domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Verify a domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- Cloudflare Pages Git integration: https://developers.cloudflare.com/pages/get-started/git-integration/
- Cloudflare Registrar: https://www.cloudflare.com/domains/
- Porkbun pricing: https://porkbun.com/products/domains
