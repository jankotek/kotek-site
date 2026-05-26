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

## Deploy

The Woodpecker pipeline builds with Zola and force-pushes `public/` to the `pages` branch. Set a private SSH deploy key in Woodpecker as the `deploy_key` secret, and make sure the deploy key has write access to `codeberg.org:jankotek/kotek.net.git`.
