---
name: GitHub
colors:
  bg-default: "#ffffff"
  bg-muted: "#f6f8fa"
  bg-emphasis: "#25292e"
  bg-inset: "#ffffff"
  fg-default: "#1f2328"
  fg-muted: "#59636e"
  fg-disabled: "#818b98"
  fg-onEmphasis: "#ffffff"
  accent-fg: "#0969da"
  accent-emphasis: "#0969da"
  accent-muted: "#ddf4ff"
  success-fg: "#1a7f37"
  success-emphasis: "#1f883d"
  success-muted: "#dafbe1"
  danger-fg: "#d1242f"
  danger-emphasis: "#cf222e"
  danger-muted: "#ffebe9"
  attention-fg: "#9a6700"
  attention-emphasis: "#9a6700"
  attention-muted: "#fff8c5"
  severe-fg: "#bc4c00"
  severe-emphasis: "#bc4c00"
  done-fg: "#8250df"
  done-emphasis: "#8250df"
  sponsors-fg: "#bf3989"
  border-default: "#d1d9e0"
  border-muted: "#d1d9e0b3"
  border-emphasis: "#818b98"
  header-bg: "#25292e"
  header-fg: "#ffffffb3"
  header-logo: "#ffffff"
  header-search-bg: "#25292e"
  control-bg-rest: "#f6f8fa"
  control-bg-hover: "#eff2f5"
  overlay-bg: "#ffffff"
  overlay-backdrop: "#c8d1da66"
  selection-bg: "#0969da33"
  underlineNav-borderActive: "#fd8c73"
  button-primary-bg: "#1f883d"
  button-primary-hover: "#1c8139"
  button-primary-active: "#197935"
  button-primary-disabled: "#95d8a6"
  button-danger-fg: "#d1242f"
  button-danger-hoverBg: "#a40e26"
  button-danger-hoverFg: "#ffffff"
  button-outline-hoverBg: "#0757ba"
  button-outline-hoverFg: "#ffffff"
  reaction-selected-bg: "#ddf4ff"
  topicTag-border: "#fff0"
  avatar-bg: "#ffffff"
  skeleton-bg: "#818b981a"
  color-ansi-black: "#1f2328"
  color-ansi-red: "#cf222e"
  color-ansi-green: "#116329"
  color-ansi-yellow: "#4d2d00"
  color-ansi-blue: "#0969da"
  color-ansi-magenta: "#8250df"
  color-ansi-cyan: "#1b7c83"
  color-ansi-white: "#59636e"
typography:
  display-xl:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 40px
    fontWeight: "500"
    lineHeight: 1.25
  display-lg:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 32px
    fontWeight: "500"
    lineHeight: 1.25
  title-xl:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 32px
    fontWeight: "600"
    lineHeight: 1.5
  title-lg:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 20px
    fontWeight: "600"
    lineHeight: 1.5
  title-md:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 16px
    fontWeight: "600"
    lineHeight: 1.5
  subtitle:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 20px
    fontWeight: "400"
    lineHeight: 1.625
  body-lg:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 1.5
  body-md:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 14px
    fontWeight: "400"
    lineHeight: 1.5
  body-sm:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 12px
    fontWeight: "400"
    lineHeight: 1.5
  caption:
    fontFamily: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif
    fontSize: 12px
    fontWeight: "400"
    lineHeight: 1.25
  code-block:
    fontFamily: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace
    fontSize: 13px
    fontWeight: "400"
    lineHeight: 1.5
  code-inline:
    fontFamily: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace
    fontSize: 0.9285em
    fontWeight: "400"
rounded:
  sm: 3px
  md: 6px
  lg: 12px
  full: 624.938rem
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
  control-large: 40px
  control-medium: 32px
  control-small: 28px
  control-xsmall: 24px
  stack-gap: 16px
  stack-gap-condensed: 8px
  stack-gap-spacious: 24px
  breakpoint-xs: 20rem
  breakpoint-sm: 34rem
  breakpoint-md: 48rem
  breakpoint-lg: 63.25rem
  breakpoint-xl: 80rem
  breakpoint-xxl: 87.5rem
components:
  button-primary:
    backgroundColor: "{colors.button-primary-bg}"
    textColor: "{colors.fg-onEmphasis}"
    typography: "{typography.body-md}"
    fontWeight: "500"
    rounded: "{rounded.md}"
    padding: "{spacing.sm}" "{spacing.lg}"
    height: "{spacing.control-medium}"
  button-primary-hover:
    backgroundColor: "{colors.button-primary-hover}"
  button-primary-active:
    backgroundColor: "{colors.button-primary-active}"
  button-primary-disabled:
    backgroundColor: "{colors.button-primary-disabled}"
  button-secondary:
    backgroundColor: "{colors.control-bg-rest}"
    textColor: "{colors.fg-default}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    padding: "{spacing.sm}" "{spacing.lg}"
    height: "{spacing.control-medium}"
  button-secondary-hover:
    backgroundColor: "{colors.control-bg-hover}"
  button-danger:
    backgroundColor: "{colors.control-bg-rest}"
    textColor: "{colors.button-danger-fg}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    padding: "{spacing.sm}" "{spacing.lg}"
    height: "{spacing.control-medium}"
  button-danger-hover:
    backgroundColor: "{colors.button-danger-hoverBg}"
    textColor: "{colors.button-danger-hoverFg}"
  header:
    backgroundColor: "{colors.header-bg}"
    color: "{colors.header-fg}"
    height: 64px
    padding: 0 16px
  header-logo:
    color: "{colors.header-logo}"
  header-search:
    backgroundColor: "{colors.header-search-bg}"
    rounded: "{rounded.md}"
    height: 28px
    width: 240px
  nav-link:
    color: "{colors.fg-muted}"
    typography: "{typography.body-md}"
    fontWeight: "500"
  nav-link-hover:
    color: "{colors.fg-default}"
  nav-link-active:
    color: "{colors.fg-default}"
    borderBottom: "2px solid {colors.accent-fg}"
  card-default:
    backgroundColor: "{colors.bg-default}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    padding: "{spacing.md}"
  card-muted:
    backgroundColor: "{colors.bg-muted}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "{colors.control-bg-rest}"
    textColor: "{colors.fg-default}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    padding: "{spacing.sm}" "{spacing.sm}"
    height: "{spacing.control-medium}"
  input-field-focus:
    borderColor: "{colors.accent-fg}"
    boxShadow: 0 0 0 3px "{colors.accent-muted}"
  input-field-disabled:
    backgroundColor: "{colors.bg-disabled}"
    color: "{colors.fg-disabled}"
  overlay-panel:
    backgroundColor: "{colors.overlay-bg}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    boxShadow: "0 8px 24px rgba(0,0,0,0.12)"
  overlay-backdrop:
    backgroundColor: "{colors.overlay-backdrop}"
  label-accent:
    backgroundColor: "{colors.accent-muted}"
    textColor: "{colors.accent-fg}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    fontSize: 12px
    fontWeight: "500"
  label-success:
    backgroundColor: "{colors.success-muted}"
    textColor: "{colors.success-fg}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    fontSize: 12px
  label-danger:
    backgroundColor: "{colors.danger-muted}"
    textColor: "{colors.danger-fg}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    fontSize: 12px
  label-attention:
    backgroundColor: "{colors.attention-muted}"
    textColor: "{colors.attention-fg}"
    rounded: "{rounded.sm}"
    padding: "0 8px"
    fontSize: 12px
  code-block:
    backgroundColor: "{colors.bg-muted}"
    textColor: "{colors.fg-default}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
    fontSize: "{typography.code-block.fontSize}"
    lineHeight: "{typography.code-block.lineHeight}"
  code-inline:
    backgroundColor: "{colors.accent-muted}"
    textColor: "{colors.fg-default}"
    rounded: "{rounded.sm}"
    padding: "2px 6px"
    fontSize: "{typography.code-inline.fontSize}"
  avatar:
    backgroundColor: "{colors.avatar-bg}"
    rounded: "{rounded.full}"
  diff-addition:
    backgroundColor: "{colors.success-muted}"
    borderColor: "{colors.success-emphasis}"
  diff-deletion:
    backgroundColor: "{colors.danger-muted}"
    borderColor: "{colors.danger-emphasis}"
  timeline-badge:
    backgroundColor: "{colors.bg-default}"
    borderColor: "{colors.border-default}"
    rounded: "{rounded.full}"
  tab-nav-item:
    color: "{colors.fg-muted}"
    typography: "{typography.body-md}"
    padding: "{spacing.sm}" "{spacing.md}"
    borderBottom: "2px solid transparent"
  tab-nav-item-active:
    color: "{colors.fg-default}"
    borderBottom: "2px solid {colors.underlineNav-borderActive}"
  tab-nav-item-hover:
    color: "{colors.fg-default}"
    borderBottom: "2px solid {colors.border-muted}"
  pagination-item:
    backgroundColor: "{colors.control-bg-rest}"
    rounded: "{rounded.md}"
    padding: "{spacing.xs}" "{spacing.sm}"
  select-menu:
    backgroundColor: "{colors.bg-default}"
    rounded: "{rounded.md}"
    borderColor: "{colors.border-default}"
    boxShadow: "0 8px 24px rgba(0,0,0,0.12)"
  select-menu-item-active:
    backgroundColor: "#b6e3ff"
---

## Overview

GitHub embodies an **Utility-First, Data-Dense** aesthetic — a platform designed for developers who spend their entire workday in its interface. Every pixel serves a purpose; nothing is decorative. The design language prioritizes information density, scanning efficiency, and clear status communication at a glance.

The brand personality is **professional, neutral, and trustworthy**. It targets software developers, open source maintainers, and engineering teams who need to navigate complex repositories, review code, manage issues, and collaborate asynchronously. The UI should feel like a well-organized command center — information-rich without being overwhelming.

The visual identity is defined by Primer, GitHub's open-source design system. The default state is **light-first** with a fully supported dark theme. Both themes are equally maintained and user-selectable via `data-color-mode`. The system extends to multiple accessibility variants (high contrast, colorblind, tritanopia, dimmed).

## Colors

The GitHub palette follows Primer's **alpha-enabled** color system — base colors are combined with transparency to create depth without multiplying color tokens.

### Light Theme (Default)

- **Page Background (#ffffff):** Clean white canvas for maximum content contrast.
- **Muted Background (#f6f8fa):** Subtle gray used for secondary surfaces, code block backgrounds, and table alternate rows.
- **Emphasis Background (#25292e):** Dark gray used for the header bar and emphasized containers.
- **Primary Text (#1f2328):** Near-black for maximum readability.
- **Muted Text (#59636e):** Mid-gray for secondary information, timestamps, and metadata.
- **Accent Blue (#0969da):** The signature GitHub blue — used for links, primary actions, and interactive states.
- **Accent Green (#1f883d):** Success states, merged pull requests, new additions.
- **Accent Red (#cf222e):** Danger states, deleted content, error indicators.
- **Accent Yellow (#9a6700):** Warnings, attention states, pinned items.
- **Accent Purple (#8250df):** Done states, sponsorship features.
- **Borders (#d1d9e0):** Light gray for structure without visual weight.
- **Orange (#fd8c73):** Active navigation indicator ("underline nav") — GitHub's signature orange underline.

### Dark Theme

All tokens preserve their semantic roles; only the luminance flips: `background: #0d1117`, `fg-default: #f0f6fc`, `accent-fg: #4493f8`, `border-default: #3d444d`. The accent blue brightens against dark backgrounds to maintain contrast.

### ANSI Terminal Colors

GitHub defines a complete 16-color ANSI palette (black, red, green, yellow, blue, magenta, cyan, white + bright variants) for terminal emulation within the interface, used in Actions logs and terminal embeds.

## Typography

GitHub uses **Mona Sans VF**, a custom variable font designed specifically for the platform, alongside a comprehensive system fallback stack.

- **Mona Sans VF:** GitHub's proprietary variable font. It supports a range of weights (300-900) and widths via font-variation-settings. The font is self-hosted on GitHub's CDN for consistent rendering across all platforms.
- **Font Stack:** `"Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"`.
- **Display Sizes:** `40px` and `32px` at `font-weight: 500` (Medium) for hero sections and page titles.
- **Title Hierarchy:** `32px` (title-xl), `20px` (title-lg), `16px` (title-md) — all at `font-weight: 600` (Semibold) with `line-height: 1.5`.
- **Body:** `16px` (body-lg), `14px` (body-md — the default), `12px` (body-sm) — all at `font-weight: 400` (Normal) with `line-height: 1.5`.
- **Caption:** `12px` at `font-weight: 400` with tighter `line-height: 1.25`.
- **Monospace Stack:** `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace` at `13px` for code blocks and `0.9285em` for inline code.
- **Line Height Scale:** tight (`1.25`), snug (`1.375`), normal (`1.5`), relaxed (`1.625`), loose (`1.75`).

## Layout & Spacing

GitHub uses a **fixed-width centered layout** with responsive breakpoints.

- **Breakpoint System:** `20rem` (320px, xsmall), `34rem` (544px, small), `48rem` (768px, medium), `63.25rem` (1012px, large), `80rem` (1280px, xlarge), `87.5rem` (1400px, xxlarge).
- **Page Width:** Content is centered within a `1280px` max-width container. Repository content areas typically cap at `1012px`.
- **Spacing Scale:** Primer uses a `4px` base unit: `4px` (base), `8px` (xs), `12px` (sm), `16px` (md), `20px` (lg), `24px` (xl), `32px` (xxl), `40px` (xxxl), `48px` (section), `64px` (128), `80px` (160), `96px` (192).
- **Control Sizing:** Buttons and inputs follow a strict height scale: `40px` (large), `32px` (medium — default), `28px` (small), `24px` (xsmall).
- **Stack Gaps:** `8px` (condensed), `16px` (normal), `24px` (spacious).
- **Header:** Fixed at the top, containing the GitHub logo/mark, navigation, search (240px wide), and user menu.

## Elevation & Depth

GitHub uses **minimal, purposeful elevation** — the interface is predominantly flat with targeted use of shadow for overlays and dropdowns.

- **Layer 0 (Page):** `bg-default` (`#ffffff` light / `#0d1117` dark).
- **Layer 1 (Surfaces):** `bg-muted` (`#f6f8fa`) for code blocks, comment threads, and secondary areas.
- **Layer 2 (Overlays & Modals):** Use a compound shadow: `0 8px 24px rgba(0,0,0,0.12)` with `overlay-backdrop` (`#c8d1da66`) as the semi-transparent backdrop.
- **Layer 3 (Dropdowns & Select Menus):** Same shadow as overlays but without backdrop. The overlay background shifts to `#010409` in dark theme to ensure contrast.
- **Header:** The site header (`header-bg: #25292e` light / `#151b23f2` dark) sits at `z-index: 32` and has a subtle bottom border.

## Shapes

GitHub's shape language is **utilitarian and precise** — radius values are small and standardized.

- **Default Radius:** `6px` (`rounded-md`) — used for all buttons, inputs, cards, and containers.
- **Small Radius:** `3px` (`rounded-sm`) — used for labels, badges, and inline code.
- **Large Radius:** `12px` (`rounded-lg`) — used for larger overlay containers and marketing cards.
- **Full/Pill:** `624.938rem` (effectively infinite) — used for avatars, reaction pills, and issue labels.
- **Focus Outline:** Use `3px` of the accent color at 33% opacity (`#0969da33` light / `#1f6febb3` dark) around the element. This is defined as `--selection-bgColor` and applied as a `box-shadow` on focus states.
- **Active Tab Underline:** `2px` solid orange (`#fd8c73` light / `#f78166` dark) — the signature GitHub underline nav indicator.

## Components

### Header

The global navigation header uses a dark background (`#25292e` light / `#151b23f2` dark) with white text at 70% opacity. The GitHub Mark logo is white. The search bar is a dark input on the dark header with a subtle border. The header contains: logo, navigation links, search (240px), notifications, and user avatar dropdown.

### Buttons

Primary buttons use green (`#1f883d`) with white text and `6px` radius. On hover they darken to `#1c8139`. Danger buttons are visually secondary (default gray) with red text (`#d1242f`), turning red on hover. Outline buttons use the accent blue for secondary actions. All buttons follow the control size scale: `32px` height by default.

### Navigation Tabs

The underline navigation pattern is signature GitHub: tabs with `2px` bottom border, transparent by default, showing `fg-muted` text. On hover, the border becomes muted gray. The active tab uses the orange underline (`#fd8c73`) with bold/default text. This pattern is used across repositories (Code, Issues, Pull Requests, Actions, Projects, etc.).

### Labels & Badges

Semantic labels use a muted background with a matching text color: accent (blue), success (green), danger (red), attention (yellow), done (purple), sponsors (pink). All labels use `3px` radius, `12px` font size, and `font-weight: 500`. They have no visible border (border defaults to transparent).

### Code Blocks

Code blocks sit on a `bg-muted` (`#f6f8fa`) background with `6px` radius and `16px` padding. Syntax highlighting follows the Prettylights theme: comments in gray, constants in blue, entities in purple, keywords in red, strings in dark blue, variables in orange. Line numbers are rendered in `fg-muted`.

### Overlays & Modals

Overlay containers use `bg-default` with `6px` radius, `1px` `border-default` border, and a compound shadow (`0 8px 24px rgba(0,0,0,0.12)`). The backdrop uses `overlay-backdrop` (`#c8d1da66`). Overlays have a controlled size system: small (`20rem`), medium (`30rem`), large (`40rem`), xlarge (`60rem`).

### Avatars

Avatars are rendered at `100%` width/height with `rounded-full` and a subtle white border/background to handle transparent PNGs gracefully.

### Diff & Code Review

Diff views use colored backgrounds for changed lines: green muted (`#dafbe1`) for additions, red muted (`#ffebe9`) for deletions. Inline word-level diffs use `#aceebb` (green) and `#ffcecb` (red) backgrounds. Hunk number headers use a blue tint (`#b6e3ff`).

### Footer

The page footer is minimal, containing the GitHub logo, navigation links (Terms, Privacy, Security, Status, Docs, etc.), and the copyright notice. It sits on `bg-default` with a `border-default` top border.

## Do's and Don'ts

- Do use the standard `6px` (`rounded-md`) radius for all interactive controls — do not deviate
- Don't use custom web fonts; always use Mona Sans VF with the Primer fallback stack
- Do maintain `4.5:1` minimum contrast ratio for all text against its background
- Don't use pure black (`#000`) for backgrounds or pure white (`#fff`) for text — use the defined sematic tokens
- Do support both light and dark themes equally; never assume one theme is primary
- Don't add shadows heavier than the overlay compound shadow (`0 8px 24px rgba(0,0,0,0.12)`)
- Do use the orange underline nav indicator (`#fd8c73`) for active navigation state — it is a signature GitHub pattern
- Don't use colored borders for decorative purposes — color must carry semantic meaning
- Do use the Prettylights syntax theme for all code highlighting
- Don't use border-radius larger than `6px` for standard UI controls; reserve `12px` for overlays and marketing cards
- Do use the `4px` spacing base for all layout calculations
- Don't mix button variants on the same row unless they have distinct semantic hierarchy
