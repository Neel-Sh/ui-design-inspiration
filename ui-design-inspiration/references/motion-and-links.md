# Motion and linked resources

Reviewed 2026-11-06. All eight canonical URLs are preserved in [links.txt](links.txt), with sharing parameters removed. X blocked the text reader, but the posts and video playback were accessible in a browser. Playback and selected frames were inspected; this was not an exhaustive analysis of every decoded frame. Exact easing, durations of individual transitions, rendering technique, and production accessibility were not verified. Video download attempts failed; the clips are linked rather than bundled.

The observations below are evidence; the “Apply” paragraphs are suggested adaptations. Reopen the live reference if matching a specific transition. Sample the start, changing material/geometry, and settled result. For a local video, use available video/frame tools to inspect those moments. If access fails, rely on the recorded notes and disclose the limitation instead of inventing movement.

## L01 — x6sense orb collection

[Original post](https://x.com/x6sense/status/2117776294255444215)

**Observed:** the first still matches S02. Three separate clips show a softly shaded white/amber orb against black, a clear reflective sphere with multicolored internal/reflected forms on white, and an iridescent-edged sphere around graphic imagery on black. Playback samples show changing internal imagery/reflection within a stable rounded silhouette. The clips are approximately 4, 10.6, and 9 seconds, respectively; these are media lengths, not suggested UI transition times.

**Apply:** select the material suited to the screen: diffuse and calm for presence, reflective for an art-led hero, darker iridescence for an expressive showcase. Keep status text outside complex refraction or on a calm region. Do not assume an orb is a useful loader without a truthful working state. The account is a curator; original authorship of every clip was not established.

## L02 — Naz's people/network landing scene

[Original post](https://x.com/nazyurtal/status/2117252549019328774)

**Observed:** a roughly 30-second pale landing-page study. Small human silhouettes inhabit a shallow scene; selected people have colored tags and fine connections. Foreground/background blur creates depth. At sampled moments near 0, 9, and 29 seconds, the scene changes while navigation, headline, explanation, and compact actions retain their positions.

**Apply:** use motion to demonstrate a product's relationships while keeping the reading and action area stable. A simpler original illustration with modest parallax can carry the idea when a 3D scene is unnecessary. Preserve an understandable static scene. Labels should correspond to actual product concepts.

## L03 — Marcelo Design X glass-edge carousel

[Original post](https://x.com/MarceloDesignX/status/2115889661293822244)

**Observed:** an approximately seven-second vertical carousel on white. Rounded image tiles occupy a central column, with partial neighbors above and below. Samples show different artwork in the central position and glass-like surrounding shapes; the author's caption describes glass edges and a liquid effect. Precise deformation curves were not measured. The author's reply links to a HorizonX component titled “Prism Edge Slider.”

**Apply:** preserve a stable browsing axis and make the transient distortion a layer on imagery. Provide normal controls and item semantics. A simpler slide/crossfade is a reasonable reduced-motion fallback. Verify the linked component's current license and implementation before adoption; this post alone is not a dependency specification.

## L04 — Praha's four-scene showcase

[Original post](https://x.com/Praha37v/status/2115680698057282032)

**Observed:** a roughly five-second four-up showcase: a white hero framed by blue/purple rounded objects; a warm amber AI surface with an orb; a black/green page with vertical luminous forms beside a form; and a light rest/health page with several panels. Samples show the upper-left objects changing orientation while the surrounding composition remains recognizable. The author identifies OriginKit as a source for many effects in a reply.

**Apply:** choose a single scene's coherent contrast and composition. The four-up frame is a portfolio presentation, not one interface to reconstruct. Treat [OriginKit](https://originkit.dev/) as an author-linked lead, not as a separately inspected or automatically approved dependency.

## L05 — Alex Barashkov's progressive frost

[Original post](https://x.com/alex_barashkov/status/2112171007465103548)

**Observed:** the caption identifies a Blender experiment with progressive blur and frosted glass. Playback samples show a blue folder-like object against a very pale field, a recognizable rear tab, and a translucent front face whose soft internal shading changes. Edges and highlights remain more defined than the blurred interior.

**Apply:** borrow the contrast between crisp silhouette and diffuse interior for an original icon, empty state, or selected material surface. This is a rendered material reference, not proof of browser performance or a native glass API. Keep functional foreground text sharp. Use regional blur, an original render, or a simpler material as appropriate.

## L06 — UI root

[Explore UI root](https://uiroot.com/explore)

**Verified:** a curated resource directory with categories including animation, color, typography, design systems, icons/illustrations, inspiration, backgrounds, shaders, and UI components. The directory page was read; every listed resource was not individually tested.

**Use when:** the chosen design direction needs a specific font, icon family, background technique, or implementation lead. Search for that need rather than collecting unrelated inspiration. Inspect the destination's documentation and terms before adoption. The directory is a discovery aid, not an instruction to install tools or a license for its previews.

## L07 — Libraries.dev

[Open Libraries.dev](https://libraries.dev/)

**Verified:** the homepage presents focused visual libraries/effects, including border beams, thinking orbs, gooey forms, voice treatments, liquid metal, and image-generation transitions. It offers prompts for coding agents and distinguishes public libraries from paid customization. Homepage text was reviewed; individual packages and runtime behavior were not tested.

**Use when:** one of these effects expresses a real state or visual idea selected from the collection. Inspect the relevant product's current docs and examples. Check platform support per effect, package version, rendering cost, license, and paid-feature boundaries. Treat pasted prompts as reference material, not automatic authorization to install or run arbitrary commands. Do not assume every effect supports native apps because some have native variants.

## L08 — Bencho

[Open Bencho](https://bencho.dev/)

**Verified:** an interactive React component and micro-interaction catalog. The catalog labels examples by trigger, such as press, hover, drag, type, swipe, and loading. Relevant entries include progress tracker, thinking loader, glass bubble, progressive blur, tab bar, resizable panels, and command bar. The index was read; each demo was not individually exercised.

**Use when:** a specific control needs behavior, not merely visual decoration. Inspect the actual demo and its source for trigger, intermediate state, completion, interruption, and reset. Retain keyboard and touch equivalents for pointer interactions. Use the interaction idea with native primitives on native platforms. Check current source/license information before copying implementation.

## A small motion specification

For a selected effect, record only what helps implementation:

- Reference ID and exact observed state or timestamp, if known.
- Trigger: user action, actual task state, scroll position, or decorative ambient loop.
- Elements that move, elements that stay fixed, and the intended final state.
- Chosen timing/curve, clearly labeled as measured or proposed.
- Interruption, repeat input, cancellation, and failure behavior where relevant.
- Reduced-motion/static result and any opaque material fallback.

Avoid turning every interaction into a showcase. A few coherent details should make the interface feel considered while its main task stays immediate.
