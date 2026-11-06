# Design directions

These recipes are interpretations of the collection, not exact design-system specifications. Choose colors, dimensions, and motion values for the actual project. S IDs resolve in [source-index.md](source-index.md); L IDs resolve in [motion-and-links.md](motion-and-links.md).

## Soft utility

**Start with:** S03, S09, S10, S11, S12. Use for dashboards, personal tools, financial summaries, setup flows, and discovery surfaces.

- Put white or near-white surfaces on a subtly different neutral canvas. Define large regions with spacing and shape, then use a fine border or restrained shadow where necessary.
- Give each metric a large readable value, short label, and subordinate unit or comparison. S09's dimmed fractional digits are a hierarchy idea, not permission for illegible text.
- Use a visibly filled primary action and quieter secondary actions. Pills fit short filters/actions; longer content belongs in a larger, less pill-shaped surface.
- Maintain coherent nested radii. For an inset panel, begin with the outer radius minus the inset, then adjust optically. Do not assign the same large radius to every layer.
- Group tasks semantically: S10's checklist, S12's discovery cards, and S09's transaction rows should remain different components.
- S09's light summary above dark activity expresses an information boundary. Use such contrast where it helps people understand the content.

**Characteristic detail:** one luminous metric card, carefully drawn progress states, or a distinct light/dark sectional boundary.

**Adaptation:** allow filters to wrap or scroll intentionally with an affordance; collapse grids without truncating names; keep sticky actions clear of content and safe areas. Horizontal preview cards suit a collection to browse, not a required form field.

## Luminous instrument

**Start with:** S02, S05, S06 and L01. Use for focused live activity, audio/AI presence, measured progress, and an expressive hero module.

- Begin with near-black and restrained charcoal controls. Make one luminous object or active panel the focal point.
- Build depth from a dark body, colored rim or reflection, and soft inner highlight. S05/S06 put bright color near an edge while leaving a quiet center for labels.
- Keep geometry simple: sphere, rounded panel, circular button, short pill. The material supplies expression; competing outlines and shadows weaken it.
- Dot matrices suit a hero visualization, compact markers, or decorative display numerals. Keep navigation, body copy, and essential data conventionally readable. Provide accessible text values for custom-drawn numbers.
- Use actual data and units when a visualization represents measurements; otherwise identify it as decorative. Do not infer a data model or physiological behavior from the breathing-app mockups.

**Characteristic detail:** an orb with moving internal light, an edge-lit panel, or a sparse dot field. Choose the detail that serves the screen's purpose.

**Adaptation:** use a lightweight gradient or original pre-rendered asset when real-time optics add little value. Pause ambient animation offscreen; retain a pleasing static state. The reference's dim secondary text is not an accessibility target.

## Airy editorial

**Start with:** S07, S08, S13 and L02. Use for onboarding, plans, portfolios, product stories, and marketing pages.

- Let a strong image, object, or typographic idea carry the composition. Use broad quiet margins and purposeful gaps rather than filling every section with cards.
- S07 pairs a display serif headline with sans-serif controls. S08/S13 show that expressive layouts can use restrained sans-serif throughout. Choose for the product identity; do not infer an exact font from an image.
- Keep headline, explanation, and action in a clear reading sequence. Use the product's actual benefit and believable content instead of copying reference slogans.
- Place a saturated, tactile object against a neutral field. Supporting content can remain nearly monochrome.
- L02 places an animated people/network scene above a static message and compact actions. Borrow this separation of expressive scene and readable interface.
- Give stacked sections a narrative appropriate to the product. Do not impose a fixed landing-page template on unrelated content.

**Characteristic detail:** a grainy light field, original sculptural object, strong photograph, or distinctive type pairing.

**Adaptation:** preserve the visual subject and copy hierarchy on small screens instead of scaling down a desktop screenshot. Keep the last feature and legal text reachable behind sticky actions. A blurred excerpt needs a real expand action and must not obscure essential information.

## Atmospheric workflow

**Start with:** S01, S04, S08, S12 and L05. Use for workflow explanations, agent activity, integration showcases, or selected overlays.

- Separate controls from a softly lit environment. S01 uses warm imagery and nearly square panels; S04 uses teal light and rounded nested surfaces. These are distinct geometry choices.
- Show relationships with aligned connectors, concise labels, and clear states. Keep connectors behind nodes and clear of text; simplify on narrow screens.
- Translucent surfaces need enough fill for readability, a subtle boundary, and background detail that gives transparency something to reveal.
- For S12-style integration cards, put artwork in a distinct media region and text in a plain reading region. Show integrations the product actually supports.
- L05's blue folder is a material study. A Blender rendering does not establish that a single CSS blur or native material can reproduce its optics.

**Characteristic detail:** warm glass over a scene, a luminous process node, or a frosted object. Keep task controls easy to read and operate.

**Adaptation:** provide opaque surfaces when transparency is unavailable or reduced. Avoid stacked backdrop blurs across every row. A reference's illustrated “Approve & send” is not authorization to send anything; actual workflows follow the product's requirements.

## Material and motion recipes

Read [motion-and-links.md](motion-and-links.md) for evidence and live references before matching a specific effect.

| Pattern | Implementation direction | Preserve |
| --- | --- | --- |
| Luminous card | Layer a radial or mesh-like color field inside the silhouette, a quiet body, and a fine highlight | Readable center, coherent lighting, clipped decoration |
| Frosted overlay | Native material or supported backdrop blur with translucent fill and opaque fallback | Sharp content, contrast over changing backgrounds |
| Progressive blur | Regionally varying blur through masked layers or an appropriate shader | Clear-to-frosted progression, bounded rendering cost |
| Orb | Simple shaded geometry first; shader when animated refraction is central | Sphere silhouette, coherent lighting, static fallback |
| Dot field | Compact drawing surface or reusable vector pattern | Accessible equivalent, limited redraws, stable layout |
| Liquid carousel | Stable semantic item order and controls; distortion on transitioning imagery | Keyboard/touch navigation, settled readability, reduced motion |
| Progress indicator | Distinct determinate, indeterminate, complete, and waiting states | Truthful status, non-color distinction, text where needed |

Do not infer animation curves from still images. If timing is unavailable, label it as an implementation choice. Rough starting points are 120–220 ms for direct feedback and 220–400 ms for small panel transitions; these are tunable proposals, not measurements of the references. Expressive transitions may take longer but must not delay input.

## Platform translation

**Web:** use semantic controls, responsive layout, and CSS tokens before effects. Keep decorative overlays non-interactive, preserve visible focus, and expose status changes accessibly. Isolate canvas/WebGL as an enhancement with a static fallback. Keep navigation usable without it. Prefer the existing motion system; check current docs for new libraries.

**Native Apple apps:** retain native navigation, safe areas, text scaling, accessibility, and desktop keyboard behavior. Use materials and animation primitives supported by the deployment target; resolve APIs against the actual SDK. Translate visual relationships rather than hard-coding screenshot dimensions. Respect reduced motion/transparency. Dense desktop tools should remain efficient; mobile hero proportions do not dictate every inspector or table row.

**Other native or cross-platform apps:** retain platform conventions. Reproduce the visual idea with an appropriate primitive; a linked React component is not automatically compatible.

## Compare the result

Check hierarchy, spacing rhythm, silhouette, lighting, and restraint. The result should feel intentionally related even after changing colors and content. If the only resemblance is a gradient, revisit composition and proportions before adding more blur.
