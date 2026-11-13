import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import {fileURLToPath} from 'node:url';

export default defineConfig({
  plugins: [react({jsxImportSource:'@carelink/i18n'})],
  resolve: {alias: {'@carelink/i18n':fileURLToPath(new URL('./src/i18n',import.meta.url))}},
  optimizeDeps: {exclude:['@carelink/i18n/jsx-runtime','@carelink/i18n/jsx-dev-runtime']},
});
