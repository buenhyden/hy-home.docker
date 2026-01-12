---
description: Create Flutter project with Dart, Material Design, and mobile best practices
---

1. **Initialize Flutter project**

    Create a new Flutter project with your organization identifier.

    ```bash
    flutter create --org com.example --platforms ios,android,web my_flutter_app
    cd my_flutter_app
    ```

    Replace `com.example` with your actual organization identifier.

2. **Configure analysis options**

    Create `analysis_options.yaml` with Flutter lints based on `500-Mobile/530-mobile-flutter-specific.md`.

    ```yaml
    include: package:flutter_lints/flutter.yaml

    linter:
      rules:
        prefer_single_quotes: true
        avoid_print: true
        prefer_const_constructors: true
        prefer_const_literals_to_create_immutables: true
    ```

3. **Add essential dependencies**

    Add recommended packages for routing, state management, and JSON serialization.

    // turbo

    ```bash
    flutter pub add go_router
    flutter pub add json_annotation
    flutter pub add dev:build_runner
    flutter pub add dev:json_serializable
    flutter pub add dev:flutter_lints
    ```

4. **Create project structure**

    Set up feature-based project structure for scalable architecture.

    Create directories:

    ```bash
    mkdir -p lib/{presentation,domain,data,core}
    mkdir -p lib/presentation/{screens,widgets}
    mkdir -p lib/domain/models
    mkdir -p lib/data/{repositories,api}
    mkdir -p lib/core/{utils,extensions,constants}
    ```

5. **Setup go_router**

    Create routing configuration in `lib/core/router.dart`.

    Example router setup:

    ```dart
    import 'package:go_router/go_router.dart';
    import 'package:flutter/material.dart';

    final GoRouter router = GoRouter(
      routes: <RouteBase>[
        GoRoute(
          path: '/',
          builder: (context, state) => const HomeScreen(),
        ),
      ],
    );
    ```

    Update `lib/main.dart` to use `MaterialApp.router`:

    ```dart
    import 'package:flutter/material.dart';
    import 'core/router.dart';

    void main() {
      runApp(const MyApp());
    }

    class MyApp extends StatelessWidget {
      const MyApp({super.key});

      @override
      Widget build(BuildContext context) {
        return MaterialApp.router(
          title: 'My Flutter App',
          routerConfig: router,
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.deepPurple,
              brightness: Brightness.light,
            ),
            useMaterial3: true,
          ),
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.deepPurple,
              brightness: Brightness.dark,
            ),
            useMaterial3: true,
          ),
        );
      }
    }
    ```

6. **Create initial screens**

    Create `lib/presentation/screens/home_screen.dart`:

    ```dart
    import 'package:flutter/material.dart';

    class HomeScreen extends StatelessWidget {
      const HomeScreen({super.key});

      @override
      Widget build(BuildContext context) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Home'),
          ),
          body: const Center(
            child: Text('Welcome to Flutter!'),
          ),
        );
      }
    }
    ```

7. **Format and analyze code**

    Run Flutter formatter and analyzer to ensure code quality.

    // turbo

    ```bash
    dart format .
    flutter analyze
    ```

    Expected: No analysis issues.

8. **Verify setup**

    Run the app on your preferred platform.

    For iOS simulator:

    // turbo

    ```bash
    flutter run -d ios
    ```

    For Android emulator:

    // turbo

    ```bash
    flutter run -d android
    ```

    For web:

    // turbo

    ```bash
    flutter run -d chrome
    ```

    Expected: App loads with Material Design UI showing "Welcome to Flutter!"

9. **Setup testing**

    Create test file structure:

    ```bash
    mkdir -p test/{unit,widget,integration}
    mkdir -p test/unit/{domain,data}
    mkdir -p test/widget/presentation
    ```

    Create a sample widget test in `test/widget/presentation/home_screen_test.dart`:

    ```dart
    import 'package:flutter/material.dart';
    import 'package:flutter_test/flutter_test.dart';
    import 'package:my_flutter_app/presentation/screens/home_screen.dart';

    void main() {
      testWidgets('HomeScreen displays welcome message', (tester) async {
        await tester.pumpWidget(
          const MaterialApp(home: HomeScreen()),
        );

        expect(find.text('Welcome to Flutter!'), findsOneWidget);
      });
    }
    ```

10. **Run tests**

    Execute tests to verify setup.

    // turbo

    ```bash
    flutter test
    ```

    Expected: All tests pass.

11. **Initialize Git**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize Flutter project with Material Design"
    ```

    **Next Steps:**

    - Review `agent/rules/500-Mobile/530-mobile-flutter-specific.md` for Flutter best practices
    - Review Dart language features (null safety, pattern matching, records)
    - Setup state management (ValueNotifier, ChangeNotifier, or Provider if needed)
    - Configure build_runner for code generation if using json_serializable
    - Add integration tests with `integration_test` package
