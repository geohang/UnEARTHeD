This is a non-functional design preview made for a proposal figure: it holds sample data only, and no computation is performed.

# UnEARTHeD · design preview

**Live page:** https://geohang.github.io/UnEARTHeD/

UnEARTHeD is a proposed service that turns archived near-surface geophysical surveys into the subsurface quantities Earth scientists use: bedrock depth, water storage, root-accessible water, reactive-zone thickness, regolith thickness. Each product comes with its uncertainty and a record of how it was produced, and is defined the same way at every site so results compare across sites.

This repository shows the interaction design only. Every site, survey, number, timestamp, token count and evaluation result on the page is illustrative, and the basemap is fictional. Nothing is uploaded, computed or deposited, and the page makes no network requests.

## How the page is organised

The page has three levels, built for three readers: a first-time reviewer, a scientist who is not a geophysicist, and a geophysicist who wants the full catalog. The product comes first, the method second and the machinery last.

1. **Front door** (`#/`). A headline, a map of the sample sites with a site list beside it, five cards that each start from a community's question, three facts about the catalog, and a plain link into the full catalog. Entry is by place or by question.
2. **Community views** (`#/community/hydrology`, and likewise `geomorphology`, `forest-ecology`, `biogeochemistry`, `natural-hazards`). Each opens with its question, lists the products it gets (units, depth range, methods), maps the sites as ready, partial or not supported (each naming the missing input), shows an example result with its uncertainty in that community's own quantity and units, says what makes the product comparable across sites, and opens the workspace with site, question and product already set.
3. **Workspace** (`#/workspace/SRV-0142?c=hydrology&p=storage`). The catalog on the left, the record cards on the right. In the middle: what the site can and cannot produce (each with the input it has or lacks), the request, the result, then the analysis plan with the origin of every parameter (measured, curated metadata, file header or inferred). A product that cannot be made is refused, with the missing input named.

The disclosure "How this was produced" holds the machinery: the **Use curated site metadata** toggle, structured output by constrained decoding against a plan schema (viewable as JSON), the planner model tier with its token budget and spend, prompt caching, retrieval-augmented parameter grounding with citations on inferred values, tool calling limited to registered tools, the context assembled for the request, deterministic execution in a pinned environment, and the evaluation against acceptance criteria on a held-out subset of the catalog.

Turning curated metadata off is the key interaction: the reported uncertainty widens, and the parameters that came from curated metadata switch to inferred.

Other interactions are presentation only: hovering or arrowing through a cross-section reads out position, depth and value; the length unit switches between metres and feet; cards open and close; and the page follows the system light or dark appearance. Browser back and forward work, and every view can be linked directly.

## The library underneath

The computation this interface would drive already exists in [PyHydroGeophysX](https://github.com/geohang/PyHydroGeophysX), an open-source Python package (Chen, Niu and Wu, 2026, *SoftwareX* 34, 102710, https://doi.org/10.1016/j.softx.2026.102710). Each method, plan row, panel and tool on the page carries a small link to the file in that repository that implements it, and the passages cited by inferred plan values are quoted from its source.

The tool names in the workspace are the ones registered in the library's tool registry, `PyHydroGeophysX/agents/runtime/catalog.py`: `load_ert_surveys`, `invert_ert`, `pick_first_breaks`, `invert_seismic`, `extract_seismic_interfaces`, `process_gpr_line`, `invert_tdem`, `convert_water_content` and `write_report`. `propagate_uncertainty` is implemented in the library (`uncertainty/posterior.py`) but is not yet in that registry. Signatures follow the functions that implement each tool.

## Files

- `index.html`: the whole preview, with HTML, CSS and JavaScript inline, and the map and cross-sections drawn as inline SVG. No build step, frameworks, images or external requests.
- `.nojekyll`: tells GitHub Pages to serve the files as they are.

## Viewing it locally

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8000
```

then visit http://localhost:8000. Links such as `index.html#/community/forest-ecology` or `index.html#/workspace/SRV-0119?c=hydrology&p=storage` open a view directly; links in the old `#analyze/SRV-0142` form still land in the workspace.

## Deployment

GitHub Pages serves the repository root from the `main` branch.
