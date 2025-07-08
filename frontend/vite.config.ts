import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  //#todo do API url here?
  //          __API_URL__: JSON.stringify('http://localhost:8000')

  plugins: [vue()],
})
