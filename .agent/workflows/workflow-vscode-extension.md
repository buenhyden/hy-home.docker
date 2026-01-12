---
description: Develop and publish VS Code extensions with TypeScript
---

1. **Initialize extension project**

    Create new VS Code extension using Yeoman generator.

    Install Yeoman and VS Code extension generator:

    ```bash
    npm install -g yo generator-code
    ```

    Create new extension:

    ```bash
    yo code
    ```

    Select options:
    - Extension type: **New Extension (TypeScript)**
    - Extension name: **my-extension**
    - Identifier: **my-extension**
    - Description: **My VS Code Extension**
    - Initialize git: **Yes**
    - Package manager: **npm**

    Navigate to project:

    ```bash
    cd my-extension
    ```

2. **Configure extension manifest**

    Update `package.json` with extension metadata and contributions.

    Key fields:

    ```json
    {
      "name": "my-extension",
      "displayName": "My Extension",
      "description": "Description of my extension",
      "version": "0.0.1",
      "engines": {
        "vscode": "^1.85.0"
      },
      "categories": ["Other"],
      "activationEvents": [],
      "main": "./out/extension.js",
      "contributes": {
        "commands": [
          {
            "command": "my-extension.helloWorld",
            "title": "Hello World"
          }
        ]
      }
    }
    ```

3. **Implement extension logic**

    Edit `src/extension.ts` to implement extension functionality.

    ```typescript
    import * as vscode from 'vscode';

    export function activate(context: vscode.ExtensionContext) {
      console.log('Extension "my-extension" is now active');

      const disposable = vscode.commands.registerCommand(
        'my-extension.helloWorld',
        () => {
          vscode.window.showInformationMessage('Hello World from My Extension!');
        }
      );

      context.subscriptions.push(disposable);
    }

    export function deactivate() {}
    ```

4. **Add more commands**

    Extend with additional commands and functionality.

    Update `package.json`:

    ```json
    {
      "contributes": {
        "commands": [
          {
            "command": "my-extension.helloWorld",
            "title": "My Extension: Hello World"
          },
          {
            "command": "my-extension.showInfo",
            "title": "My Extension: Show Info"
          }
        ]
      }
    }
    ```

    Implement in `src/extension.ts`:

    ```typescript
    const showInfo = vscode.commands.registerCommand(
      'my-extension.showInfo',
      () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
          const document = editor.document;
          const selection = editor.selection;
          const text = document.getText(selection);
          
          vscode.window.showInformationMessage(`Selected: ${text}`);
        }
      }
    );

    context.subscriptions.push(showInfo);
    ```

// turbo
5. **Compile TypeScript**

    Build the extension.

    ```bash
    npm run compile
    ```

    Or watch mode for development:

    ```bash
    npm run watch
    ```

    Expected: Compiles successfully to `out/extension.js`.

6. **Debug extension**

    Test the extension in Extension Development Host.

    **In VS Code:**
    - Press `F5` (or Run > Start Debugging)
    - A new VS Code window opens (Extension Development Host)
    - Press `Ctrl+Shift+P` (Command Palette)
    - Type "My Extension: Hello World"
    - Execute the command

    Expected: Information message appears.

    **Debug tips:**
    - Set breakpoints in `src/extension.ts`
    - Use `console.log()` for debugging
    - Check Debug Console for output

7. **Add configuration options**

    Allow users to configure extension behavior.

    Update `package.json`:

    ```json
    {
      "contributes": {
        "configuration": {
          "title": "My Extension",
          "properties": {
            "myExtension.enableFeature": {
              "type": "boolean",
              "default": true,
              "description": "Enable special feature"
            },
            "myExtension.maxItems": {
              "type": "number",
              "default": 10,
              "description": "Maximum number of items"
            }
          }
        }
      }
    }
    ```

    Read configuration in code:

    ```typescript
    const config = vscode.workspace.getConfiguration('myExtension');
    const maxItems = config.get<number>('maxItems', 10);
    ```

8. **Add keyboard shortcuts**

    Define keybindings for commands.

    Update `package.json`:

    ```json
    {
      "contributes": {
        "keybindings": [
          {
            "command": "my-extension.helloWorld",
            "key": "ctrl+shift+h",
            "mac": "cmd+shift+h",
            "when": "editorTextFocus"
          }
        ]
      }
    }
    ```

9. **Write tests**

    Create unit tests for extension functionality.

    Create `src/test/suite/extension.test.ts`:

    ```typescript
    import * as assert from 'assert';
    import * as vscode from 'vscode';

    suite('Extension Test Suite', () => {
      vscode.window.showInformationMessage('Start all tests.');

      test('Sample test', () => {
        assert.strictEqual(-1, [1, 2, 3].indexOf(5));
        assert.strictEqual(-1, [1, 2, 3].indexOf(0));
      });

      test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('publisher.my-extension'));
      });
    });
    ```

    // turbo
    Run tests:

    ```bash
    npm test
    ```

10. **Package extension**

    Create `.vsix` package file.

    Install vsce:

    ```bash
    npm install -g @vscode/vsce
    ```

    Package extension:

    ```bash
    vsce package
    ```

    This creates `my-extension-0.0.1.vsix`.

    **Verify package:**
    - Check file size (should be reasonable, < 10MB typically)
    - Install locally: `code --install-extension my-extension-0.0.1.vsix`
    - Test all features

11. **Prepare for publishing**

    Setup publisher and update metadata.

    **Create publisher:**
    - Go to <https://marketplace.visualstudio.com/manage>
    - Create publisher ID

    **Update `package.json`:**

    ```json
    {
      "publisher": "your-publisher-id",
      "repository": {
        "type": "git",
        "url": "https://github.com/username/my-extension.git"
      },
      "icon": "images/icon.png",
      "license": "MIT"
    }
    ```

    **Add README.md:**

    ```markdown
    # My Extension

    Description of your extension.

    ## Features

    - Feature 1
    - Feature 2

    ## Usage

    Press `Ctrl+Shift+H` to activate.

    ## Requirements

    VS Code ^1.85.0
    ```

    **Add CHANGELOG.md:**

    ```markdown
    # Change Log

    ## [0.0.1]
    - Initial release
    ```

12. **Publish to marketplace**

    Publish extension to VS Code Marketplace.

    **Create Personal Access Token (PAT):**
    - Go to <https://dev.azure.com>
    - User Settings > Personal Access Tokens
    - Create token with **Marketplace (Manage)** scope

    **Login:**

    ```bash
    vsce login your-publisher-id
    ```

    Enter PAT when prompted.

    **Publish:**

    ```bash
    vsce publish
    ```

    Extension will be available at:
    `https://marketplace.visualstudio.com/items?itemName=your-publisher-id.my-extension`

    **Update version:**

    ```bash
    vsce publish patch  # 0.0.1 -> 0.0.2
    vsce publish minor  # 0.0.1 -> 0.1.0
    vsce publish major  # 0.0.1 -> 1.0.0
    ```

    **Next Steps:**
    - Add extension icon (128x128 PNG)
    - Write comprehensive documentation
    - Add screenshots/GIFs to README
    - Setup CI/CD for automated publishing
    - Monitor extension analytics
    - Respond to user feedback and issues
