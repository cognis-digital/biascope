# Cognis interop map

How **biascope** fits the wider Cognis suite — a composable set of defensive, analytical
tools that all run on your own hardware and speak plain **JSON** (or an OpenAI-compatible
**`/v1`**). `biascope` lives in the **Geospatial / GEOINT** cluster.

```mermaid
graph LR
  subgraph infra["AI backbone (private)"]
    EM[edgemesh]:::hub
    MR[modelroute]; UF[uncensored-fleet]; CC[cognis-code]
    MR --> EM; UF --> EM; CC --> EM
  end
  subgraph cog["Agents + cognition"]
    AL[agentlex]; HM[humind]; AS[agentsmith]; EN[engram]
    HM -- speaks --> AL; AL -- facts --> HM; AS -- orchestrates --> AL; EN --- HM
  end
  subgraph dom["Domain intelligence"]
    MI[maritimeint]; GEO[geoint]; FIN[ownership/finance]; TI[threat-intel]; DR[drone/C-UAS]
  end
  EM -- "/v1 add-ins" --> dom
  EM -- "/v1 enrichment" --> cog
  dom -- "findings as messages" --> cog
  classDef hub fill:#6b46c1,color:#fff;
```

## Key edges

| from | relation | to |
|---|---|---|
| `biascope` | JSON findings compose with | [`locateanything`](https://github.com/cognis-digital/locateanything), [`geolens`](https://github.com/cognis-digital/geolens), [`geoaoi-pro`](https://github.com/cognis-digital/geoaoi-pro) |
| `biascope` | AI add-ins are served `/v1` by | [`edgemesh`](https://github.com/cognis-digital/edgemesh) (your fleet) |
| `biascope` | findings can be narrated / reasoned over by | [`humind`](https://github.com/cognis-digital/humind) -> [`agentlex`](https://github.com/cognis-digital/agentlex) |
| `biascope` | export to intel formats via | [`stixgen`](https://github.com/cognis-digital/stixgen) (STIX) / [`attackmap`](https://github.com/cognis-digital/attackmap) (ATT&CK) |

## Composition patterns

Everything reads/writes JSON, so tools chain with ordinary pipes; nothing leaves the box.

**1 — chain within the geospatial / geoint cluster.** `biascope` output feeds the next tool:
```bash
biascope ... --format json > out.json          # this tool's findings (see `biascope --help`)
locateanything ... < out.json                      # the cluster sibling consumes them
```

**2 — enrich with the private-AI backbone.** Point add-ins at one `/v1` for the whole fleet:
```bash
export OPENAI_BASE_URL=http://localhost:8080/v1   # an edgemesh gateway over your fleet
biascope ...                                         # vision / reasoning add-ins light up
```

**3 — export findings to your SOC's formats.**
```bash
biascope ... --format json | stixgen from-json > bundle.stix.json   # STIX 2.1
biascope ... --format json | attackmap map > attack.json            # ATT&CK techniques
```

**4 — narrate through cognition + agents.** `humind` extracts salience from `biascope`'s
output; `agentlex` holds it as KB facts and fires Horn rules to escalate. `biascope` slots
into the **GEOINT fusion**, **Threat-intel export** stacks below.

## Reference stacks

Pick the smallest stack that answers your question; each is a subset of the 300+ suite.

| Stack | Representative repos | Flow |
|---|---|---|
| **Sanctions-evasion screening** | maritimeint + OFAC/OFSI/EU/OpenSanctions feeds | importers -> screen -> pass/fail gate |
| **GEOINT fusion** | locateanything - geolens - geoaoi-pro | imagery -> geolocate -> plot on AOI / MIL-STD-2525 |
| **Ownership & finance** | corpmap - cryptotrace - personagraph | entity -> beneficial owner -> wallets -> identity |
| **Threat-intel export** | stixgen - iocextract - attackmap - ttphunt | findings -> STIX / IOCs -> ATT&CK -> hunt |
| **Counter-UAS maritime** | maritimeint - uaslog - awesome-drone-warfare-osint | AIS + drone telemetry -> correlated picture |
| **Cognition + agents** | humind - agentlex - agentsmith - engram | extract -> KB facts/rules -> orchestrate -> memory |
| **Private-AI backbone** | edgemesh - modelroute - uncensored-fleet - cognis-code | one `/v1` powering every tool's add-ins |

Every domain stack sits **on top of** the private-AI backbone: point any tool's add-ins at
an `edgemesh` gateway (`OPENAI_BASE_URL`) and one fleet serves vision, reasoning, and
narration to all of them.

> Part of a cross-repo interop pass. **300+ tools ->** [github.com/cognis-digital](https://github.com/cognis-digital) - [awesome-cognis](https://github.com/cognis-digital/awesome-cognis)
