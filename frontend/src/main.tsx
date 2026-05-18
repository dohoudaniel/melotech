import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Self-hosted Geist Sans font — bundled by Vite, no external CDN required.
import '@fontsource/geist-sans'
import './index.css'
import App from './App.tsx'

// StrictMode double-invokes certain lifecycle methods in development to
// surface side effects and deprecated patterns. No effect in production.
// The `!` non-null assertion tells TypeScript that #root always exists in index.html.
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
