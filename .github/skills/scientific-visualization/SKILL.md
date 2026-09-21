---
name: scientific-visualization
description: Creates accurate, reproducible scientific figures matched to the analytical question, data structure, audience, and target venue. Use for /scientific_visualization or figure creation and review.
---

# Scientific visualization

Read the underlying data or result artifact, analysis code, intended claim, uncertainty definition, and venue requirements before plotting.

## Principles
- Choose the plot from the question and data structure.
- Show independent units or distributions where practical; do not hide variability behind bars.
- Define denominators, transformations, error bars, confidence intervals, and statistical annotations.
- Use consistent, accessible encodings and verify readability at final size.
- Avoid misleading axes, inappropriate smoothing, excessive precision, and duplicated information.
- Preserve provenance from source data through plotting code to exported figure.

## Workflow
1. Verify that the source output is current.
2. Build the figure with a deterministic script and project configuration.
3. Check labels, units, sample counts, legends, panels, and accessibility.
4. Export the formats and dimensions required by the target venue.
5. Create or update the caption from actual plotted content and analysis results.
6. Link the figure to its source script, data, DVC stage, and manuscript claim in the evidence map when appropriate.

Never fabricate data for a project figure or add significance annotations unsupported by the analysis.
