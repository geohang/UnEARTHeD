This is a non-functional design preview made for a proposal figure: it holds sample data only, and no computation is performed.

# UnEARTHeD · design preview

**Live page:** https://geohang.github.io/UnEARTHeD/

UnEARTHeD is a proposed service for Earth scientists who are not geophysicists. A user picks an archived near-surface geophysical survey from a curated catalog, says in plain language what they want, and receives a subsurface product (for example water content) with its uncertainty and a full record of how it was produced.

This repository shows the interaction design only. Every survey, number, timestamp, token count and evaluation result on the page is illustrative. Nothing is uploaded, computed or deposited, and the page makes no network requests.

## What the page shows

- **Browse**: the catalog of sample surveys (electrical resistivity, seismic refraction, ground-penetrating radar), each with data-quality and metadata-completeness chips.
- **Analyze**: a three-column workspace. On the left, the catalog. In the middle, the request, the analysis plan (each value labelled measured, curated metadata, file header or inferred), and the water-content cross-section with its uncertainty panel. On the right, the record cards: `Provenance`, `Uncertainty`, `Publish`, `Orchestration`, `Evaluation` and `What runs underneath`.
- **Results**: the product as a user would receive it.
- **Orchestration**: how a language model would act as the planner. It shows capability tiers with context window and token budget, prompt caching, structured output by constrained decoding against a plan schema (viewable as JSON), tool calling limited to registered tools, retrieval-augmented parameter grounding with citations on inferred values, the context assembled for the request, and deterministic execution in a pinned environment with no model in the loop.
- **Evaluation**: the acceptance gate an offline eval harness would apply to a plan, measured on a held-out subset of the catalog. The values shown are sample values.

Interactions are presentation only: selecting a survey swaps the sample content, the segmented control switches views, cards open and close, hovering a cross-section reads out position, depth and value, and the length unit switches between metres and feet. The page follows the system light or dark appearance.

## The library underneath

The computation this interface would drive already exists in [PyHydroGeophysX](https://github.com/geohang/PyHydroGeophysX), an open-source Python package (Chen, Niu and Wu, 2026, *SoftwareX* 34, 102710, https://doi.org/10.1016/j.softx.2026.102710). Each method, plan row, panel and tool on the page carries a small link to the file in that repository that implements it.

The tool names in the Orchestration card are the ones registered in the library's tool registry, `PyHydroGeophysX/agents/runtime/catalog.py`: `load_ert_surveys`, `invert_ert`, `pick_first_breaks`, `invert_seismic`, `extract_seismic_interfaces`, `process_gpr_line`, `invert_tdem`, `convert_water_content` and `write_report`. `propagate_uncertainty` is implemented in the library (`uncertainty/posterior.py`) but is not yet in that registry. Signatures follow the functions that implement each tool.

## Files

- `index.html`: the whole preview, with HTML, CSS and JavaScript inline and the cross-sections drawn as inline SVG. No build step, frameworks, images or external requests.
- `.nojekyll`: tells GitHub Pages to serve the files as they are.

## Viewing it locally

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000
```

then visit http://localhost:8000. A view and survey can be linked directly, for example `index.html#results/SRV-0142`.

## Deployment

GitHub Pages serves the repository root from the `main` branch.
