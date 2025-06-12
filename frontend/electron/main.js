'use strict'

import { app, BrowserWindow, shell, dialog } from 'electron'
import path from 'node:path'
import { spawn } from 'child_process'
import { fileURLToPath } from 'node:url'

// Define __dirname for ES modules
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const isDevelopment = process.env.NODE_ENV !== 'production'
let backendProcess = null

function startBackend() {
  return new Promise((resolve, reject) => {
    // In development, assume the backend is started manually.
    if (isDevelopment) {
      console.log('Development mode: Assuming backend is running separately.')
      return resolve()
    }
  
    // In production, spawn the packaged executable.
    const backendExecutablePath = path.join(process.resourcesPath, 'backend', 'dist', 'scidog_backend.exe')
    const backendDir = path.dirname(backendExecutablePath)

    console.log(`Starting backend from: ${backendExecutablePath}`)
    console.log(`Setting backend working directory to: ${backendDir}`)

    backendProcess = spawn(backendExecutablePath, [], {
      // Set the correct working directory for the backend process
      cwd: backendDir,
    })
 
    backendProcess.stdout.on('data', (data) => {
      const output = data.toString()
      console.log(`Backend stdout: ${output}`)
      // A simple check to see if the server is ready
      if (output.includes('Running on http://127.0.0.1:5000')) {
        console.log('Backend is ready!')
        resolve()
      }
    })
 
    backendProcess.stderr.on('data', (data) => {
      console.error(`Backend stderr: ${data}`)
    })
 
    backendProcess.on('error', (err) => {
      console.error('Failed to start backend process.', err)
      dialog.showErrorBox('Backend Error', `Failed to start the backend service: ${err.message}`)
      reject(err)
    })
    
    backendProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Backend process exited with code ${code}`)
            dialog.showErrorBox('Backend Error', `The backend service exited unexpectedly with code ${code}.`)
        }
    })

    // Timeout to prevent hanging forever
    setTimeout(() => {
        reject(new Error('Backend startup timed out after 20 seconds.'))
    }, 20000)
  })
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      // In a pure static site context, nodeIntegration and contextIsolation
      // are less critical, but we keep them for security best practices.
      nodeIntegration: false,
      contextIsolation: true,
    },
  })

  // VITE_DEV_SERVER_URL is set by `vite-plugin-electron` in development
  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL)
    // Open DevTools in dev mode.
    win.webContents.openDevTools()
  } else {
    // Load the index.html from the dist folder in production
    win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'))
  }
}

app.on('will-quit', () => {
  if (backendProcess) {
    console.log('Terminating backend process...')
    backendProcess.kill()
  }
})

app.whenReady().then(async () => {
  try {
    await startBackend()
    createWindow()
  } catch (error) {
    console.error('Fatal error during startup:', error)
    dialog.showErrorBox('Application Startup Error', `Failed to start the backend service. The application will now close.\n\nDetails: ${error.message}`)
    app.quit()
  }
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
}) 