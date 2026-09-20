# Todo List V2 — Product & Technical Specification

## 1. Goal

Upgrade the current single-file Todo List from a basic demo into a polished, reliable small task-management app that is pleasant to use every day.

V2 should remain deliberately lightweight:

- Single-page frontend
- No backend
- No account system
- No database
- No build step
- Persist data with `localStorage`
- Keep implementation in a single `index.html` for this version

The focus is usability, visual polish, maintainable structure, and safe rendering.

---

## 2. Core user experience

A user should be able to:

1. Open the page and immediately understand what to do.
2. Add a task by clicking the add button or pressing Enter.
3. Mark a task complete or restore it to active.
4. Edit an existing task.
5. Delete a task.
6. Filter tasks by All / Active / Completed.
7. See how many tasks remain and how many are completed.
8. Clear all completed tasks at once.
9. Refresh or reopen the browser and keep existing tasks.
10. Use the app comfortably on desktop and mobile.

---

## 3. V2 feature requirements

### 3.1 Add task

- Provide a clear task input field.
- Provide an Add button.
- Pressing Enter while focused on the input must add the task.
- Trim leading/trailing whitespace.
- Empty or whitespace-only input must not create a task.
- After a successful add, clear the input and keep the interaction fast.

### 3.2 Complete / restore task

- Each task must have an explicit checkbox-style control.
- Clicking it toggles the task between active and completed.
- Completed tasks should have a visually subdued style and strike-through text.
- A completed task can be restored to active.

### 3.3 Edit task

- Each task must expose an Edit action, either directly or through a compact menu.
- Editing should happen inline.
- Enter saves the edit.
- Escape cancels the edit.
- Empty edited text must not replace the existing task.
- Editing must preserve the task's stable ID and creation timestamp.

### 3.4 Delete task

- Each task must expose a Delete action.
- Deletion should happen immediately without a confirmation modal.
- No undo feature is required in V2.

### 3.5 Filters

Provide three filters:

- All
- Active
- Completed

Filtering should update the visible task list immediately without changing the underlying stored tasks.

### 3.6 Statistics

Show useful live statistics, including:

- Number of active tasks remaining.
- Number of completed tasks.

A concise top or footer summary is enough, e.g.:
- "3 tasks remaining"
- "3 remaining · 2 completed"

### 3.7 Clear completed

- Show a "Clear completed" action when completed tasks exist.
- Clicking it removes all completed tasks.
- Hide or disable it when there are no completed tasks.

### 3.8 Empty states

Do not leave the list area blank.

Examples:
- All + no tasks: "No tasks yet. Add your first task."
- Active + no active tasks: "Everything is done 🎉"
- Completed + no completed tasks: "No completed tasks yet."

Wording may be refined, but the state must be clear and friendly.

### 3.9 Persistence

Use `localStorage`.

Recommended key:
`todo-v2-tasks`

Data should survive refreshes and browser restarts.

---

## 4. Data model

Each task should use a stable object structure:

```js
{
  id: "task_...",
  text: "Complete Homework 1",
  completed: false,
  createdAt: 1723456789000
}
```

Application state can remain simple:

```js
const state = {
  tasks: [],
  filter: "all"
};
```

Valid filter values:
- `all`
- `active`
- `completed`

Task IDs must not depend on the task's array index.

---

## 5. Technical architecture

Keep V2 in one `index.html`, but organize the JavaScript into clear responsibilities.

### Storage

Functions such as:

```js
loadTasks()
saveTasks()
```

### Actions

Functions such as:

```js
addTask()
toggleTask()
editTask()
deleteTask()
clearCompleted()
setFilter()
```

### Rendering

Functions such as:

```js
render()
renderTasks()
renderStats()
renderFilters()
renderEmptyState()
```

Exact names may differ, but storage, state mutation, and UI rendering should not be unnecessarily tangled.

---

## 6. Security requirement

User-entered task text must never be injected into the DOM through unsafe HTML interpolation.

Do not render task text using patterns like:

```js
element.innerHTML = `<span>${task.text}</span>`;
```

Use DOM APIs and `textContent` for user content:

```js
const span = document.createElement("span");
span.textContent = task.text;
```

The app should safely display strings such as:

```html
<img src=x onerror=alert(1)>
```

as plain text rather than executing them.

---

## 7. Visual design

Retain the current purple identity, but make the interface feel like a finished product rather than a tutorial demo.

Desired qualities:

- Calm
- Minimal
- Clear hierarchy
- Comfortable spacing
- Fast interactions
- Subtle animation only

Suggested visual direction:

- Soft purple / blue gradient background
- White or lightly translucent main card
- Main card around 520–620 px on desktop
- 12–18 px corner radii
- Light shadow
- System font stack
- Consistent 8 px-based spacing
- 150–200 ms hover / press / completion transitions
- Clear active filter state
- Distinct but unobtrusive destructive actions

Avoid excessive animation, glassmorphism, or decorative effects that reduce clarity.

---

## 8. Responsive behavior

### Desktop

- Center the app.
- Comfortable max width around 520–620 px.
- Keep actions visually tidy.

### Mobile

- Use almost full viewport width with sensible outer margin.
- Input and buttons must remain easy to tap.
- Do not rely on hover-only controls.
- Task actions must remain discoverable and tappable.
- Avoid horizontal scrolling.

---

## 9. Accessibility / interaction quality

At minimum:

- Buttons should be actual `button` elements.
- Interactive controls should be keyboard accessible.
- Focus states should be visible.
- Inputs should have an accessible label or equivalent ARIA labeling.
- Completed state should not be conveyed by color alone.
- Avoid tiny tap targets.

---

## 10. Out of scope for V2

Do NOT add these unless explicitly requested later:

- Login / accounts
- Backend
- Cloud sync
- Database
- Due dates
- Calendar
- Notifications
- Categories
- Tags
- Priority
- Drag-and-drop ordering
- Subtasks
- AI features
- Multi-user collaboration

These belong to a possible V3 or later.

---

## 11. Acceptance criteria

V2 is complete when all of the following are true:

1. A task can be added by button and Enter.
2. Empty tasks cannot be created.
3. A task can be completed and restored.
4. A task can be edited inline.
5. Enter saves an edit and Escape cancels it.
6. A task can be deleted.
7. All / Active / Completed filters work correctly.
8. Remaining and completed counts update correctly.
9. "Clear completed" removes only completed tasks.
10. Appropriate empty states appear.
11. Tasks persist after page refresh.
12. User task text is rendered safely via `textContent` or equivalent DOM-safe methods.
13. The page works at common desktop and mobile widths.
14. There are no obvious JavaScript console errors during normal use.
15. Existing V1 behavior is preserved where compatible.
16. The app remains runnable simply by opening `index.html` or serving the folder with a basic static server.

---

## 12. Product boundary

V2 should feel complete without becoming large.

The intended progression is:

V1 → basic working demo  
V2 → polished, usable local Todo app  
V3 → dates, priority, categories, richer task management  
V4 → backend, accounts, sync if ever needed
