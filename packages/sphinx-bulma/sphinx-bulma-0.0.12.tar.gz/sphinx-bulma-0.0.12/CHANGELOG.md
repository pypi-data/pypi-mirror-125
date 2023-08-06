# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

## 0.1.0 - TBD

### Updated

- All **npm** dev dependencies into new versions without security issues
- Main font family now is **Josefin Sans** and **Courier Prime** for code highlights
- Main theme layout now is mostly `Bulma` classes (or `@extend` ones)

### Removed

- All `sass` files from project `scss/module` folder (new components on `scss/components`)
- Many deprecated tags from **Sphinx** template generation
- Old **GitHub** action file

### Changed

- Fontello icons font uses new and different icons now (including custom **Sphinx** and **Bulma** icons)
- Moved from deprecated `node-sass` npm package into **Dart** `sass` package
- Use of deprecated and outdated `cpy` npm package for npm commands, now using `copyfiles` package
- No longer uses `KarmaCSS` package, changed to `Bulma` styles
- Project name from `sphinx_karma_theme` to `sphinx-bluma`

### Added

- Dark and light color palettes using native **CSS** and **JavaScript**
- Custom code highlights styling
- Support for favicon and `navbar` logo
- New theme options `display_git`, `git_host`, `git_user`, `git_repo`, `git_blob`, `git_version`, `git_icon`, `git_desc`, `default_palette`, `sidebar`, `primary`, and `primary_invert`
- Appended new copyright notice (under same license)
- Use examples
