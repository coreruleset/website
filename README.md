# CRS Project Website Repository

This repository contains the website for the OWASP CRS Project.

## For users of the CRS

The generated website is automatically updated at https://coreruleset.org/. If you intend to _contribute_ to the website, the rest of this page will guide you through it.

## Requirements

You can edit the documentation on your local system. You will need is the latest [Hugo binary](https://gohugo.io/getting-started/installing/) for your OS (Windows, Linux, Mac), and a working NodeJS compiler (required by the theme we use).

**Important: You need Hugo _extended_ version >= 0.93.0.**

## Cloning this repository

After getting hugo, just clone this repository to work locally. This way you can edit and verify quickly that everything is working properly before creating a new pull request.

To clone, use the *recursive* option so you will be getting also the theme to render the pages properly:

```bash
git clone --recursive git@github.com:coreruleset/website.git
```

We use two subrepos:
- the theme
- the documentation subrepo, which is built with a different theme

If you just want to edit documentation (not the website), you can do it in the [documentation repo](https://github.com/coreruleset/documentation/)

## Editing locally

Now you have all in place to perform your local edits.

Everything is created using markdown, and you will normally use the `content` subdirectory to add your edits.

The theme has many shortcodes and others that you can use to simplify editing. You can get more information about it on [Hugo Dot-Org theme](https://themes.gohugo.io/themes/dot-org-hugo-theme/).

You can run `hugo` to serve the pages, and while you edit and save, your changes will be refreshed in the browser!

Use:
```
hugo serve
```

Then check your edits on http://localhost:1313/.

## Authors

Because users are `git` users now (there is no user "logged"), there is a [mapping between authors and github users](https://github.com/coreruleset/website/blob/main/data/authors.yaml). If you want to collaborate, please add your github username as the key, and your data below. See the examples in that file.

## Sending changes for review

Once you are happy with your local changes, please send a PR.

## Drawings

All illustrations are coming from https://undraw.co/, unless explicitly noted. Their license is as follows:

Copyright 2024 Katerina Limpitsouni

All images, assets and vectors published on unDraw can be used for free. You can use them for noncommercial and commercial purposes. You do not need to ask permission from or provide credit to the creator or unDraw.

More precisely, unDraw grants you an nonexclusive, worldwide copyright license to download, copy, modify, distribute, perform, and use the assets provided from unDraw for free, including for commercial purposes, without permission from or attributing the creator or unDraw. This license does not include the right to compile assets, vectors or images from unDraw to replicate a similar or competing service, in any form or distribute the assets in packs or otherwise. This extends to automated and non-automated ways to link, embed, scrape, search or download the assets included on the website without our consent.

## Favicons

Favicons were generated using https://realfavicongenerator.net.

## Emojis! :tada:

Check the hugo reference for the [list of supported emojis!](https://gohugo.io/quick-reference/emojis/)
