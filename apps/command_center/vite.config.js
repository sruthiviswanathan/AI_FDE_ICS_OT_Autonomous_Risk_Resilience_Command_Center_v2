import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const dir = path.dirname(fileURLToPath(import.meta.url));
const apiOrigin = process.env.OT_API_ORIGIN || "http://127.0.0.1:8001";

export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === "build" ? "/ui/static/" : "/",
  publicDir: false,
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    open: "/",
    proxy: {
      "/health": apiOrigin,
      "/diagnostics": apiOrigin,
      "/ops": apiOrigin,
      "/identity": apiOrigin,
      "/assets": apiOrigin,
      "/telemetry": apiOrigin,
      "/graph": apiOrigin,
      "/case": apiOrigin,
      "/risk": apiOrigin,
      "/safety": apiOrigin,
      "/recommendations": apiOrigin,
      "/access": apiOrigin,
      "/recovery": apiOrigin,
      "/authority": apiOrigin,
      "/recommend": apiOrigin,
      "/lookup": apiOrigin,
      "/ui": apiOrigin,
      "/docs": apiOrigin,
    },
  },
  build: {
    outDir: path.join(dir, "static"),
    emptyOutDir: false,
    cssCodeSplit: false,
    rollupOptions: {
      input: path.join(dir, "src/main.jsx"),
      output: {
        format: "es",
        entryFileNames: "app.js",
        assetFileNames: "app.css",
        inlineDynamicImports: true,
      },
    },
  },
}));
