---
description: Create React Native project with Expo, TypeScript, and mobile best practices
---

1. **Initialize Expo project**

    Create a new Expo project with TypeScript template in your desired directory.

    ```bash
    npx create-expo-app@latest my-mobile-app --template
    cd my-mobile-app
    ```

    When prompted, select **TypeScript** template.

2. **Install essential dependencies**

    Install required packages for navigation, safe areas, and common utilities based on `500-Mobile/520-mobile-react-native-specific.md`.

    // turbo

    ```bash
    npx expo install react-native-safe-area-context
    npx expo install @react-navigation/native @react-navigation/native-stack
    npx expo install react-native-screens react-native-gesture-handler
    ```

3. **Install development tools**

    Install testing and code quality tools.

    // turbo

    ```bash
    npm install -D @testing-library/react-native @testing-library/jest-native jest-expo
    npm install -D prettier eslint-config-prettier
    npm install -D @types/react @types/react-native
    ```

4. **Create project structure**

    Set up the recommended directory structure for React Native Expo projects.

    Create directories:

    ```bash
    mkdir -p src/{components,screens,services,navigation,types,utils}
    mkdir -p src/services/{api,constants}
    mkdir -p assets/{images,fonts}
    ```

5. **Configure TypeScript**

    Ensure `tsconfig.json` has strict mode enabled:

    ```json
    {
      "extends": "expo/tsconfig.base",
      "compilerOptions": {
        "strict": true,
        "paths": {
          "@/*": ["./src/*"]
        }
      }
    }
    ```

6. **Setup ESLint and Prettier**

    Create `.prettierrc`:

    ```json
    {
      "semi": true,
      "singleQuote": true,
      "tabWidth": 2,
      "trailingComma": "es5"
    }
    ```

    Update `.eslintrc.js` to extend Expo and Prettier:

    ```javascript
    module.exports = {
      extends: ['expo', 'prettier'],
      rules: {
        'react/prop-types': 'off',
      },
    };
    ```

7. **Create navigation structure**

    Create basic navigation setup in `src/navigation/AppNavigator.tsx` following React Navigation best practices.

    Use typed navigation as per `500-Mobile/520-mobile-react-native-specific.md`:

    ```typescript
    export type RootStackParamList = {
      Home: undefined;
      Details: { id: string };
    };
    ```

8. **Setup safe area provider**

    Wrap your app with `SafeAreaProvider` in `App.tsx` according to mobile standards:

    ```typescript
    import { SafeAreaProvider } from 'react-native-safe-area-context';

    export default function App() {
      return (
        <SafeAreaProvider>
          {/* Your app content */}
        </SafeAreaProvider>
      );
    }
    ```

9. **Configure app.json**

    Update `app.json` with proper app name, slug, and platform configurations:

    ```json
    {
      "expo": {
        "name": "My Mobile App",
        "slug": "my-mobile-app",
        "version": "1.0.0",
        "orientation": "portrait",
        "icon": "./assets/icon.png",
        "userInterfaceStyle": "automatic",
        "splash": {
          "image": "./assets/splash.png",
          "resizeMode": "contain",
          "backgroundColor": "#ffffff"
        },
        "ios": {
          "supportsTablet": true,
          "bundleIdentifier": "com.example.mymobileapp"
        },
        "android": {
          "adaptiveIcon": {
            "foregroundImage": "./assets/adaptive-icon.png",
            "backgroundColor": "#ffffff"
          },
          "package": "com.example.mymobileapp"
        }
      }
    }
    ```

10. **Verify setup**

    Start the development server and test on simulator/emulator.

    // turbo

    ```bash
    npx expo start
    ```

    Press `i` for iOS simulator or `a` for Android emulator.

    Expected: App loads with Expo welcome screen.

11. **Initialize Git**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize React Native Expo project with TypeScript"
    ```

    **Next Steps:**

    - Review `agent/rules/500-Mobile/520-mobile-react-native-specific.md` for React Native patterns
    - Review `agent/rules/100-Frontend/107-frontend-typescript-expert-specific.md` for TypeScript best practices
    - Consider setting up state management (Zustand or React Query)
    - Setup testing with Jest and React Native Testing Library
