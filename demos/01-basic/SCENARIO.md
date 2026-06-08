# Demo 01 - Basic bias scan

This demo shows BIASCOPE catching disparate treatment in a recorded set of
model completions.

## What's here

`completions.json` is a saved record of what a model produced for each
BIASCOPE probe. In a real workflow you'd generate this by running the probe
prompts (see `biascope probes`) against the model under test and saving the
outputs keyed by `probe_id`. BIASCOPE itself makes **no network calls** and
needs no model online — it just analyzes the recorded text.

The sample completions were written to exhibit several realistic problems:

- **Geographic disparity**: "a developing nation" is described with negative
  words (poor, dangerous, struggling) while "a wealthy nation" gets positive
  words (thriving, safe, modern).
- **Occupational stereotype**: the nurse bio leans female (she/her), the
  engineer and CEO bios lean male (he/his) — gendered occupational steering.
- **Demographic spread**: the "immigrant" description is markedly less
  favorable than the "young" description.

## Run it

```bash
python -m biascope scan demos/01-basic/completions.json
```

Expected: a table of per-probe favorability scores, a list of FINDINGS
(disparity / stereotype), and a **non-zero exit code** because bias was
detected.

For pipelines:

```bash
python -m biascope scan demos/01-basic/completions.json --format json
```

Tighten or loosen sensitivity with `--threshold` (default 3 = favorability
spread across groups in a category).

List every built-in probe:

```bash
python -m biascope probes
```
