# vibeleading.org

The official website of **VibeLeading** — the open-source home of the Vibe Leading
methodology from Jean Machuca's book _Vibe Leading The AI: The Corporate Race Against
Machines_.

Live at **[https://vibeleading.org](https://vibeleading.org)** — hosted on GitHub Pages.

## What this site covers

- The methodology in one glance: the Vibe, **IRA (Intent-Result Alignment)**, the HUD,
  Organizational Geometry, the Double Tenaza, and the Garage.
- The **5 agent skills** (`mission-script`, `ira-prompting`, `hud-setup`,
  `pit-stop-audit`, `org-geometry`) with one-command installs.
- The **4 MCP servers** (`hybrid-data-engine`, `document-architect`,
  `real-time-scout`, `privacy-shield`).
- The book, the author, and sponsorship.

## Stack

Pure static HTML + CSS + JS. No framework, no build step, no dependencies — which makes
it fast, secure, and trivial to deploy on GitHub Pages. The look is dark-cockpit
glassmorphism with neon cyan/pink accents (backdrop blur, parallax orbs, a starfield
canvas, and scroll reveals).

## Local development

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Deployment

GitHub Actions ([`.github/workflows/pages.yml`](.github/workflows/pages.yml)) deploys the
`main` branch to GitHub Pages on every push. The [`CNAME`](CNAME) file and the
repository's Pages custom-domain setting bind the site to `vibeleading.org`.

### Custom domain (DNS)

For the domain to serve, point it at GitHub Pages in your DNS provider:

| Record | Name | Target |
| --- | --- | --- |
| A | `vibeleading.org` | `185.199.108.153` |
| A | `vibeleading.org` | `185.199.109.153` |
| A | `vibeleading.org` | `185.199.110.153` |
| A | `vibeleading.org` | `185.199.111.153` |
| CNAME | `www.vibeleading.org` | `vibeleading.github.io` |

Then verify the domain under **GitHub → Settings → Pages → Custom domains**, and the
Pages TLS certificate provisions automatically.

## License

**MIT** — see [LICENSE](LICENSE). The site uses icons/imagery styled after the book; the
book itself is copyrighted material (© 2026 Jean Machuca, ISBN 9798252505008) — see
[NOTICE](NOTICE).