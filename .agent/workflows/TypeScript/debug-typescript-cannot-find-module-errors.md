---
description: Fix TypeScript module resolution issues
---

1. **Check tsconfig.json Paths**:
   - Verify path mappings are correct.

   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["./src/*"],
         "@/components/*": ["./src/components/*"]
       }
     }
   }
   ```

2. **Restart TypeScript Server**:
   - VS Code: Cmd+Shift+P → "TypeScript: Restart TS Server".

3. **Check Module Resolution**:
   - Verify import paths match file structure.

   ```tsx
   // ❌ Wrong
   import { Button } from '@/Components/Button';
   // ✅ Correct (case-sensitive)
   import { Button } from '@/components/Button';
   ```

4. **Install Missing Type Definitions**:
   - Check if @types package exists.
   // turbo
   - Run `npm install --save-dev @types/node @types/react`

5. **Fix Declaration File Conflicts**:
   - Check for duplicate .d.ts files.
   - Exclude node_modules in tsconfig:

   ```json
   {
     "exclude": ["node_modules", "**/*.spec.ts"]
   }
   ```

6. **Clear TypeScript Cache**:
   - Delete build artifacts.
   // turbo
   - Run `rm -rf .next tsconfig.tsbuildinfo`

7. **Pro Tips**:
   - Use `moduleResolution: "bundler"` for modern projects.
   - Check `package.json` exports field for library imports.
   - Enable `skipLibCheck` to speed up compilation.
