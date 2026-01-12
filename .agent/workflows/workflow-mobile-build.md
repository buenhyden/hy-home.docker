---
description: Build and Run React Native/Expo Application
---

1. Check Environment
Ensure Node.js, Expo CLI, and standard dependencies are installed.

```bash
node -v
npm list -g expo-cli || npm install -g expo-cli
```

// turbo
2. Install Dependencies
Install modules if `node_modules` is missing or packages changed.

```bash
npm install
```

1. Select Platform
Determine if you are running on Android, iOS, or Web.

// turbo
4. Start Metro Bundler
Start the development server.

```bash
npx expo start
```

1. Build for Production (Optional)
If a build is requested, run EAS build.

```bash
eas build --profile production
```
