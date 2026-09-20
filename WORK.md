# Todo List V2 — Work Instructions

## Objective

Implement the V2 specification in `SPEC.md` for the repository `Attention0/todo-list`.

Treat `SPEC.md` as the source of truth. Do not add out-of-scope product features unless they are required to satisfy the specification.

---

## Required workflow

1. Read the current `index.html`.
2. Read all of `SPEC.md`.
3. Inspect the existing V1 behavior before changing it.
4. Implement V2 in `index.html`.
5. Keep the project dependency-free and build-free.
6. Run the app in a browser using a local static server.
7. Test the acceptance criteria below.
8. Fix issues found during testing.
9. Create or update `RESULT.md` with an implementation and test report.
10. Commit and push the completed changes to GitHub.

If your environment supports branches / pull requests, prefer working on a branch such as:

`feature/todo-v2`

and open a pull request back to `main`.

If branch / PR creation is not practical in the current environment, commit to the available working branch and clearly report which branch and commit contain the result.

---

## Implementation requirements

### Preserve project simplicity

- Keep V2 in a single `index.html`.
- Do not introduce React, Vue, npm, bundlers, or external frameworks.
- Do not require any installation to run the final app.

### Implement all core V2 features

- Add tasks by button.
- Add tasks by Enter.
- Complete / restore tasks.
- Inline editing.
- Enter to save edit.
- Escape to cancel edit.
- Delete individual tasks.
- All / Active / Completed filters.
- Remaining / completed statistics.
- Clear completed.
- Empty states.
- `localStorage` persistence.
- Responsive desktop/mobile UI.

### Data

Use stable task IDs and preserve a structure equivalent to:

```js
{
  id,
  text,
  completed,
  createdAt
}
```

Do not use array indexes as task identity.

### Safe rendering

This is mandatory.

Never insert user-provided task text through unsafe `innerHTML` interpolation.

Render task text with `textContent` or another safe DOM API.

Explicitly test a task containing:

```html
<img src=x onerror=alert(1)>
```

It must appear as visible plain text and must not execute.

### UX

- Keep interactions fast.
- Do not add delete confirmation dialogs.
- Do not rely on hover-only controls.
- Keep focus states visible.
- Use explicit clickable controls for completion and task actions.

### Visual direction

Keep the purple identity from V1, but improve polish:

- softer purple / blue background
- refined centered card
- clear typography hierarchy
- consistent spacing
- subtle transitions
- useful active states
- mobile-friendly layout

Avoid over-design.

---

## Browser testing checklist

Verify each item manually in the browser:

- [ ] Page loads with no visible breakage.
- [ ] Empty state is shown when appropriate.
- [ ] Add a normal task using the Add button.
- [ ] Add a task using Enter.
- [ ] Whitespace-only task is rejected.
- [ ] Complete a task.
- [ ] Restore a completed task.
- [ ] Edit a task and save with Enter.
- [ ] Edit a task and cancel with Escape.
- [ ] Delete a task.
- [ ] All filter shows all tasks.
- [ ] Active filter shows only active tasks.
- [ ] Completed filter shows only completed tasks.
- [ ] Counts remain correct after all mutations.
- [ ] Clear completed removes completed tasks only.
- [ ] Refresh the page and confirm persistence.
- [ ] Add the literal text `<img src=x onerror=alert(1)>` and confirm it is not executed.
- [ ] Check a desktop-sized viewport.
- [ ] Check a mobile-sized viewport.
- [ ] Check browser console for obvious runtime errors.

---

## RESULT.md format

Create or replace `RESULT.md` using roughly this structure:

```md
# Todo List V2 — Implementation Result

## Summary
What was implemented.

## Files changed
- index.html
- RESULT.md
...

## Key implementation decisions
Important architecture / UX choices.

## Testing performed
List the browser tests performed and their results.

## Acceptance criteria
Mark each SPEC acceptance criterion pass/fail.

## Known issues
Any known limitations or remaining problems.

## Branch / commit
Branch name, commit SHA, and PR link if available.
```

Do not claim a test passed unless it was actually performed.

---

## Definition of done

The task is done only when:

1. V2 is implemented.
2. The browser version is actually run.
3. Core interactions are tested.
4. Any discovered defects are addressed where practical.
5. `RESULT.md` accurately records the result.
6. Changes are committed and pushed so Chat can review them from GitHub.
