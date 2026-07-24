# kotek.net site

Static site for <https://kotek.net>, built with [Zola](https://www.getzola.org) and deployed to Codeberg Pages.

## Local

```sh
zola serve
zola build
zola check
```

## Migration

The old PHP site is kept under `oldsite/kotek.net/www`. Regenerate migrated content and static assets with:

```sh
./scripts/migrate_old_site.py
```

The migration preserves legacy blog slugs such as `/blog/MapDB_update/`.

## Deploy (GitHub Pages)

Hosted on GitHub Pages via GitHub Actions. Every push to `main` runs
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the
site with Zola 0.22.1 and publishes it to the `github-pages` environment.
There is no `pages` branch to maintain.

The custom domain (`kotek.net`) is set in the repository's **Settings -> Pages**.
DNS: point the apex `kotek.net` at GitHub Pages (A/AAAA records) and set
`www.kotek.net` as a CNAME to `jankotek.github.io`. Enable *Enforce HTTPS* once the
certificate is provisioned.

