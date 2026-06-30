---
name: VS Code
colors:
  accent-primary: "#0078d4"
  accent-secondary: "#0069b9"
  background: "#0d1014"
  foreground: "#e2e2e2"
  foreground-muted: "#b6bbc4"
  foreground-intense: "#e6eefa"
  link-foreground: "#4daafc"
  link-foreground-hover: "#8fc3fe"
  border-background: "rgba(255,255,255,0.12)"
  card-background: "rgba(255,255,255,0.04)"
  card-hover-background: "rgba(255,255,255,0.08)"
  card-border: "rgba(255,255,255,0.12)"
  button-primary-background: "#0078d4"
  button-primary-foreground: "#ffffff"
  button-primary-hover: "#005ba4"
  button-secondary-background: "#25292e"
  button-secondary-foreground: "#e2e2e2"
  button-secondary-border: "rgba(255,255,255,0.3)"
  code-background: "#1e1e1e"
  code-foreground: "#d4d4d4"
  inline-code-background: "rgba(255,255,255,0.1)"
  inline-code-foreground: "#d4d4d4"
  inline-code-border: "rgba(255,255,255,0.15)"
  selection-background: "#7ed4e8"
  selection-foreground: "#1a1a1a"
  keybinding-background: "rgba(255,255,255,0.15)"
  keybinding-foreground: "#4daafc"
  scrollbar-slider-background: "rgba(255,255,255,0.15)"
  scrollbar-slider-hover-background: "rgba(255,255,255,0.25)"
  syntax-keyword: "#c586c0"
  syntax-function: "#dcdcaa"
  syntax-param: "#9cdcfe"
  syntax-type: "#4ec9b0"
  syntax-comment: "#6a9955"
  syntax-string: "#ce9178"
  syntax-value: "#569cd6"
  alert-note-border: "#00bcf2"
  alert-tip-border: "#bad80a"
  alert-warning-border: "#fff100"
  alert-important-border: "#b4a0ff"
  alert-caution-border: "#fe7543"
  accent-card-1: "#3794ff"
  accent-card-2: "#a371f7"
  accent-card-3: "#3fb950"
  hero-background-dark: "linear-gradient(180deg,#0e0e0e 0%,#141414 100%)"
  banner-background: "linear-gradient(135deg,#0d1014 0%,rgba(0,32,80,0.25) 15%,rgba(0,32,80,0.25) 75%,#0d1014 100%)"
  color-blue: "#0072be"
  color-purple: "#5c2d91"
  color-green: "#477a32"
  color-orange: "#d83b01"
  color-red: "#e81123"
typography:
  display-hero:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 80px
    fontWeight: "700"
    lineHeight: 1.1
    letterSpacing: -0.8px
  display-xl:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 42px
    fontWeight: "600"
    lineHeight: 1.15
    letterSpacing: -0.5px
  display-lg:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 36px
    fontWeight: "600"
    lineHeight: 1.2
  headline-lg:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 28px
    fontWeight: "600"
    lineHeight: 1.3
  headline-md:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 24px
    fontWeight: "600"
    lineHeight: 1.3
  headline-sm:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 20px
    fontWeight: "600"
    lineHeight: 1.4
  body-lg:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 1.6
  body-md:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 14px
    fontWeight: "400"
    lineHeight: 1.6
  body-sm:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 13px
    fontWeight: "400"
    lineHeight: 1.5
  label-lg:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 14px
    fontWeight: "600"
    lineHeight: 1.4
  label-sm:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 11px
    fontWeight: "600"
    lineHeight: 1.3
    letterSpacing: 0.05em
  code-md:
    fontFamily: Menlo, Monaco, Consolas, "Courier New", monospace
    fontSize: 13px
    fontWeight: "400"
    lineHeight: 1.7
  code-inline:
    fontFamily: Menlo, Monaco, Consolas, "Courier New", monospace
    fontSize: 90%
    fontWeight: "400"
    lineHeight: 1.4
rounded:
  sm: 2px
  md: 4px
  lg: 6px
  xl: 8px
  xxl: 12px
  card: 10px
  pill: 999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  xxxl: 40px
  section: 48px
  section-lg: 64px
  gutter: 24px
  margin-page: 24px
  max-content: 800px
  max-layout: 1440px
components:
  navbar:
    backgroundColor: "{colors.background}"
    minHeight: 50px
    fontSize: 16px
  navbar-brand:
    color: "#9d9d9d"
    fontSize: 15px
    paddingLeft: 30px
  nav-link:
    color: "#9d9d9d"
    typography: "{typography.body-lg}"
  nav-link-hover:
    color: "{colors.foreground}"
  nav-link-active:
    color: "{colors.foreground}"
  nav-dropdown-menu:
    backgroundColor: "{colors.background}"
    rounded: "{rounded.md}"
    padding: 6px
    minWidth: 200px
    boxShadow: 0 4px 16px rgba(0,0,0,0.12), 0 1px 3px rgba(0,0,0,0.08)
  button-primary:
    backgroundColor: "{colors.button-primary-background}"
    textColor: "{colors.button-primary-foreground}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.xl}"
    padding: 9px 16px
  button-primary-hover:
    backgroundColor: "{colors.button-primary-hover}"
  button-secondary:
    backgroundColor: "{colors.button-secondary-background}"
    textColor: "{colors.button-secondary-foreground}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.xl}"
    borderColor: "{colors.button-secondary-border}"
    padding: 9px 16px
  button-secondary-hover:
    backgroundColor: "#333940"
  card-default:
    backgroundColor: "{colors.card-background}"
    rounded: "{rounded.xxl}"
    borderColor: "{colors.card-border}"
    padding: "{spacing.xl}"
  card-default-hover:
    backgroundColor: "{colors.card-hover-background}"
  card-feature:
    backgroundColor: "{colors.card-background}"
    rounded: "{rounded.xxl}"
    borderWidth: 1px
    borderColor: "{colors.card-border}"
    padding: "{spacing.xxl}"
  card-docs-latest:
    backgroundColor: "{colors.card-background}"
    rounded: "{rounded.card}"
    borderColor: "{colors.card-border}"
    padding: "{spacing.md}" "{spacing.lg}"
  code-block:
    backgroundColor: "{colors.code-background}"
    textColor: "{colors.code-foreground}"
    rounded: 0 0 "{rounded.lg}" "{rounded.lg}"
    padding: "{spacing.sm}"
    fontFamily: "{typography.code-md.fontFamily}"
    fontSize: "{typography.code-md.fontSize}"
  code-block-header:
    backgroundColor: "rgba(255,255,255,0.05)"
    color: "#9FB1D1"
    rounded: "{rounded.lg}" "{rounded.lg}" 0 0
    padding: "{spacing.xs}" "{spacing.md}"
  inline-code:
    backgroundColor: "{colors.inline-code-background}"
    textColor: "{colors.inline-code-foreground}"
    rounded: "{rounded.md}"
    borderColor: "{colors.inline-code-border}"
    padding: 1px 5px
    fontSize: 90%
  docs-layout:
    maxWidth: "{spacing.max-layout}"
    padding: 0 24px
    gridTemplateColumns: "minmax(240px,280px) 1fr"
  docs-left-sidebar:
    width: "minmax(240px, 280px)"
    stickyTop: 70px
  docs-content-wrapper:
    gridTemplateColumns: "minmax(0,800px) minmax(200px,240px)"
    gap: "{spacing.xxl}"
  docs-right-sidebar:
    width: "minmax(200px, 240px)"
    stickyTop: 70px
  callout-box:
    backgroundColor: "rgba(56,55,55,0.2)"
    borderColor: "{colors.link-foreground}"
    borderRadius: "{rounded.xl}"
    padding: "{spacing.md}" "{spacing.lg}"
    borderLeftWidth: 4px
  markdown-alert:
    rounded: "{rounded.xl}"
    padding: "{spacing.sm}" "{spacing.md}"
    borderLeftWidth: 4px
  markdown-alert-tip:
    borderColor: "{colors.alert-tip-border}"
  markdown-alert-note:
    borderColor: "{colors.alert-note-border}"
  markdown-alert-important:
    borderColor: "{colors.alert-important-border}"
  markdown-alert-warning:
    borderColor: "{colors.alert-warning-border}"
  markdown-alert-caution:
    borderColor: "{colors.alert-caution-border}"
  search-container:
    backgroundColor: "#eaeaea"
    rounded: "{rounded.lg}"
  search-input:
    backgroundColor: transparent
    textColor: "{colors.foreground}"
    borderColor: "{colors.border-background}"
  search-input-focus:
    borderColor: "{colors.accent-primary}"
  keybinding:
    backgroundColor: "{colors.keybinding-background}"
    textColor: "{colors.keybinding-foreground}"
    rounded: "{rounded.sm}"
    padding: 2px 6px
    fontSize: 11px
  scrollbar-thumb:
    backgroundColor: "{colors.scrollbar-slider-background}"
    rounded: "{rounded.pill}"
  scrollbar-thumb-hover:
    backgroundColor: "{colors.scrollbar-slider-hover-background}"
  sidebar-action-card:
    backgroundColor: "{colors.card-background}"
    rounded: "{rounded.xxl}"
    borderColor: "{colors.card-border}"
    padding: "{spacing.md}"
  sidebar-action-card-hover:
    backgroundColor: "{colors.card-hover-background}"
  footer-background:
    backgroundColor: "{colors.background}"
---

## Overview

VS Code embodies a **Developer-First Minimalist** aesthetic — a functional, unadorned interface that prioritizes readability and content clarity above all else. The design language is defined by the philosophy of the editor itself: clean, efficient, and transparent.

The brand personality is **professional, precise, and neutral**. It targets developers who spend hours in the tool and need an interface that fades into the background. The UI should feel like a well-organized workshop — every tool is exactly where you expect it, nothing is decorative, everything serves a purpose.

The default state is **dark-first** (`#0d1014` background), with a fully supported light theme. Both themes maintain identical spatial relationships — only the color values change. This dual-theme commitment is non-negotiable.

## Colors

The VS Code palette is anchored in a **Dark-First dual-theme** system. Color serves as informational signals, not decoration.

### Dark Theme (Default)

- **Background (#0d1014):** Deep charcoal — the canvas. Never pure black; allows subtle layering.
- **Foreground (#e2e2e2):** Soft off-white for body text. High legibility without the glare of pure white.
- **Foreground Intense (#e6eefa):** Brighter tone for headings and emphasized content.
- **Foreground Muted (#b6bbc4):** Secondary text, metadata, less prominent information.
- **Link Foreground (#4daafc):** The sole interactive accent on the site — a clear, readable blue for all hyperlinks.
- **Link Foreground Hover (#8fc3fe):** Brightened link on hover, providing clear interactive feedback.
- **Accent Primary (#0078d4):** The VS Code blue — used for primary buttons, focus indicators, and active states.
- **Border Background (rgba(255,255,255,0.12)):** Subtle separators that provide structure without visual weight.
- **Card Background (rgba(255,255,255,0.04)):** Barely-there white for card surfaces — depth through tint, not shadow.

### Light Theme

All token names remain the same; values invert: `background: #ffffff`, `foreground: #333333`, `link-foreground: #005fb8`. Card backgrounds shift to `rgba(0,0,0,0.01)` with darker borders `rgba(0,0,0,0.10)`. The structural relationships are preserved — only the luminance polarity changes.

### Syntax Highlighting

Code syntax tokens follow VS Code's Dark+ theme: keywords in purple (`#c586c0`), functions in yellow (`#dcdcaa`), parameters in light blue (`#9cdcfe`), types in teal (`#4ec9b0`), comments in green (`#6a9955`), strings in warm orange (`#ce9178`), and values in blue (`#569cd6`).

### Alert Colors

Five alert levels use distinct left-border colors: Tip (green `#bad80a`), Note (cyan `#00bcf2`), Important (purple `#b4a0ff`), Warning (yellow `#fff100`), Caution (orange `#fe7543`).

## Typography

The typography strategy is **utilitarian and system-native**. No custom fonts are loaded — the interface uses the operating system's native font stack for maximum performance and familiarity.

- **System UI Stack:** `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif` — ensures the interface feels native to every platform.
- **Headlines:** Use `font-weight: 600` (Semi Bold) for all heading levels. The hierarchy spans from `80px` (hero) down to `20px` (small headlines). Letter-spacing tightens at the largest sizes.
- **Body:** `16px` for large body, `14px` for default body — both with generous line-height of `1.6` for comfortable reading.
- **Labels & UI:** `14px` at `font-weight: 600` for buttons and interactive elements. Small labels at `11px` with `0.05em` letter-spacing for metadata and tags.
- **Code:** The monospace stack `Menlo, Monaco, Consolas, "Courier New", monospace` at `13px` with `1.7` line-height for code blocks. Inline code is slightly smaller (`90%`) with distinct background and border.

## Layout & Spacing

The layout follows a **Structured Information Grid** optimized for documentation reading.

- **Site Maximum:** `1440px` centered, with `24px` page margins.
- **Documentation Layout:** Three-column grid: left sidebar (240-280px) for table of contents, center content (max 800px) for the article, right sidebar (200-240px) for on-page navigation. Both sidebars are sticky (`top: 70px` to clear the navbar).
- **Content Width:** Article content is capped at `800px` for optimal reading line length. This is the most important constraint — never exceed it for text-heavy pages.
- **Spacing Rhythm:** A `4px` base unit scales up: `8px` (tight), `12px` (snug), `16px` (base), `20px` (comfortable), `24px` (generous), `32px` (section), `40px` (large section), `48px` (page section), `64px` (major section).
- **Navigation Bar:** Fixed at the top, `50px` height. The brand ("Visual Studio Code") sits at `15px` with `30px` left padding. Navigation links are `16px` in muted gray (`#9d9d9d`).

## Elevation & Depth

The VS Code design system uses **minimal layering** — content hierarchy is established through tint and border rather than shadow.

- **Layer 0 (Background):** The page background (`#0d1014` dark / `#ffffff` light). This is the canvas.
- **Layer 1 (Cards & Containers):** Elevated via tint — `rgba(255,255,255,0.04)` in dark mode, `rgba(0,0,0,0.01)` in light mode. A `1px` border at `rgba(255,255,255,0.12)` (dark) or `rgba(0,0,0,0.10)` (light) defines the edge.
- **Layer 2 (Interactive Hover):** Cards on hover become `rgba(255,255,255,0.08)` (dark) — still minimal, never aggressive.
- **Layer 3 (Dropdowns & Modals):** Dropdown menus use a compound shadow: `0 4px 16px rgba(0,0,0,0.12), 0 1px 3px rgba(0,0,0,0.08)`. The modal shadow is more pronounced: `0 10px 30px rgba(0,0,0,0.2)`.

## Shapes

The shape language is **Functionally Minimal** — radius values are small and consistent, never decorative.

- **Buttons & Interactive Elements:** `8px` (`rounded-xl`) — the standard for all clickable surfaces.
- **Cards & Containers:** `12px` (`rounded-xxl`) — larger containers use a slightly bigger radius.
- **Dropdowns & Inputs:** `4px` (`rounded-md`) — compact and precise.
- **Code Blocks:** Bottom corners at `6px` (`rounded-lg`), top corners flat when preceded by a header bar.
- **Inline Code:** `4px` (`rounded-md`) — matches input fields.
- **Focus Indicators:** Use `2px` outline at `#007acc` (the accent primary blue).
- **Keybindings:** `2px` (`rounded-sm`) — subtle enough to not distract from the text.
- **Alert/Callout Boxes:** `8px` (`rounded-xl`) — with a prominent `4px` left border for color coding.

## Components

### Navigation Bar

The fixed top navbar is the primary wayfinding element. The brand logo/text ("Visual Studio Code") is on the left, followed by top-level navigation (Features, Docs, Release Notes, Blog, Learn, Events, Resources). Navigation dropdowns appear on hover with a compound shadow and `4px` radius. The right side contains the search widget, theme toggle, and Download button.

### Buttons

Primary buttons use the VS Code blue (`#0078d4`) with white text and `8px` radius. On hover, they darken to `#005ba4`. Secondary buttons use a transparent style with a subtle background (`#25292e`) and a white border at 30% opacity. Focus state uses a `2px` blue outline.

### Code Blocks

Code blocks are displayed on a dedicated `#1e1e1e` background (matching the VS Code editor) with `#d4d4d4` foreground. A header bar may appear above the code showing the language label at `rgba(255,255,255,0.05)` with `#9FB1D1` text. A "Copy" button in the top-right uses a neutral gray. The block has `12px` padding and `6px` bottom radius. Syntax highlighting follows the Dark+ theme.

### Markdown Alerts

Five alert types share a common structure: a `4px` colored left border, `12px` padding, and `8px` radius. Each has a dedicated border color and an SVG icon: Tip (green), Note (cyan), Important (purple), Warning (yellow), Caution (orange).

### Callout Boxes

Interactive callout boxes feature a `4px` blue left border with a gradient background. They contain a title (bold, `16px`), description, and a CTA button. Used primarily in documentation to suggest next-step learning actions.

### Keybinding Display

Keyboard shortcuts are shown as inline badge elements: `2px` radius, `rgba(255,255,255,0.15)` background, `#4daafc` text, `2px 6px` padding, `11px` font size.

### Sidebar Action Cards

Cards in the right sidebar contain a title, description, and call-to-action link. They use `12px` radius and the standard card background/border, with a subtle hover state.

### Search

The search widget in the navbar uses a container background of `#eaeaea` (light) with a transparent input. On focus, the input border transitions to the accent blue. The search dialog overlay uses a strong shadow (`0 10px 30px rgba(0,0,0,0.2)`) to elevate it above all page content.

## Do's and Don'ts

- Do use the dark theme as the default; light theme is an explicit opt-in via `data-theme=light`
- Don't use custom webfonts — always use the system UI font stack for performance
- Do maintain the `4px` spacing base; all spacing values should be multiples of `4px`
- Don't apply shadows heavier than the dropdown compound shadow (`0 4px 16px, 0 1px 3px`)
- Do keep content width at max `800px` for text-heavy pages; only full-width layouts may exceed it
- Don't use pure black (`#000`) for backgrounds or pure white (`#fff`) for text — always use the defined tokens
- Do provide both dark and light theme equivalents for every color token
- Don't use colored borders or backgrounds for decorative purposes — color must carry semantic meaning
- Do use syntax highlighting that follows the Dark+ theme consistently across all code blocks
- Don't mix border-radius values smaller than `2px` or larger than `12px` for standard components
