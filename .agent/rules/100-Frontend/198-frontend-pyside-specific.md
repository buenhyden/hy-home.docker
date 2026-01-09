---
trigger: always_on
glob: "**/*.py"
description: "PySide (Qt for Python): GUI Development Standards."
---
# PySide Standards

## 1. Threading

- **Main Thread**: NEVER block the main thread (GUI thread). Long operations freeze the UI.
- **Worker Threads**: Use `QThread` or `QRunnable` with `QThreadPool` for background tasks.
- **Signals/Slots**: Use Signals/Slots to communicate results back to the GUI thread safely.

### Example: Worker

**Good**

```python
class Worker(QObject):
    finished = Signal()
    def run(self):
        # Heavy work
        self.finished.emit()

thread = QThread()
worker = Worker()
worker.moveToThread(thread)
thread.started.connect(worker.run)
thread.start()
```

## 2. Layouts

- **Responsive**: Always use Layout Managers (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`) instead of fixed positioning (`setGeometry`). This handles resizing and DPI scaling automatically.

## 3. Resource Management

- **Parents**: Pass a parent to `QWidget` constructors where possible (`super().__init__(parent)`). This ensures automatic memory management (children are deleted when parents are).
- **Designer**: Use `.ui` files (Qt Designer) for complex layouts to separate UI definition from logic. Load them with `QUiLoader` or compile with `pyside6-uic`.
