# Visual Design Specifications
## Notion Kanban Board - Complete Reference

---

## 🎨 Color Palette

### Primary Colors
```css
Background (Page):      #ffffff
Background (Board):     #f7f6f3  /* Subtle warm gray */
Column Background:      #f7f6f3
Column Header:          #e9e9e7  /* Default gray */
Card Background:        #ffffff
```

### Text Colors
```css
Primary Text:           #37352f  /* Dark gray, almost black */
Secondary Text:         #787774  /* Medium gray */
Tertiary Text:          #9b9a97  /* Light gray for empty states */
```

### Border Colors
```css
Primary Border:         #e3e2e0  /* Light gray */
Hover Border:           #d3d2d0  /* Slightly darker on hover */
Focus Border:           #2383e2  /* Notion blue */
```

### Interactive Colors
```css
Accent Blue:            #2383e2  /* Buttons, links, focus */
Hover Background:       rgba(0, 0, 0, 0.05)  /* Button hover */
Delete Red:             #eb5757  /* Danger actions */
Success Green:          #81ecec  /* Optional: "Done" column */
Warning Yellow:         #ffeaa7  /* Optional: "In Progress" */
```

### Shadow Colors
```css
Card Shadow:            rgba(0, 0, 0, 0.12)
Card Hover Shadow:      rgba(0, 0, 0, 0.15)
Card Drag Shadow:       rgba(0, 0, 0, 0.16)
Modal Shadow:           rgba(0, 0, 0, 0.24)
```

---

## 📐 Spacing System

### Layout Spacing
```css
Page Padding:           24px 32px
Board Column Gap:       16px
Card Gap (vertical):    8px
```

### Component Padding
```css
Card Padding:           12px
Column Padding:         16px
Column Header Padding:  12px 16px
Modal Padding:          24px
```

### Internal Spacing
```css
Stack Spacing (small):  4px
Stack Spacing (medium): 8px
Stack Spacing (large):  12px
Button Spacing:         4px 8px
```

---

## 🔤 Typography

### Font Family
```css
Primary Font Stack:
  -apple-system, 
  BlinkMacSystemFont, 
  'Segoe UI', 
  'Inter', 
  'Roboto', 
  'Oxygen', 
  'Ubuntu', 
  sans-serif
```

### Font Sizes
```css
Page Title:             28px (Heading)
Column Title:           14px
Card Title:             14px
Card Description:       12px
Card Count:             12px
Button Text:            13px (regular) / 11px (small)
```

### Font Weights
```css
Page Title:             700 (Bold)
Column Title:           600 (Semibold)
Card Title:             500 (Medium)
Card Description:       400 (Regular)
Card Count:             400 (Regular)
```

### Line Heights
```css
Card Title:             1.5
Card Description:       1.4
Default:                1.5
```

---

## 📦 Component Dimensions

### Columns
```css
Min Width:              280px
Max Width:              320px
Preferred Width:        300px
Min Height:             200px (cards area)
Border Radius:          6px
Border:                 1px solid #e3e2e0
```

### Cards
```css
Width:                  100% (fill column)
Min Height:             auto (content-based)
Border Radius:          3px
Border:                 1px solid #e3e2e0
```

### Buttons
```css
Height (regular):       32px
Height (small):         24px
Padding (regular):      8px 16px
Padding (small):        4px 8px
Border Radius:          4px
```

### Modals
```css
Max Width:              500px (card modal)
Max Width:              400px (column modal)
Border Radius:          8px
Min Height:             auto
```

### Icons
```css
Size (regular):         16px
Size (small):           14px
Size (large):           18px
```

---

## 🎭 Shadows & Elevation

### Card Shadows
```css
Default:
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);

Hover:
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

Dragging:
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.16);
```

### Modal Shadow
```css
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.24);
```

### No Shadow
```css
Columns: no box-shadow
Column Headers: no box-shadow
```

---

## 🎬 Animations & Transitions

### Transition Durations
```css
Fast:                   0.1s (button press)
Default:                0.2s (hover, focus)
Slow:                   0.3s (modal open/close)
```

### Transition Properties
```css
All:                    all 0.2s ease
Opacity:                opacity 0.2s ease
Transform:              transform 0.2s ease
Box-Shadow:             box-shadow 0.2s ease
```

### Animation Curves
```css
Default:                ease
Bounce:                 cubic-bezier(0.68, -0.55, 0.265, 1.55)
Smooth:                 cubic-bezier(0.4, 0, 0.2, 1)
```

### Specific Animations
```css
Modal Fade In:
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  animation: fadeIn 0.2s ease;
```

---

## 🖱️ Interactive States

### Card States
```css
Default:
  background: #ffffff
  border: 1px solid #e3e2e0
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12)
  cursor: default

Hover:
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15)
  border-color: #d3d2d0

Dragging:
  cursor: grabbing
  opacity: 0.7
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.16)
```

### Button States
```css
Default:
  background: transparent (ghost)
  color: #787774

Hover:
  background: rgba(0, 0, 0, 0.05)
  color: #37352f

Active:
  background: rgba(0, 0, 0, 0.08)
  transform: scale(0.98)

Disabled:
  opacity: 0.4
  cursor: not-allowed
```

### Input States
```css
Default:
  border: 1px solid #e3e2e0
  background: #ffffff

Focus:
  border: 1px solid #2383e2
  box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.1)
  outline: none

Error:
  border: 1px solid #eb5757
  box-shadow: 0 0 0 2px rgba(235, 87, 87, 0.1)
```

---

## 🎯 Cursor States

```css
Default:                default
Clickable:              pointer
Draggable:              grab
Dragging:               grabbing
Text Input:             text
Not Allowed:            not-allowed
```

---

## 📱 Responsive Breakpoints

```css
Mobile:                 < 768px
Tablet:                 768px - 1024px
Desktop:                > 1024px
```

### Responsive Adjustments

**Mobile (< 768px):**
```css
Column Min Width:       260px (reduced from 280px)
Page Padding:           16px (reduced from 24px 32px)
Horizontal Scroll:      enabled for columns
```

**Tablet (768px - 1024px):**
```css
Column Width:           280px
Show 2-3 columns:       depending on screen width
```

**Desktop (> 1024px):**
```css
Column Width:           300px
Show 3+ columns:        optimal viewing
```

---

## 🔧 Scrollbar Styling

```css
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f7f6f3;
}

::-webkit-scrollbar-thumb {
  background: #d3d2d0;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #b4b3b0;
}
```

---

## ✨ Special Effects

### Hover Reveal
```css
/* Action buttons hidden by default */
.card-actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}

/* Reveal on card hover */
.kanban-card:hover .card-actions {
  opacity: 1;
}
```

### Focus Ring
```css
/* Notion-style focus */
input:focus, textarea:focus {
  outline: none;
  border-color: #2383e2;
  box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.1);
}
```

### Smooth Scrolling
```css
html {
  scroll-behavior: smooth;
}
```

---

## 🎨 Column Color Variations (Optional)

```css
To Do (Gray):           #e9e9e7
In Progress (Yellow):   #ffeaa7
Done (Teal):            #81ecec
Blocked (Red):          #ffb3ba
Review (Purple):        #e0b3ff
```

---

## 📊 Z-Index Layers

```css
Base:                   0
Cards:                  1
Dragging Card:          10
Column Headers:         5
Dropdown Menus:         100
Modals:                 1000
Modal Overlay:          999
Tooltips:               1001
```

---

## 🖼️ Grid System (Board Layout)

```css
Display:                flex
Direction:              row
Gap:                    16px
Align Items:            flex-start
Overflow X:             auto
Padding:                24px 32px
```

---

## 📐 Aspect Ratios & Constraints

```css
Card Min Height:        auto (no minimum)
Card Max Height:        none (content-based)
Column Min Height:      200px (cards area only)
Column Max Height:      none (scroll if needed)
Modal Max Width:        500px
```

---

## 🎯 Accessibility

```css
Focus Visible:          2px solid #2383e2
Outline Offset:         2px
Min Touch Target:       44px x 44px (mobile)
Color Contrast:         4.5:1 minimum (WCAG AA)
```

---

## 💡 Design Principles

1. **Subtle over Loud:** Use soft colors, gentle shadows
2. **Consistent Spacing:** Multiples of 4px (4, 8, 12, 16, 24, 32)
3. **Smooth Interactions:** 0.2s is the sweet spot
4. **Hover Reveals:** Hide complexity until needed
5. **Focus on Content:** Minimize chrome, maximize content area
6. **System Fonts:** Fast loading, consistent across platforms
7. **Soft Shadows:** Low opacity, subtle elevation changes
8. **Rounded Corners:** Small radius (3-6px) for modern feel

---

## 📸 Screenshot Comparison Checklist

When comparing to Notion, verify:
- [ ] Background colors match exactly
- [ ] Text colors are identical
- [ ] Spacing between elements is pixel-perfect
- [ ] Shadows have same blur radius and opacity
- [ ] Border radius matches
- [ ] Font sizes and weights are correct
- [ ] Hover states behave the same
- [ ] Animations have similar timing
- [ ] Icons are the same size
- [ ] Overall proportions feel identical

---

**Use this document as reference during development and in the interview!**
