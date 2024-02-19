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

## Sending changes for review

Once you are happy with your local changes, please send a PR.
