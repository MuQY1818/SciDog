import { app as t, BrowserWindow as m, dialog as f, shell as k } from "electron";
import o from "path";
import { spawn as b } from "child_process";
import { fileURLToPath as D } from "url";
import c from "fs";
const v = D(import.meta.url), h = o.dirname(v);
process.env.DIST_ELECTRON = o.join(h, ".");
process.env.DIST = o.join(process.env.DIST_ELECTRON, "../dist");
process.env.PUBLIC = process.env.VITE_DEV_SERVER_URL ? o.join(process.env.DIST_ELECTRON, "../public") : process.env.DIST;
const S = process.env.NODE_ENV !== "production";
let e = null, r = null;
function T() {
  return new Promise((n, s) => {
    if (S)
      return console.log("Development mode: Assuming backend is running separately."), n();
    const p = o.join(process.resourcesPath, "backend", "dist", "scidog_backend.exe"), E = o.dirname(p), l = t.getPath("userData"), d = o.join(l, "backend.log");
    c.existsSync(l) || c.mkdirSync(l, { recursive: !0 }), c.writeFileSync(d, `--- Log started at ${(/* @__PURE__ */ new Date()).toISOString()} ---
`);
    const g = c.createWriteStream(d, { flags: "a" });
    f.showMessageBox({
      type: "info",
      title: "Backend Logging",
      message: "The backend service is starting.",
      detail: `For debugging purposes, logs are being written to:
${d}

If the application fails to load data, please check this file.`
    }), e = b(p, [], { cwd: E }), e.stdout.pipe(g), e.stderr.pipe(g);
    const i = (a) => {
      const u = a.toString();
      console.log(`Backend: ${u}`), u.includes("Running on http://127.0.0.1:5000") && (console.log("Backend is ready!"), e.stdout.removeListener("data", i), e.stderr.removeListener("data", i), n());
    };
    e.stdout.on("data", i), e.stderr.on("data", i), e.on("error", (a) => {
      console.error("Failed to start backend process.", a), s(a);
    }), setTimeout(() => {
      s(new Error("Backend startup timed out after 20 seconds. Check the log file for errors."));
    }, 2e4);
  });
}
const _ = o.join(h, "preload.mjs"), R = process.env.VITE_DEV_SERVER_URL, I = o.join(process.env.DIST, "index.html");
async function w() {
  r = new m({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: _,
      nodeIntegration: !1,
      contextIsolation: !0
    }
  }), r.webContents.setWindowOpenHandler(({ url: n }) => (n.startsWith("http") && k.openExternal(n), { action: "deny" })), process.env.VITE_DEV_SERVER_URL ? (r.loadURL(R), r.webContents.openDevTools()) : r.loadFile(I);
}
t.on("window-all-closed", () => {
  process.platform !== "darwin" && t.quit();
});
t.on("will-quit", () => {
  e && (console.log("Terminating backend process..."), e.kill());
});
t.on("activate", () => {
  m.getAllWindows().length === 0 && w();
});
t.commandLine.appendSwitch("disable-gpu");
t.whenReady().then(async () => {
  try {
    await T(), w();
  } catch (n) {
    console.error("Fatal error during startup:", n);
    const s = o.join(t.getPath("userData"), "backend.log");
    f.showErrorBox(
      "Application Startup Error",
      `Failed to start the backend service. The application will now close.

Details: ${n.message}

Please check the log file for more information:
${s}`
    ), t.quit();
  }
});
