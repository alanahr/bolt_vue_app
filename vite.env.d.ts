/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND_URI: string
  readonly VITE_BACKEND_PORT: string
  readonly VITE_BACKEND_WSURI: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare const __API_URL__: string