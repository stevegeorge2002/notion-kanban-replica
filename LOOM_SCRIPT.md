# Loom Video Walkthrough Script
## 5-7 Minute Demo

---

### INTRODUCTION (30 seconds)

"Hi! I'm Steve, and I'll be walking you through my Notion Kanban Board replica for the Full-Stack Engineer assessment. I completed this in 3.5 hours using a pure Python stack - Reflex for the frontend and FastAPI for the backend. Let me show you what I built."

---

### DEMO: VISUAL FIDELITY (2 minutes)

**[Split screen: Notion vs. My Replica]**

"First, let's talk about visual fidelity. I opened Notion side-by-side with my replica to show you the pixel-perfect match."

**[Point to colors]**
"I extracted Notion's exact color palette using Chrome DevTools:
- Background: #f7f6f3 - this subtle warm gray
- Card borders: #e3e2e0
- Text colors: #37352f for primary, #787774 for secondary
- The blue accent: #2383e2 for interactive elements"

**[Point to spacing]**
"Spacing is identical:
- 16px between columns
- 8px between cards
- 12px padding inside cards
- 3px border radius on cards, 6px on modals"

**[Show shadows]**
"I matched the exact shadow values:
- Cards: 0 1px 3px with 12% opacity
- Modals: 0 8px 32px with 24% opacity
- On hover, cards get a deeper shadow for elevation"

**[Show hover states]**
"Notice the hover interactions:
- Action buttons fade in smoothly
- Cards lift with deeper shadows
- Cursor changes to 'grab' during drag"

**[Show typography]**
"Typography matches Notion's system font stack: -apple-system, then Segoe UI, then Roboto as fallbacks. Title is 14px at 500 weight, descriptions are 12px at 400 weight."

---

### DEMO: FUNCTIONALITY (2 minutes)

**[Demonstrate features]**

"Now let's test the functionality. Everything is fully interactive:"

**Create Column:**
"I'll click 'Add Column' - modal appears with smooth animation. Type 'Testing' - notice the Notion-blue focus ring. Click Create."

**Add Cards:**
"Each column has a + button on hover. I'll add a card: 'Build API endpoints'. The card position is automatically managed."

**Edit Card:**
"Hover over a card - Edit and Delete buttons appear. Click Edit - modal pre-fills with existing data. I'll add a description: 'FastAPI with Pydantic validation'. Save."

**Drag and Drop:**
"Now the key feature - drag and drop. Watch the cursor change to 'grabbing'. I'll drag this card from 'To Do' to 'In Progress'. The API updates positions in real-time, no conflicts."

**Delete:**
"Hover actions work on columns too. Each column can be deleted - this cascades and removes all cards inside."

**Persistence:**
"Let me refresh the page. Everything persists in SQLite. All changes are saved via the RESTful API."

---

### CODE WALKTHROUGH (2 minutes)

**[Show project structure]**

"Let's look at the architecture. This is a pure Python full-stack application."

**Backend (app/api.py):**
"The FastAPI backend has RESTful endpoints:
- GET/POST/DELETE for columns
- CRUD operations for cards
- A special PATCH endpoint for moving cards that handles position reordering

Here's the move_card endpoint - it updates the card's column_id and position, then reorders all affected cards in both the old and new columns to prevent conflicts."

**Database (app/models.py):**
"SQLAlchemy models with relationships:
- BoardColumn has many Cards
- Cascade delete ensures removing a column removes its cards
- Position fields maintain card order within columns"

**Frontend (app/components/):**
"Reflex components are pure Python but compile to React:
- board.py orchestrates the layout
- column.py renders each column with its cards
- card.py handles individual card styling and drag events
- modal.py creates the dialog overlays

This is actual Python code that generates type-safe React components."

**State Management (app/state.py):**
"KanbanState manages:
- API calls using httpx async client
- UI state like modal visibility
- Drag-drop tracking
- Data loading and updates

All state updates trigger automatic re-renders."

**Custom CSS (assets/styles.css):**
"I added custom CSS for:
- Hover effect transitions
- Drag cursor states
- Smooth scrollbars
- Modal animations
- Notion-style focus rings"

---

### WORKFLOW EFFICIENCY (1.5 minutes)

"Let me explain my workflow that allowed me to complete this in 3.5 hours:"

**Python-First Development:**
"Using Reflex meant I never left Python. No context switching between JavaScript and Python. Reflex auto-generates React components, so I get the benefits of React without writing JSX."

**AI-Assisted Coding:**
"I used Claude and GitHub Copilot heavily:
- Generated component structures: 'Create a Reflex card component with drag-drop'
- Auto-completed CSS matching Notion's design system
- Scaffolded API endpoints with validation
- This saved approximately 60 minutes of boilerplate"

**Browser DevTools:**
"I inspected Notion's live site:
- Extracted computed CSS values directly
- Measured spacing with the pixel ruler
- Copied shadow and color values
- This saved 30 minutes of trial-and-error styling"

**Reflex Hot Reload:**
"Changes appear instantly - no build step. This tight feedback loop accelerated UI development significantly."

---

### TESTING (30 seconds)

**[Show terminal]**

"I built a pytest suite covering all API endpoints:
- Column CRUD operations
- Card CRUD and position management
- Cascade deletes
- Card movement between columns

Running pytest... 10 tests, all passing in under 2 seconds."

---

### CLOSING (30 seconds)

"This replica demonstrates:
✓ Pixel-perfect visual replication using DevTools inspection
✓ Full-stack Python expertise with Reflex and FastAPI
✓ Aggressive use of AI tools and automation
✓ Clean, modular, production-ready code
✓ Comprehensive test coverage
✓ Fast execution - 3.5 hours total

The application is ready to deploy via Docker and scale with PostgreSQL, Redis caching, and WebSocket collaboration.

Thanks for watching! The full code is available in the GitHub repository with detailed documentation."

---

### RECORDING TIPS

**Setup:**
1. Close unnecessary browser tabs
2. Clear terminal history
3. Reset database to clean state with sample data
4. Have Notion.so open in split screen
5. Test screen recording resolution (1080p minimum)
6. Use a good microphone

**During Recording:**
- Speak clearly and at moderate pace
- Use cursor to highlight what you're discussing
- Pause briefly between sections
- Show, don't just tell (always demonstrate)
- Keep energy high and enthusiasm genuine

**After Recording:**
- Add chapter markers in Loom:
  * 0:00 - Introduction
  * 0:30 - Visual Fidelity
  * 2:30 - Functionality Demo
  * 4:30 - Code Architecture
  * 6:00 - Workflow Efficiency
  * 7:30 - Testing & Closing
