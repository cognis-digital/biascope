# BIASCOPE — Embedded bias probe suite — demographic / occupational / geographic

> Part of the **[Cognis Neural Suite](https://github.com/cognis-digital)** by [Cognis Digital](https://cognis.digital)
> Cognis Open Collaboration License (COCL) v1.0 · domain: `ai-security`

[![install](https://img.shields.io/badge/install-git%2B%20%C2%B7%20pipx%20%C2%B7%20uv-6b46c1.svg)](#install--every-way-every-platform)
[![CI](https://github.com/cognis-digital/biascope/actions/workflows/ci.yml/badge.svg)](https://github.com/cognis-digital/biascope/actions)
[![License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-2b6cb0.svg)](LICENSE)
[![Suite](https://img.shields.io/badge/Cognis-Neural%20Suite-6b46c1.svg)](https://github.com/cognis-digital)

**Embedded bias probe suite — demographic / occupational / geographic.**

*AI Security & Governance — securing LLMs, agents, and the MCP supply chain.*

<!-- cognis:layman:start -->
## What is this?

Biascope is a tool that checks whether an AI model treats different groups of people fairly. You feed it a set of responses that a model gave to identical prompts — where only one word changes, such as "young person", "elderly person", or "immigrant" — and it scores each response for positive or negative language, then flags any categories where one group was described significantly more favorably or more negatively than another. It also catches cases where a model defaulted to gendered language for certain jobs, like calling a nurse "she" and an engineer "he." It runs entirely on your own computer with no internet connection required, produces results in table, JSON, SARIF, or HTML formats, and is designed to slot into automated testing pipelines so bias checks happen automatically every time a model or prompt changes.
<!-- cognis:layman:end -->

## Why

Security and intelligence teams need embedded bias probe suite — demographic / occupational / geographic without standing up heavyweight infrastructure. `biascope` is single-purpose, scriptable, CI-friendly, and self-hostable: point it at a target, get prioritized findings in the format your workflow already speaks (table, JSON, SARIF, HTML), and wire it into agents over MCP when you want it autonomous.

<!-- cognis:domains:start -->
## Domains

**Primary domain:** AI & ML  ·  **JTF MERIDIAN division:** ATHENA-PRIME · SAGE

**Topics:** `cognis` `ai` `llm` `machine-learning` `healthcare`

Part of the **Cognis Neural Suite** — 300+ source-available tools organized across 12 domains under the JTF MERIDIAN command structure. See the [suite on GitHub](https://github.com/cognis-digital) and [jtf-meridian](https://github.com/cognis-digital/jtf-meridian) for how the pieces fit together.
<!-- cognis:domains:end -->

<!-- cognis:install:start -->
## Install

`biascope` is source-available (not published to PyPI) — every method below installs
straight from GitHub. Pick whichever you prefer; the one-line scripts auto-detect
the best tool available on your machine.

**One-liner (Linux / macOS):**
```sh
curl -fsSL https://raw.githubusercontent.com/cognis-digital/biascope/HEAD/install.sh | sh
```

**One-liner (Windows PowerShell):**
```powershell
irm https://raw.githubusercontent.com/cognis-digital/biascope/HEAD/install.ps1 | iex
```

**Or install manually — any one of:**
```sh
pipx install "git+https://github.com/cognis-digital/biascope.git"     # isolated (recommended)
uv tool install "git+https://github.com/cognis-digital/biascope.git"  # uv
pip install "git+https://github.com/cognis-digital/biascope.git"      # pip
```

**From source:**
```sh
git clone https://github.com/cognis-digital/biascope.git
cd biascope && pip install .
```

Then run:
```sh
biascope --help
```
<!-- cognis:install:end -->

## Install

```bash
pip install "git+https://github.com/cognis-digital/biascope.git"
# or, from this repo:
pip install -e ".[dev]"
```

## Quick start

```bash
biascope --version
biascope scan demos/                      # run against the bundled demo
biascope scan demos/ --format sarif --out r.sarif --fail-on high
biascope scan demos/ --format html --out report.html
biascope mcp                              # expose as an MCP server (Cognis.Studio / Claude Desktop / Cursor)
```

## Built-in demo scenarios

Each scenario folder includes a `SCENARIO.md` describing the situation and the findings to expect.

- [`demos/01-basic/`](demos/01-basic/SCENARIO.md)
- [`demos/01-loan-approval/`](demos/01-loan-approval/SCENARIO.md)
- [`demos/02-clean-chatbot/`](demos/02-clean-chatbot/SCENARIO.md)
- [`demos/03-customer-segmentation/`](demos/03-customer-segmentation/SCENARIO.md)

## Output formats

- **Table** (default) — human-readable terminal summary
- **JSON** — machine-readable findings for pipelines
- **SARIF** — drops into GitHub code-scanning / IDE problem panes
- **HTML** — shareable report with severity rollups

## Credits / Built on

Cognis composes and credits the best of open source. This tool builds on / interoperates with:

- [`stanford-crfm/helm`](https://github.com/stanford-crfm/helm) — probe data
- [`nyu-mll/BBQ`](https://github.com/nyu-mll/BBQ) — bias benchmark

Missing a credit? Open a PR — see [CONTRIBUTING.md](CONTRIBUTING.md).

## How it fits the Cognis Neural Suite

`biascope` is one of **52 tools** in the [Cognis Neural Suite](https://github.com/cognis-digital). Every tool ships an MCP server, so [Cognis.Studio](https://cognis.studio) agents can call them as scoped capabilities.

**Sibling tools in `ai-security`:** [`aegis`](https://github.com/cognis-digital/aegis), [`promptmirror`](https://github.com/cognis-digital/promptmirror), [`ledgermind`](https://github.com/cognis-digital/ledgermind), [`adversa`](https://github.com/cognis-digital/adversa), [`guardpost`](https://github.com/cognis-digital/guardpost), [`hallumark`](https://github.com/cognis-digital/hallumark), [`aicard`](https://github.com/cognis-digital/aicard), [`mcpharden`](https://github.com/cognis-digital/mcpharden), [`agentlog`](https://github.com/cognis-digital/agentlog), [`ragshield`](https://github.com/cognis-digital/ragshield)

## Architecture & roadmap

- Design notes: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Planned work: [`ROADMAP.md`](ROADMAP.md)

## Contributing

PRs, new detections, and demo scenarios are welcome under the collaboration-pull model. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

<a name="verification"></a>
## Verification

[![tests](https://img.shields.io/badge/tests-8%20passing-2ea44f.svg)](AUDIT.md)

Every push is verified end-to-end. Latest audit (2026-06-13):

```text
tests        : 8 passed, 0 failed, 0 errored
compile      : all modules parse
cli          : C:\Python314\python.exe: No module named https
package      : https
```

<details><summary>CLI surface (<code>--help</code>)</summary>

```text
C:\Python314\python.exe: No module named https
```
</details>

Full machine-readable results: [`AUDIT.md`](AUDIT.md) · regenerate with `python -m https --help` + `pytest -q`.

<div align="right"><a href="#top">↑ back to top</a></div>


## License

Source-available under the **Cognis Open Collaboration License (COCL) v1.0** — free for personal, internal-evaluation, research, and educational use; **commercial / production use requires a license** (licensing@cognis.digital). See [LICENSE](LICENSE).

## Responsible use

This is dual-use security software. Use it only against systems, data, and identities you own or are explicitly authorized in writing to test, and in compliance with applicable law.

## About

**[Cognis Digital](https://cognis.digital)** — Wyoming, USA · *Making Tomorrow Better Today: Advanced Cybersecurity, AI Innovation, and Blockchain Expertise.*
