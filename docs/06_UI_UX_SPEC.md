# 06 - UI / UX Spec

The terminal UI should feel like a modern developer tool: keyboard-first, clean,
dark-theme friendly, and fast. It should not feel like a basic text-prompt app.

## Interaction model

- `devbrew` launches the interactive terminal UI.
- **Arrow keys** move between options.
- **Enter** selects an item.
- **Esc** / **q** goes back or quits where appropriate.
- A **footer** always shows the relevant keyboard shortcuts.

## Screens (Sprint 1)

- **Auth screen** - register (name, email, phone) and log in (email); clear
  inline error messages for invalid input.
- **Menu screen** - list of drinks, each showing name, price, size options, and a
  short description; navigable with arrow keys.
- **Customization screen** - choose size, milk option, sugar level, and extra
  shot; selections summarised for the order.

## Later screens (Sprint 2+)

Cart, tracking progress, ETA, rider details, order history, help, and health.
