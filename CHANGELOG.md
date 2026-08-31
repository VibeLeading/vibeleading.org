# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial site: hero with live HUD telemetry, methodology cards, Diamond Squad band,
  5 skills, 4 MCP servers, book section, Pilot's Oath, support section.
- GitHub Pages deployment workflow and custom-domain CNAME for vibeleading.org.
- NOTICE clarifying MIT-licensed code vs the copyrighted book.
- SEO: canonical, robots, Open Graph + Twitter cards with og-cover image, JSON-LD
  graph (Organization, WebSite, Person, Book, ItemList for skills and MCPs, FAQPage).
- GEO: visible FAQ section with schema.org FAQPage markup.
- PWA: web manifest, PNG icon set (192/512/maskable/apple-touch), service worker
  with offline fallback, update-toast, robots.txt and sitemap.xml.

### Fixed

- Mobile menu: `hidden` attribute was overridden by the flex display rule.