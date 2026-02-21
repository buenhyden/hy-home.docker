---
description: Build Chrome extension with manifest V3, background workers, and content scripts
---

1. **Initialize extension project**

    Create directory structure for Chrome extension.

    ```bash
    mkdir my-chrome-extension
    cd my-chrome-extension
    mkdir -p src/{background,content,popup,icons}
    ```

    **Required files:**

    ```
    my-chrome-extension/
    ├── manifest.json          # Extension configuration
    ├── src/
    │   ├── background/
    │   │   └── service-worker.js
    │   ├── content/
    │   │   ├── content.js
    │   │   └── content.css
    │   ├── popup/
    │   │   ├── popup.html
    │   │   ├── popup.js
    │   │   └── popup.css
    │   └── icons/
    │       ├── icon16.png
    │       ├── icon48.png
    │       └── icon128.png
    └── README.md
    ```

2. **Create manifest.json**

    Configure extension with Manifest V3.

    Create `manifest.json`:

    ```json
    {
      "manifest_version": 3,
      "name": "My Chrome Extension",
      "version": "1.0.0",
      "description": "A useful Chrome extension",
      "permissions": [
        "storage",
        "activeTab"
      ],
      "host_permissions": [
        "https://*.example.com/*"
      ],
      "background": {
        "service_worker": "src/background/service-worker.js"
      },
      "action": {
        "default_popup": "src/popup/popup.html",
        "default_icon": {
          "16": "src/icons/icon16.png",
          "48": "src/icons/icon48.png",
          "128": "src/icons/icon128.png"
        }
      },
      "content_scripts": [
        {
          "matches": ["https://*/*"],
          "js": ["src/content/content.js"],
          "css": ["src/content/content.css"]
        }
      ],
      "icons": {
        "16": "src/icons/icon16.png",
        "48": "src/icons/icon48.png",
        "128": "src/icons/icon128.png"
      }
    }
    ```

    **Common permissions:**
    - `storage`: chrome.storage API
    - `activeTab`: Access current tab
    - `tabs`: Tab manipulation
    - `cookies`: Cookie access
    - `notifications`: Show notifications
    - `contextMenus`: Right-click menus

3. **Implement background service worker**

    Create background script for extension logic.

    Create `src/background/service-worker.js`:

    ```javascript
    // Listen for extension installation
    chrome.runtime.onInstalled.addListener(() => {
      console.log('Extension installed');

      // Initialize storage
      chrome.storage.local.set({ count: 0 });

      // Create context menu
      chrome.contextMenus.create({
        id: 'myAction',
        title: 'My Action',
        contexts: ['selection'],
      });
    });

    // Listen for messages from content scripts or popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === ' increment') {
        chrome.storage.local.get(['count'], (result) => {
          const newCount = (result.count || 0) + 1;
          chrome.storage.local.set({ count: newCount });
          sendResponse({ count: newCount });
        });
        return true; // Required for async sendResponse
      }
    });

    // Listen for tab updates
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.url) {
        console.log('Tab loaded:', tab.url);
      }
    });
    ```

4. **Create popup UI**

    Build popup HTML and JavaScript.

    Create `src/popup/popup.html`:

    ```html
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <link rel="stylesheet" href="popup.css">
    </head>
    <body>
      <div class="container">
        <h1>My Extension</h1>
        <p>Count: <span id="count">0</span></p>
        <button id="incrementBtn">Increment</button>
        <button id="resetBtn">Reset</button>
      </div>
      <script src="popup.js"></script>
    </body>
    </html>
    ```

    Create `src/popup/popup.js`:

    ```javascript
    // Load current count
    chrome.storage.local.get(['count'], (result) => {
      document.getElementById('count').textContent = result.count || 0;
    });

    // Increment button
    document.getElementById('incrementBtn').addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'increment' }, (response) => {
        document.getElementById('count').textContent = response.count;
      });
    });

    // Reset button
    document.getElementById('resetBtn').addEventListener('click', () => {
      chrome.storage.local.set({ count: 0 }, () => {
        document.getElementById('count').textContent = 0;
      });
    });

    // Get active tab info
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentTab = tabs[0];
      console.log('Current tab:', currentTab.url);
    });
    ```

    Create `src/popup/popup.css`:

    ```css
    body {
      width: 300px;
      padding: 0;
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .container {
      padding: 20px;
    }

    h1 {
      font-size: 18px;
      margin: 0 0 16px 0;
    }

    button {
      background: #4285f4;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      margin-right: 8px;
    }

    button:hover {
      background: #357ae8;
    }
    ```

5. **Implement content script**

    Inject scripts into web pages.

    Create `src/content/content.js`:

    ```javascript
    console.log('Content script loaded');

    // Modify page content
    function highlightText() {
      const paragraphs = document.querySelectorAll('p');
      paragraphs.forEach((p) => {
        p.style.backgroundColor = 'yellow';
      });
    }

    // Listen for messages from background or popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'highlight') {
        highlightText();
        sendResponse({ success: true });
      }
    });

    // Send message to background
    chrome.runtime.sendMessage({
      action: 'pageLoaded',
      url: window.location.href
    });
    ```

    Create `src/content/content.css`:

    ```css
    .my-extension-highlight {
      background-color: yellow;
      padding: 2px 4px;
      border-radius: 2px;
    }
    ```

6. **Create extension icons**

    Generate icons in required sizes.

    **Using ImageMagick:**

    ```bash
    # Install ImageMagick
    # Ubuntu: sudo apt-get install imagemagick
    # macOS: brew install imagemagick

    # Convert from source image
    convert source.png -resize 16x16 src/icons/icon16.png
    convert source.png -resize 48x48 src/icons/icon48.png
    convert source.png -resize 128x128 src/icons/icon128.png
    ```

    **Or use online tools:**
    - <https://www.favicon-generator.org/>
    - <https://realfavicongenerator.net/>

7. **Test extension locally**

    Load unpacked extension in Chrome.

    **Steps:**
    1. Open Chrome
    2. Navigate to `chrome://extensions/`
    3. Enable "Developer mode" (top right)
    4. Click "Load unpacked"
    5. Select your extension directory

    **Debug:**
    - Right-click extension icon → Inspect popup
    - Background: chrome://extensions/ → Service Worker → inspect
    - Content script: F12 in any web page

8. **Add TypeScript (optional)**

    Convert to TypeScript for better DX.

    ```bash
    npm init -y
    npm install --save-dev typescript @types/chrome webpack webpack-cli ts-loader
    ```

    Create `tsconfig.json`:

    ```json
    {
      "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "lib": ["ES2020", "DOM"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "types": ["chrome"]
      },
      "include": ["src/**/*"]
    }
    ```

    Create `webpack.config.js`:

    ```javascript
    const path = require('path');

    module.exports = {
      mode: 'production',
      entry: {
        'background/service-worker': './src/background/service-worker.ts',
        'content/content': './src/content/content.ts',
        'popup/popup': './src/popup/popup.ts',
      },
      output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js',
      },
      resolve: {
        extensions: ['.ts', '.js'],
      },
      module: {
        rules: [
          {
            test: /\.ts$/,
            use: 'ts-loader',
            exclude: /node_modules/,
          },
        ],
      },
    };
    ```

    // turbo
    Build:

    ```bash
    npm run build
    ```

9. **Package extension**

    Create distributable ZIP file.

    ```bash
    # Exclude unnecessary files
    zip -r my-extension.zip . -x "*.git*" "*node_modules*" "*.DS_Store" "src/*"
    ```

    **Or using npm script:**

    ```json
    {
      "scripts": {
        "build": "webpack",
        "package": "zip -r extension.zip dist manifest.json icons README.md"
      }
    }
    ```

10. **Publish to Chrome Web Store**

    Submit extension to Chrome Web Store.

    **Prerequisites:**
    - Google account
    - One-time $5 developer registration fee

    **Steps:**
    1. Go to <https://chrome.google.com/webstore/devconsole>
    2. Click "New Item"
    3. Upload `extension.zip`
    4. Fill in store listing:
       - Name,description
       - Screenshots (1280x800 or 640x400)
       - Category
       - Privacy policy URL
    5. Submit for review

    **Review process:** 1-3 days typically

11. **Update extension**

    Push updates to existing extension.

    **Increment version in `manifest.json`:**

    ```json
    {
      "version": "1.1.0"
    }
    ```

    **Build and package:**

    ```bash
    npm run build
    npm run package
    ```

    **Upload to Web Store:**
    - Dashboard → Your extension → Package
    - Upload new ZIP
    - Submit

    **Auto-update:**
    Chrome automatically updates extensions for users.

    **Next Steps:**
    - Add analytics (Google Analytics for extensions)
    - Implement options page for settings
    - Add keyboard shortcuts
    - Publish README with usage instructions
    - Monitor user reviews and feedback
    - Setup CI/CD for automated builds
