# UI/UX PRD — AI Learning Path Recommender

**Generated using:** `ui-ux-pro-max` skill (design-system + ux + chart + icons + react-stack domain queries)
**Goal:** an interface that feels conversational and light on first touch, then becomes an easily-scannable, navigable roadmap + dashboard as the learner progresses.

> Every recommendation below is either pulled directly from the skill's local design database (marked ✅ verified match) or explicitly flagged as a fallback where the database had no match — per the skill's own no-fabrication rule.

---

## 1. Design System (✅ verified — `--design-system` query: "AI learning platform education dashboard")

### Visual direction
- **Style:** AI-Native UI — conversational, minimal chrome, streaming text, ambient assistant feel. Best-fit category for chatbot/copilot-style products.
- **Pattern:** Product-demo-led structure (hero → live interaction → feature breakdown), adapted here as: Chat onboarding → Roadmap reveal → Dashboard.
- **Key effects:** typing indicators (3-dot pulse), streaming text as the LLM responds, soft context cards, smooth reveals — not hard cuts.
- **Anti-patterns to avoid:** heavy chrome (no dense toolbars around the chat), slow response feedback (always show a loading/typing state within ~150ms of a user action).

### Color tokens

| Role | Hex | Use |
|---|---|---|
| Primary | `#7C3AED` | Primary actions, active nav, selected roadmap node |
| Secondary | `#A78BFA` | Secondary accents, hover states |
| Accent/CTA | `#0891B2` | "Continue learning" / key CTA button |
| Background | `#FAF5FF` | App background |
| Foreground | `#1E1B4B` | Body text |
| Card | `#FFFFFF` | Cards, panels, chat bubbles |
| Muted | `#ECEEF9` | Disabled/locked roadmap nodes |
| Muted Foreground | `#475569` | Secondary text, timestamps |
| Border | `#DDD6FE` | Card borders, dividers |
| Destructive | `#DC2626` | Errors, "skip" warnings |
| Ring | `#7C3AED` | Focus ring (keyboard nav) |

Status colors for roadmap nodes (derived, not raw hex in components — use semantic tokens): `--status-locked` (muted gray), `--status-current` (primary purple), `--status-done` (success green), `--status-skipped` (warning amber).

### Typography
- **Font:** Inter (heading + body — cross-platform, dashboard-friendly, good at small sizes for data-dense screens).
- **Scale:** 12 / 14 / 16 / 18 / 24 / 32px — consistent modular scale, base body at 16px, line-height 1.5.
- **Import:** `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');`

### Design dials for this product
- **Density: 8/10 (dashboard-dense)** for the progress dashboard screen — 8–32px spacing scale, more information per view.
- **Density: 3/10 (spacious)** for the onboarding chat screen — 24–96px spacing, one thing at a time, low cognitive load for a first-time conversational flow.
- **Motion: 5/10 (standard)** — streaming text, node reveals, and milestone-complete celebrations use standard scroll/stagger motion, not complex choreography. Keep it calm; this is a learning tool, not a marketing site.

---

## 2. Information Architecture — 4 primary screens

```
1. Onboarding Chat  →  2. Roadmap View  →  3. Dashboard  →  4. Resource/Explain Panel
        (entry)          (main artifact)      (home base)      (drill-in, contextual)
```

- **Onboarding Chat** — first-run only, conversational, low density, revisitable via a persistent "chat" affordance (never fully hidden — this is also the ongoing Q&A surface per requirement 6.5).
- **Roadmap View** — the core deliverable made visual: milestones as a vertical stepper (mobile) / horizontal-scroll timeline (desktop), nodes color-coded by status.
- **Dashboard** — return-visit home base: skill radar, "what's next" card, progress stats.
- **Resource/Explain Panel** — a slide-over or modal triggered from any roadmap node: shows the "why this?" explanation and lets the learner mark complete/skip or ask a follow-up in chat.

**Navigation rule (✅ verified — Navigation/Breadcrumbs guideline):** use breadcrumbs only if the roadmap ever exceeds 3+ nested levels (e.g., Domain → Milestone → Resource); for a flat milestone list, skip breadcrumbs entirely — a persistent top nav (Chat / Roadmap / Dashboard) is enough.

**Sticky nav rule (✅ verified):** if the top nav is sticky, compensate with `padding-top` equal to nav height so it never overlaps the first roadmap node or chat message.

---

## 3. Screen-by-screen UX spec

### 3.1 Onboarding Chat
- Single-column, centered, max-width ~640px — spacious density.
- Learner types goal in free text; assistant responds with streaming text + typing indicator (3-dot pulse) while the LLM extracts profile fields.
- **Progressive disclosure, not a form dump:** ask one follow-up at a time ("What's your experience with SQL?") rather than a multi-field form up front.
- **User freedom (✅ verified — Onboarding/User Freedom):** always show a "Skip for now, use defaults" option and a way to go back and correct a previous answer — never a locked, linear, unskippable sequence.
- As soon as enough fields are captured, show an inline "Generating your roadmap…" transition state (loading → success, never a silent gap) that hands off to the Roadmap View.

### 3.2 Roadmap View (core artifact)
- **Desktop:** horizontal milestone timeline, each milestone a card cluster; scroll right to progress through time. **Mobile:** vertical stepper — this avoids horizontal scroll on small viewports, which the skill explicitly flags as an anti-pattern.
- Node states, visually distinct (not color-only — see accessibility below): `locked` (muted, lock icon), `current` (primary color, subtle pulse/glow), `done` (checkmark), `skipped` (dashed border + warning tone).
- Tapping/clicking a node opens the **Resource/Explain Panel** (slide-over, not full navigation away — keeps roadmap context visible).
- Milestone headers use the modular type scale (18–24px) so the page scans at a glance without reading every node.

### 3.3 Dashboard (home base, high-density)
Three zones, in priority order:
1. **"Next recommended action"** card — top of page, one clear CTA (Accent/CTA color `#0891B2`), not buried below stats.
2. **Skill development view** — ✅ verified chart pick: **Radar chart** for comparing the learner across a fixed set of skill dimensions (5–8 axes ideal; beyond 8, the data itself recommends switching to a grouped bar or parallel coordinates instead of cramming the radar).
   - Accessibility requirement from the chart data: never rely on the radar's color/shape alone — pair with a small data table or a "view as list" toggle, and label each axis directly.
3. **Milestone/overall progress** — ✅ verified chart pick: **Bullet chart** or simple progress bar for "% through current milestone," since this is a performance-vs-target metric, not a trend. Use a **line chart** only if/when you want to show progress *over time* (e.g., resources completed per week) — don't use a line chart for a single point-in-time completion percentage.
- Cards use the dense 8–32px spacing scale — this screen is meant to be scanned, not read top to bottom like the chat.

### 3.4 Resource/Explain Panel
- Slide-over panel (not a full page navigation) — preserves roadmap context underneath.
- Structure: resource title/format/duration → one-paragraph "why this was recommended" (ties back to the learner's stated goal/gap) → actions: **Mark complete**, **Skip**, **Ask a question** (opens inline chat scoped to this resource).
- **Submit feedback rule (✅ verified):** every action (mark complete, skip) must show a loading state then a clear success/error confirmation — never a silent click with no visible response.
- **Live status updates (✅ verified — Contextual Live Badge Updates):** when marking a node complete triggers a re-rank of the remaining path, announce it as one meaningful status message (e.g. "Roadmap updated — 2 resources adjusted") via `role="status" aria-atomic="true"`, not a bare changing number, and don't steal keyboard focus away from where the learner was.

---

## 4. Interaction & motion

- Streaming text for AI responses (chat + "why this recommendation" explanations) — reinforces the AI-native feel and gives instant feedback that something is happening.
- Node status changes (locked → current, current → done) animate with a smooth reveal, not an instant snap — motion should *convey* the state change, not just decorate it.
- Respect `prefers-reduced-motion` everywhere — disable streaming/pulse effects and use instant-but-clear state changes instead.
- Standard transition timing: 150–300ms for hover/focus states; nothing longer for anything the learner does repeatedly (marking resources complete will happen often — keep it snappy).

---

## 5. Accessibility (Priority 1 in the skill's own rule ranking — treat as non-negotiable, not a stretch item)

- Text contrast ≥ 4.5:1 in both light and dark mode (the Foreground/Background pair above passes this).
- Full keyboard navigation: every roadmap node, chat input, and dashboard control reachable and operable via keyboard, with a visible focus ring using the `--color-ring` token — never remove focus outlines.
- Heading hierarchy must be sequential (h1 page title → h2 section → h3 card), never skipped for styling reasons.
- Icon-only buttons (e.g. a lock icon on a locked node) need an `aria-label` — never rely on the icon alone.
- Charts: radar and bullet charts both need a non-visual fallback (data table / list view) — don't ship a chart as the *only* way to read skill progress.
- Minimum touch target 44×44px, 8px+ spacing between tappable roadmap nodes on mobile.

---

## 6. Icons ⚠️ fallback (no verified match)

A direct search for education/learning-specific icons ("book", "graduation cap", "course") returned **no match in the skill's icon database** — flagging this explicitly rather than inventing a result. Fallback guidance (general default, not a DB match): use an outline icon set such as **Lucide** or **Heroicons**, SVG only — never emoji as functional icons. Suggested icon roles: lock (locked node), check-circle (done), circle-dashed (current/in-progress), skip-forward (skipped), message-circle (chat), bar-chart-2 (dashboard).

---

## 7. React implementation notes (✅ verified — `--stack react` query: "list virtualize memo")

Relevant to this project specifically because the course catalog and roadmap node list can grow:

| Guideline | Why it matters here |
|---|---|
| Virtualize long lists (react-window / react-virtual) for lists over ~100 items | The course catalog browser (if exposed outside the roadmap) can exceed 100 items even at hackathon scale |
| Use stable IDs as `key`, never array index | Roadmap nodes get reordered on re-rank — index keys would cause visual glitches/lost state exactly when the adaptive feedback loop fires |
| Use `React.memo` only for components with real render cost and stable props (e.g. the radar chart), not blanket-applied to every small component | Keeps the dashboard responsive without premature optimization eating hackathon time |
| Generic typed list components (`<List<T> items={T[]}>`) over loose `any[]` typing | Roadmap nodes, courses, and chat messages are distinct shapes — generics catch mismatches before a demo-day bug |

---

## 8. Responsive breakpoints

Test at: **375px** (mobile), **768px** (tablet — roadmap may switch from vertical stepper to a 2-column milestone grid here), **1024px** (small desktop — horizontal timeline becomes viable), **1440px** (full dashboard with radar + bullet charts side by side). No horizontal scroll below 768px except within an explicitly scrollable component (never the page itself).

---

## 9. Pre-delivery checklist (✅ from skill's canonical list)

- [ ] No emojis as icons — SVG only (Lucide/Heroicons fallback, see §6)
- [ ] `cursor-pointer` on all clickable roadmap nodes and cards
- [ ] Hover states with 150–300ms smooth transitions
- [ ] Light mode text contrast ≥ 4.5:1 (dark mode supported per style match, verify separately)
- [ ] Visible focus states on every interactive element, keyboard-only pass done
- [ ] `prefers-reduced-motion` respected for streaming text, pulses, and reveals
- [ ] Responsive tested at 375 / 768 / 1024 / 1440px
- [ ] Every async action (mark complete, skip, re-rank) shows loading → success/error, never silent
- [ ] Charts have a non-color, non-visual fallback (table/list)
- [ ] Onboarding chat has Skip/Back — never a locked linear sequence

---

## 10. How this maps back to the six required modules

| Required module | Screen(s) | Design system element applied |
|---|---|---|
| Conversational interface | Onboarding Chat + chat-in-panel | AI-Native style, streaming text, typing indicator |
| Learner profiling engine | Onboarding Chat (backend-facing, no dedicated screen) | Progressive disclosure, skip/back affordances |
| Recommendation engine | Roadmap View nodes | Card pattern, status color tokens |
| Path generator | Roadmap View structure | Milestone timeline/stepper pattern |
| Explainability + assistant Q&A | Resource/Explain Panel | Slide-over pattern, submit-feedback loading states |
| Progress dashboard | Dashboard | Radar chart (skills) + bullet/progress bar (milestone %) |
