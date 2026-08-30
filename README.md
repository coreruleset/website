# CRS Project Website Repository
[![Build and link check](https://github.com/coreruleset/website/actions/workflows/test.yml/badge.svg)](https://github.com/coreruleset/website/actions/workflows/test.yml)

This repository contains the website for the OWASP CRS Project.

## For users of the CRS

The generated website is automatically updated at https://coreruleset.org/. If you intend to _contribute_ to the website, the rest of this page will guide you through it.

## Requirements

You can edit the documentation on your local system. You will need:
- [Node.js and pnpm](https://pnpm.io) for installing dependencies
- [dart-sass](https://github.com/sass/dart-sass) for transpiling to CSS

`pnpm install` pulls in Hugo _extended_ as the `hugo-extended` package, so the pnpm scripts below work without a system-wide install. If you prefer your own [Hugo binary](https://gohugo.io/getting-started/installing/), it must be the **extended** build.

**Important: You need Hugo _extended_ >= 0.163.0** — the version CI builds with is pinned in `package.json` and `.github/workflows/test.yml`.

There is also a devcontainer (`.devcontainers/devcontainer.json` plus the `Dockerfile`) if you would rather not install anything locally.

## Cloning this repository

Clone this repository to work locally. This way you can edit and verify quickly that everything is working properly before creating a new pull request.

To clone, use the *recursive* option so you will be getting also the theme to render the pages properly:

```bash
git clone --recursive git@github.com:coreruleset/website.git
```

We use two subrepos:
- the theme
- the documentation subrepo, which is built with a different theme

If you just want to edit documentation (not the website), you can do it in the [documentation repo](https://github.com/coreruleset/documentation/)

## Editing locally

Install the dependencies once:

```sh
pnpm install
```

Now you have all in place to perform your local edits.

Everything is created using markdown, and you will normally use the `content` subdirectory to add your edits.

The theme has shortcodes that can be used to simplify editing. You can get more information about it on [Hugo Dot-Org theme](https://themes.gohugo.io/themes/dot-org-hugo-theme/).

Then start the development server — while you edit and save, your changes are refreshed in the browser:

```sh
pnpm dev
```

Then check your edits on http://localhost:1313/. Drafts and future-dated posts are included, so you can preview a post before its publication date.

Other scripts:

| command | what it does |
|---------|--------------|
| `pnpm dev` | development server with drafts and future posts |
| `pnpm dev:start:with-pagefind` | same, but builds the [Pagefind](https://pagefind.app/) index first so site search works locally |
| `pnpm dev:build` | one-off build, no server |
| `pnpm build` | production build (`--gc --minify`), output in `public/` |

The documentation subsite is a separate Hugo site and is not part of these builds. CI builds it with `hugo -s subsite/docs` and merges the output into `public/docs`.

## Online Preview

The site is hosted on Cloudflare Pages. Merges to `main` are deployed to https://coreruleset.org/, and every pull request gets its own preview deployment, linked from the PR.

Pull requests also run the [test workflow](.github/workflows/test.yml), which builds both the main site and the docs subsite and runs a [lychee](https://lychee.cli.rs/) link check over `content/`.

## Authors

Because users are `git` users now (there is no user "logged"), there is a [mapping between authors and github users](https://github.com/coreruleset/website/blob/main/data/authors.yaml). If you want to collaborate, please add your github username as the key, and your data below. See the examples in that file.

## Sending changes for review

Once you are happy with your local changes, please send a PR.

## Drawings

All illustrations are coming from https://undraw.co/, unless explicitly noted. See their [license](https://undraw.co/license).

All images, assets and vectors published on unDraw can be used for free. You can use them for noncommercial and commercial purposes. You do not need to ask permission from or provide credit to the creator or unDraw. Thanks to [Katerina Limpitsouni](https://twitter.com/ninaLimpi) for her work :pray:


## Favicons

Favicons were generated using https://realfavicongenerator.net.

## Emojis! :tada:

Check the hugo reference for the [list of supported emojis!](https://gohugo.io/quick-reference/emojis/)
