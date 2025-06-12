const { app: t, BrowserWindow: c, shell: i } = require("electron"), s = require("path"), { spawn: a } = require("child_process");
process.env.DIST_ELECTRON = s.join(__dirname, "..");
process.env.DIST = s.join(process.env.DIST_ELECTRON, "../dist");
process.env.PUBLIC = process.env.VITE_DEV_SERVER_URL ? s.join(process.env.DIST_ELECTRON, "../public") : process.env.DIST;
const d = process.env.NODE_ENV !== "production";
let o = null;
function l() {
  if (d) {
    console.log("Development mode: Backend process not started by Electron.");
    return;
  }
  const n = s.join(process.resourcesPath, "backend", "dist", "scidog_backend.exe");
  console.log(`Starting backend at: ${n}`), o = a(n), o.stdout.on("data", (e) => {
    console.log(`Backend stdout: ${e}`);
  }), o.stderr.on("data", (e) => {
    console.error(`Backend stderr: ${e}`);
  }), o.on("close", (e) => {
    console.log(`Backend process exited with code ${e}`);
  });
}
async function r() {
  const n = new c({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: s.join(__dirname, "preload.js")
    }
  });
  n.webContents.setWindowOpenHandler(({ url: e }) => (e.startsWith("http") && i.openExternal(e), { action: "deny" })), process.env.VITE_DEV_SERVER_URL ? (n.loadURL(process.env.VITE_DEV_SERVER_URL), n.webContents.openDevTools()) : n.loadFile(s.join(process.env.DIST, "index.html"));
}
t.on("window-all-closed", () => {
  process.platform !== "darwin" && t.quit();
});
t.on("will-quit", () => {
  o && (console.log("Terminating backend process..."), o.kill());
});
t.on("activate", () => {
  c.getAllWindows().length === 0 && r();
});
t.whenReady().then(() => {
  l(), r();
});
