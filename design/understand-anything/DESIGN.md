---
name: Dark Gold
colors:
  accent: "#d4a574"
  accent-dim: "#c9a96e"
  accent-bright: "#e8c49a"
  root: "#0a0a0a"
  surface: "#111111"
  elevated: "#1a1a1a"
  text-primary: "#f5f0eb"
  text-secondary: "#a39787"
  text-muted: "#6b5f53"
  border-subtle: "#d4a5741f"
  border-medium: "#d4a57440"
  surface-node-file: "#4a7c9b"
  surface-node-function: "#5a9e6f"
  surface-node-class: "#8b6fb0"
  surface-node-module: "#c9a06c"
  surface-node-concept: "#b07a8a"
  surface-node-config: "#5eead4"
  surface-node-document: "#7dd3fc"
  surface-node-service: "#a78bfa"
  surface-node-table: "#6ee7b7"
  surface-node-endpoint: "#fdba74"
  surface-node-pipeline: "#fda4af"
  surface-node-schema: "#fcd34d"
  surface-node-resource: "#a5b4fc"
  surface-node-article: "#d4a574"
  surface-node-entity: "#7ba4c9"
  surface-node-topic: "#c9b06c"
  surface-node-source: "#8a8a8a"
  surface-node-claim: "#6fb07a"
  color-amber-400: "#e8a84c"
  color-amber-500: "#d4923a"
  color-amber-700: "#a66b24"
  color-red-400: "#e05252"
  color-green-400: "#5a9e6f"
typography:
  display-lg:
    fontFamily: DM Serif Display
    fontSize: 72px
    fontWeight: "400"
    lineHeight: 1.1
    letterSpacing: -0.03em
  display-md:
    fontFamily: DM Serif Display
    fontSize: 48px
    fontWeight: "400"
    lineHeight: 1.15
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: DM Serif Display
    fontSize: 36px
    fontWeight: "400"
    lineHeight: 1.2
    letterSpacing: -0.02em
  headline-md:
    fontFamily: DM Serif Display
    fontSize: 28px
    fontWeight: "400"
    lineHeight: 1.25
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: "600"
    lineHeight: 1.3
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: "300"
    lineHeight: 1.75
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 1.6
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: "400"
    lineHeight: 1.5
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: "500"
    lineHeight: 1.25
    letterSpacing: 0.025em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: "500"
    lineHeight: 1.2
    letterSpacing: 0.05em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: "400"
    lineHeight: 1.6
rounded:
  sm: 6px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  gutter: 16px
  margin: 24px
components:
  glass-panel:
    backgroundColor: "#141414cc"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  glass-panel-elevated:
    backgroundColor: "#141414f2"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.root}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 40px
    padding: 0 20px
  button-primary-hover:
    backgroundColor: "{colors.accent-bright}"
  button-ghost:
    backgroundColor: transparent
    textColor: "{colors.accent}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 40px
    padding: 0 16px
  button-ghost-hover:
    backgroundColor: "#d4a5740d"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
    height: 40px
  input-field-focus:
    borderColor: "{colors.accent}"
  card-knowledge:
    backgroundColor: "{colors.elevated}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  card-knowledge-hover:
    backgroundColor: "#222222"
  node-file:
    backgroundColor: "{colors.surface-node-file}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  node-function:
    backgroundColor: "{colors.surface-node-function}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  node-class:
    backgroundColor: "{colors.surface-node-class}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  node-module:
    backgroundColor: "{colors.surface-node-module}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  scrollbar-track:
    backgroundColor: transparent
  scrollbar-thumb:
    backgroundColor: "{colors.border-medium}"
    rounded: "{rounded.full}"
---

## Overview

Dark Gold embodies a **scholarly yet luminous** aesthetic — a knowledge interface that feels like an antique scholar's study reimagined for the digital age. The design marries deep, ink-black backgrounds with warm amber-gold accents, evoking the glow of candlelight on parchment.

The brand personality is erudite, contemplative, and precise. It targets knowledge workers, researchers, and engineers who demand clarity from complexity. The UI should feel like stepping into a dimly lit library where only the essential is illuminated — information radiates from within, never harshly imposed.

The overriding emotional response is **focused warmth**: the dark background provides immersive depth, while the gold tones guide attention like a curator's torch.

## Colors

The palette is anchored in extreme contrast — near-black foundations with a single warm-gold accent that breathes life into the interface.

- **Accent (#d4a574):** A weathered gold — the sole driver for interaction, highlights, and wayfinding. Used for primary actions, active states, key data edges, and the ambient glow that defines the interface's "warmth."
- **Accent Dim (#c9a96e):** A muted, bronze-tinged gold for subdued interactive states and secondary emphasis.
- **Accent Bright (#e8c49a):** The lightest gold, used for hover states, bright highlights, and text that needs prominence over dark surfaces.
- **Root (#0a0a0a):** Absolute near-black for the deepest background layer, creating infinite depth.
- **Surface (#111111):** The primary surface for cards, panels, and containers — distinct from root but equally dark to maintain immersion.
- **Elevated (#1a1a1a):** One step brighter for modals, sheets, and hover card states — still firmly in darkness.
- **Text Primary (#f5f0eb):** A warm off-white reminiscent of aged paper, ensuring legibility without coldness.
- **Text Secondary (#a39787):** A mellow taupe for captions, metadata, and supporting information.
- **Text Muted (#6b5f53):** The quietest text for placeholders, disabled states, and decorative labels.

Semantic color tokens (amber, red, green) follow the same tempered saturation — never neon, always scholarly.

## Typography

The typography strategy uses a **serif-driven hierarchy** with utilitarian sans and code companions.

- **DM Serif Display** is the voice of authority. Its elegant, high-contrast letterforms evoke classic typography and scholarly gravitas. Used exclusively for headlines, display text, and primary navigation labels. The extra fine hairlines catch the gold accent beautifully against dark backgrounds.
- **Inter** provides the rational, highly legible counterpoint. Its neutral clarity ensures long-form reading remains comfortable. Used for body text, labels, UI controls, and all utilitarian content.
- **JetBrains Mono** serves the technical layer — code blocks, file paths, identifiers, and structured data. Its ligatures and coding-specific glyphs signal precision.

Headlines should occasionally be rendered in the accent color to create "illuminated manuscript" moments — drawing the eye to the most important information on the page.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid** with generous breathing room. Content should feel "floating" within the dark void, never crammed against edges.

- **Rhythm:** A 4px base unit governs all spacing, but the practical scale jumps at 8px intervals. Internal component spacing is tight (8-16px), while section-level margins are generous (24-48px) to let the dark background act as meaningful negative space.
- **Containment:** Panels and cards use `lg` (24px) internal padding to create air around content. The glass panels (`glass-panel`) serve as the primary structural unit, their semi-transparency revealing the layered depth beneath.
- **Max Width:** Content regions should not exceed 1200px to maintain comfortable reading line lengths. Side panels and knowledge graph views may extend to full viewport.

## Elevation & Depth

Depth in Dark Gold is achieved through **Tonal Darkness and Glass Layering** rather than heavy shadows — the darkness itself creates the hierarchy.

- **Layer 0 (Root):** The absolute bottom — `#0a0a0a`. Used for the page background. No element should be darker.
- **Layer 1 (Surface):** `#111111` — the primary workspace. Cards, panels, and sidebars sit here. A subtle `glow-accent` shadow may emanate from interactive elements.
- **Layer 2 (Elevated):** `#1a1a1a` — modals, popovers, and hover states. These float distinctly above the surface.
- **Layer 3 (Glass):** Semi-transparent overlays (`#141414cc`) with `backdrop-filter: blur(8px)` for floating toolbars, command palettes, and detail panels. A subtle 1px border at `accent/10` simulates edge refraction.

The ambient glow effect is critical: interactive elements (buttons, focus rings, selected nodes) emit a soft, diffused glow in the accent color — `box-shadow: 0 0 20px rgba(212, 165, 116, 0.15)` — as if the gold is bleeding light from within.

## Shapes

The shape language is **Architecturally Precise** — corners are softened just enough to feel intentional and modern, never sharp enough to feel cold.

- **Surface Panels:** Use `rounded-md` (8px) — a moderate radius that signals "crafted" without sacrificing density.
- **Interactive Elements:** Buttons and inputs use `rounded-sm` (6px) for a tighter, more technical feel.
- **Elevated Panels:** Use `rounded-lg` (12px) to distinguish them as higher-order surfaces.
- **Node Badges:** Use `rounded-sm` (6px) to maintain density in the knowledge graph.

No element should use a radius larger than 12px except the `rounded-full` utility for decorative pills and tags.

## Components

### Glass Panels

The fundamental container unit. Uses a semi-transparent dark fill (`#141414` at 80-95% opacity) with `backdrop-filter: blur(8px)` to create depth layering. The 1px border at `accent/10` is critical — without it, the glass edge disappears into the background. Elevated panels use higher opacity to sit "closer" to the user.

### Buttons

Primary buttons are solid gold (`accent`) on near-black text — high contrast and unmistakable. Ghost buttons invert this: transparent background with gold text and a subtle gold background on hover (6% opacity). Button typography uses `label-md` (13px Inter Medium, 0.025em letter spacing) for precision.

### Knowledge Graph Nodes

Each semantic type (file, function, class, module, concept, etc.) has a dedicated node color. Nodes are compact (`rounded-sm`, `8px` padding) to maximize graph density. Selected nodes should emit an accent glow ring.

### Scrollbar

Custom scrollbars use the accent color at low opacity (20%) to blend with the dark theme. Thumb hover increases to 35% opacity for wayfinding — never intrusive.

### Input Fields

Inputs sit at the `surface` layer with no border by default. On focus, they emit an accent-colored ring/glow. The dark background keeps the UI immersive; the gold focus state guides the eye precisely.

## Do's and Don'ts

- Do use the accent gold sparingly — it should feel precious, not pervasive
- Don't apply the accent color to large background areas; reserve it for highlights, actions, and wayfinding
- Do maintain WCAG AA contrast (4.5:1) for all body text against surface backgrounds
- Don't use pure white (#ffffff) anywhere — always use the warm off-white `text-primary`
- Do apply `backdrop-filter: blur(8px)` to all glass panels to justify their translucency
- Don't stack more than three glass layers — depth becomes disorienting
- Do use the accent glow (`0 0 20px rgba(212,165,116,0.15)`) on interactive focus states
- Don't mix the gold accent with other bright colors (neon, electric blue) — it destroys the scholarly mood
- Do let the dark background occupy at least 30% of any viewport — it is not unused space, it is intentional depth
- Don't use heavy box-shadows — prefer thin, glowing borders and tonal separation instead
