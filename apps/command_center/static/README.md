# Build output (generated — do not edit)

This folder receives the production bundle from Vite:

```powershell
cd apps\command_center
npm run build
```

That writes `app.js` and `app.css` here. FastAPI serves them at `/ui/static/*`.

**Source of truth:** `../src/` (React). Edit JSX/CSS there, not files in this folder.
