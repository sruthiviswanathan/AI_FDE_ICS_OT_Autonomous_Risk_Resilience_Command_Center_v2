import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(dir, "..", "..");
const preferred = process.env.OT_API_PORT || "8001";
const candidates = [...new Set([preferred, "8001", "8000"])];

async function healthy(origin) {
  try {
    const r = await fetch(origin + "/health", { signal: AbortSignal.timeout(800) });
    return r.ok;
  } catch {
    return false;
  }
}

function pythonBin() {
  const win = process.platform === "win32";
  const venv = path.join(repo, ".venv", win ? "Scripts\\python.exe" : "bin/python");
  if (fs.existsSync(venv)) return venv;
  return win ? "python" : "python3";
}

async function ensureApi() {
  for (const port of candidates) {
    const origin = `http://127.0.0.1:${port}`;
    if (await healthy(origin)) {
      console.log("API already running at " + origin);
      return origin;
    }
  }
  const origin = `http://127.0.0.1:${preferred}`;
  console.log("Starting API at " + origin);
  const child = spawn(
    pythonBin(),
    ["-m", "uvicorn", "ot_command.api:app", "--host", "127.0.0.1", "--port", preferred],
    {
      cwd: repo,
      env: {
        ...process.env,
        PYTHONPATH: path.join(repo, "src"),
        AI_ENABLED: process.env.AI_ENABLED || "0",
      },
      stdio: "inherit",
      windowsHide: true,
    },
  );
  child.on("error", (err) => {
    console.error("Failed to start API:", err.message);
  });
  for (let i = 0; i < 50; i++) {
    if (await healthy(origin)) return origin;
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error("API did not become ready at " + origin);
}

const origin = await ensureApi();
process.env.OT_API_ORIGIN = origin;

console.log("Starting React (Vite) at http://127.0.0.1:5173");
console.log("Edit JSX in src/. This is not npm run build — build only writes static files.");

const viteJs = path.join(dir, "node_modules", "vite", "bin", "vite.js");
const vite = spawn(process.execPath, [viteJs, "--open"], {
  cwd: dir,
  env: process.env,
  stdio: "inherit",
  windowsHide: true,
});
vite.on("exit", (code) => process.exit(code ?? 0));
