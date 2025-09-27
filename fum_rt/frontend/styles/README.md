# FUM Frontend Styles (Modular)

This package provides a modular CSS system for the Dash UI. Instead of a single monolithic CSS string, styles are layered and composed at runtime in a stable order.

Layering contract:
1) base: variables, resets, typography, form controls, scrollbars (no layout)
2) layout: grids, cards, responsive rules, utilities (no component overrides)
3) components: dcc.Dropdown/react-select, rc-slider, and component-specific rules

Exported API:
- from fum_rt.frontend.styles import get_global_css
- from fum_rt.frontend.styles import get_base_css, get_layout_css, get_components_css

## Usage

Inject the CSS into Dash index_string (already wired in app.py):

```python
from fum_rt.frontend.styles import get_global_css

GLOBAL_CSS = get_global_css()
app.index_string = app.index_string.replace("</head>", f"<style>{GLOBAL_CSS}</style></head>")
```

If legacy imports are still present elsewhere:
```python
# Backward compatible shim
from fum_rt.frontend.styles.theme import get_global_css
```
The shim forwards to the modular aggregator.

## Why modular?

- Separation of concerns:
  - base is safe, foundational, and broadly applicable
  - layout organizes structure and responsiveness
  - components encapsulate third‑party widget tweaks (react-select, rc-slider)
- Lower coupling: view-specific changes can be added without touching core layers
- Fewer regressions: targeted updates reduce incidental style bleed

## Files

- base.py
  - get_base_css(): CSS variables, resets, typography, form controls, scrollbars
- layout.py
  - get_layout_css(): grid/card/row utilities, responsive rules, minor layout helpers (e.g., .tight)
- components.py
  - get_components_css(): dropdown (react-select) and rc-slider styling, layering fixes (z-index), clipping fixes

- __init__.py
  - get_global_css(): concatenates base → layout → components in a fail-soft manner

- theme.py (deprecated shim)
  - Keeps old import path working by delegating to styles.get_global_css

## Adding view-specific styles

For a new view or composite component, there are two options:

1) Extend components.py (small and generic additions)
   - Ideal for adding minor UI polish or tweaking existing component rules.

2) Create a new module and opt-in at composition time
   - Create a new file (e.g., view_run_config.py) next to existing layers with:
     ```python
     def get_run_config_view_css() -> str:
         return '''
         /* styles specific to the run-config view */
         .run-config-advanced {
             display: grid;
             grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
             gap: 12px;
         }
         '''
     ```
   - Then import and append in __init__.py as a new layer after components:
     ```python
     from .view_run_config import get_run_config_view_css
     ...
     layers = [get_base_css, get_layout_css, get_components_css, get_run_config_view_css]
     ```
   - Keep the rule of thumb: more specific layers later in the list.

Note: If you expect multiple view-specific files, consider a subpackage (e.g., styles/views/) with a local __init__.py to assemble view layers, then include that combined view CSS at the end of the main list.

## Conventions and constraints

- No global scans, no schedulers: All CSS is static strings concatenated at build/start time.
- Respect existing className contracts in layout (e.g., className="grid").
- Keep base.css free of layout or component specifics to minimize interactions.
- Layout should not override third‑party components; that belongs in components.py.
- Use z-index sparingly; menu portals (react-select) need to sit above cards. This is handled in components.py.

## Responsive decisions (summary)

- The grid defaults to minmax(300px, 360px) 1fr for two-column layouts, with breakpoints:
  - ≤1200px: left column narrows slightly
  - ≤900px: stacks to a single column
- Cards allow overflow: visible for dropdowns and menus (prevents clipping).
- Inputs and long text are clamped with max-width: 100% to prevent layout shifts.

## Duplicate rule sanity

- By design, base/layout/components do not duplicate selectors with conflicting declarations.
- If you add view-specific rules, keep selector specificity scoped (e.g., prefix with a container class for the view) to avoid broad overrides.
- In case of an intentional override, place it later in the layer order.

## Example: switching from legacy

Before:
```python
from fum_rt.frontend.styles.theme import get_global_css
```

After (preferred):
```python
from fum_rt.frontend.styles import get_global_css
```

Legacy imports continue to function via the shim.

## Governance

- Any proposal to add a new layer must justify why existing layers cannot host the rules.
- Maintain the base → layout → components → views ordering to preserve determinism.
- Target changes to the minimal layer that owns the concern.

Author: Justin K. Lietz