---
name: understand-anything-style
description: 基于 understand-anything.com 网站的设计风格系统，提供暖色暗调设计规范。当用户提到"understand-anything风格"、"暖色暗调"、"琥珀色主题"、"amber dark"、"温暖暗黑"、"像 understand-anything 那样"、"暗色暖调"、"黑底琥珀"等涉及该网站风格或类似设计的场景时触发此技能。也适用于用户需要暗色背景 + 暖色强调色 + 衬线标题搭配的设计方案时。即使用户没有明确说"风格"，只要上下文提到使用"有质感的暗色"、"暖色系暗色"、"金色暗色主题"等，也应触发。
---

# Understand Anything 设计风格系统

基于 https://understand-anything.com/ 提取的完整设计语言。用于生成 HTML 演示文稿、页面、组件时参考应用。

## 设计特征总览

这套风格的核心是**暗色暖调**——近黑背景（#0a0a0a）搭配琥珀色强调（#d4a574），通过暖色渐变文字、颗粒噪点纹理、衬线标题与无衬线正文的对比，营造出温润、有质感的科技感。

## 配色方案

```css
:root {
  --bg:        #0a0a0a;   /* 纯黑背景 */
  --surface:   #141414;   /* 卡片/表层面板，略浅于背景 */
  --border:    #1a1a1a;   /* 极细边框，几乎与背景融为一体 */
  --accent:    #d4a574;   /* 核心强调色 — 暖琥珀色 */
  --accent-glow: rgba(212, 165, 116, .15);
  --text:      #e8e2d8;   /* 暖白文字，带有轻微米色 */
  --text-muted:#8a8578;   /* 辅助文字，暖灰 */
  --grad-cool: #c9867a;   /* 渐变冷端 — 灰玫瑰 */
  --grad-mid:  #b8865c;   /* 渐变中端 — 琥珀 */
  --grad-warm: #d4a574;   /* 渐变暖端 — 金棕 */
}
```

**核心渐变**：`linear-gradient(135deg, var(--grad-cool), var(--grad-mid), var(--grad-warm))`

### 配色使用规则

- 深色背景（`--bg`）上全部使用白色系文字（`--text` / `--text-muted`）
- `--accent` 用于按钮、链接、高亮、焦点边框
- `--accent-glow` 用于按钮阴影、卡片发光
- 渐变文字仅用于**标题层级**，不使用在正文
- 卡片边框使用 `--border`，选中/强调状态切换为 `rgba(212, 165, 116, .3)`

## 字体

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:wght@400&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --font-heading: 'DM Serif Display', Georgia, 'Times New Roman', serif;
  --font-body:    'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-code:    'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}
```

| 用途 | 字体 | 字重 | 说明 |
|------|------|------|------|
| 标题 | DM Serif Display | 400 | 衬线体，与无衬线正文形成强烈对比 |
| 正文 | Inter | 400 / 600 | 干净可读，600 用于加粗强调 |
| 代码/标签 | JetBrains Mono | 400 | 等宽，用于小型标签、代码块 |

## 核心设计模式

### 1. 渐变文字

仅用于主标题和关键强调词。背景使用核心渐变 + `background-clip: text`。

```css
.grad-text {
  background: linear-gradient(135deg, #c9867a, #b8865c, #d4a574);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 2. 颗粒噪点纹理

固定全屏的 SVG 噪点层，为暗色背景增加深度。

```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: .03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

### 3. 卡片

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 2rem;
  transition: border-color .3s ease, box-shadow .3s ease;
}
.card:hover {
  border-color: rgba(212, 165, 116, .25);
  box-shadow: 0 0 24px var(--accent-glow);
}
```

### 4. 毛玻璃导航栏

```css
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1rem 2rem;
  transition: background-color .3s ease, backdrop-filter .3s ease;
}
.nav.scrolled {
  background-color: rgba(10, 10, 10, .85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
```

### 5. 按钮

主要按钮使用 `--accent` 背景 + 黑色文字，带发光阴影：
```css
.btn-primary {
  background: var(--accent);
  color: var(--bg);
  padding: .85rem 2.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: box-shadow .3s ease, transform .2s ease;
}
.btn-primary:hover {
  box-shadow: 0 0 30px var(--accent-glow);
  transform: translateY(-2px);
}
```

次要按钮使用 `--accent` 边框 + 透明背景。

### 6. 药丸标签（Pill）

```css
.pill {
  font-family: var(--font-code);
  font-size: .8rem;
  color: var(--text-muted);
  padding: .4rem 1rem;
  border: 1px solid rgba(138, 133, 120, .25);
  border-radius: 100px;
  background: rgba(255, 255, 255, .03);
}
.pill-accent {
  color: var(--accent);
  border-color: rgba(212, 165, 116, .3);
  background: rgba(212, 165, 116, .06);
}
```

### 7. 终端风格 UI

代码块包含窗口标题栏（红/黄/绿圆点）：
```html
<div class="terminal">
  <div class="terminal-titlebar">
    <span class="dot red"></span>
    <span class="dot yellow"></span>
    <span class="dot green"></span>
    <span class="terminal-title">Label</span>
  </div>
  <pre><code>...</code></pre>
</div>
```
```css
.dot.red    { background: #ff5f57; }
.dot.yellow { background: #ffbd2e; }
.dot.green  { background: #28c840; }
```

### 8. 动画 — fadeSlideUp

```css
@keyframes fadeSlideUp {
  0%   { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}
.reveal { opacity: 0; }
.reveal.visible { animation: fadeSlideUp .8s ease-out forwards; }
.reveal-delay-1 { animation-delay: .1s; }
.reveal-delay-2 { animation-delay: .25s; }
.reveal-delay-3 { animation-delay: .4s; }
```

配合 Intersection Observer 在滚动进入视口时触发：
```javascript
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: .15 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### 9. 对比卡片

用于"前后对比"场景，两个卡片并排：
- **旧方案**：半透明（`opacity: .7`），无发光
- **新方案**：带 `--accent` 发光边框（`box-shadow: 0 0 40px var(--accent-glow)`）

### 10. 领域标签组

代码/领域标签使用 `font-family: var(--font-code)` + 通明背景：
```css
.domain-badge {
  background: linear-gradient(135deg, rgba(201, 134, 122, .15), rgba(212, 165, 116, .15));
  border: 1px solid rgba(212, 165, 116, .3);
  border-radius: 6px;
  padding: .4rem .85rem;
  font-weight: 600;
}
.domain-item {
  font-family: var(--font-code);
  font-size: .8rem;
  background: rgba(255, 255, 255, .03);
  border-radius: 4px;
  padding: .3rem .6rem;
}
```

## 与其他技能配合

当用户需要生成 HTML 演示文稿时：
1. 委托 `frontend-slides` 技能完成 HTML 框架生成
2. 本技能提供完整的设计系统规范供 `frontend-slides` 使用
3. 在生成的演示文稿中应用本规范的全部设计模式

## 禁止事项

- ❌ 使用冷色强调色（蓝色、青色）— 必须使用暖琥珀色 `#d4a574`
- ❌ 使用纯白色文字（#ffffff）— 必须使用暖白 `#e8e2d8`
- ❌ 亮色背景 — 必须使用近黑背景 `#0a0a0a`
- ❌ 无衬线字体作标题 — 标题必须使用 `DM Serif Display`
- ❌ 使用 emoji — 使用几何符号或 Font Awesome 图标
- ❌ 平面无质感设计 — 必须添加噪点纹理和微光晕
