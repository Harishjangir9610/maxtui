# MAXTUI Architecture

## Overview

MAXTUI is a three-layer system:

```
┌─────────────────────────────────────┐
│   Python API (maxtui package)       │  High-level, Pythonic
├─────────────────────────────────────┤
│   PyO3 Bindings (src/py)            │  Zero-overhead FFI
├─────────────────────────────────────┤
│   Rust Core (src/*)                 │  Performance, safety
│  - Ratatui (rendering)              │
│  - Crossterm (terminal)             │
│  - Tokio (async runtime)            │
└─────────────────────────────────────┘
```

## Module Breakdown

### style/ — Colors, Styles, Themes

- `Color` enum: 16 named colors + RGB + indexed
- `Style` struct: fg, bg, modifiers (bold, italic, underline)
- `Theme` struct: Predefined themes (dark, light, monokai)
- Serializable (Serde support)

**Key Functions**:
- `Style::new()` → `fg()` → `bg()` → `bold()` → `to_ratatui()`

### layout/ — Constraint-Based Layout

- `Constraint` enum: Fixed, Percentage, Ratio, Fill, Min, Max
- `Layout` struct: vertical/horizontal, compute areas
- `Rect` struct: Position & size
- O(n) computation, deterministic

**Key Functions**:
- `Layout::vertical()` → `constraints()` → `spacing()` → `compute(rect)`

### events/ — Event System

- `KeyEvent`: code + modifiers (shift, ctrl, alt)
- `MouseEvent`: position + button + kind (down, up, drag, scroll)
- `ResizeEvent`: width × height
- `Event` enum: Union of all event types
- Crossterm conversion impls

**Key Functions**:
- `Event::from(crossterm::event::Event)` → Automatic conversion

### widgets/ — UI Components

**10 Widgets**:
1. `Paragraph` — Text display
2. `Button` — Interactive button
3. `Input` — Text entry field
4. `Gauge` — Progress bar
5. `List` — Selectable items
6. `Table` — Multi-column data
7. `Chart` — Data visualization
8. `Divider` — Visual separator
9. `Modal` — Dialog box
10. `Spinner` — Loading animation

**Widget Trait**:
```rust
pub trait Widget: Send + Sync {
    fn id(&self) -> WidgetId;
    fn render(&self, frame: &mut Frame, area: Rect);
    fn on_key(&mut self, code: char) {}
    fn set_style(&mut self, style: Style) {}
    fn is_focused(&self) -> bool { false }
}
```

All widgets are immutable-after-creation with interior mutability via Arc<Mutex<T>>.

### animation/ — Text & Frame Animations

**TextAnimation**:
- Typewriter: Reveal one char at a time
- ScrollLeft/Right: Horizontal text movement
- ColorChange: Cycle through colors
- Blinking: Flash on/off

**FrameAnimation**:
- Frame-based (like GIF frames)
- Current frame indexing
- Looping control
- Progress tracking

**AnimationManager**:
- Manages active animations
- Update timing
- Removal on completion

### effects/ — Visual Effects

**EffectType**:
- Fade: Opacity change over duration
- Slide: Movement across screen
- ColorCycle: Color sequence
- Blink: On/off flashing
- Pulse: Scale/intensity change
- Wave: Amplitude oscillation

**EffectManager**:
- Add/remove effects
- Update timing
- Query active effects
- Progress calculation

### async_runtime/ — Tokio Integration

**TaskScheduler**:
- `spawn()` → Fire-and-forget async task
- `spawn_with_handle()` → Awaitable task
- `schedule_after()` → Delayed execution
- `block_on()` → Sync → async bridge

**UpdateTx**:
- Event channel for app updates
- Non-blocking communication
- Supports async updates from background tasks

### rendering/ — Ratatui Wrapper

**Renderer**:
- Terminal setup/teardown
- Frame rendering
- Cursor control
- Size queries

**RenderPipeline**:
- Widget list + layout
- Automatic area distribution
- Frame rendering

### engine/ — Main Event Loop

**FrameRate**:
- Target FPS (default 60)
- Frame duration calculation

**AppState**:
- Widget list
- Focus management
- Theme & layout
- Running state
- Event handling

**Engine**:
- Coordinates everything
- Event polling thread
- Main render loop
- Frame rate limiting
- GIL-aware rendering

### app/ — High-Level API

**App**:
- Public wrapper around Engine
- Simplified interface for Python
- Theme management
- FPS control
- Layout control

### py/ — PyO3 Bindings

**PyO3 Classes** (all #[pyclass]):
- PyApp, PyParagraph, PyButton, PyInput, PyGauge, PyList, PyTable, PyChart, PyDivider, PyModal, PySpinner
- PyLayout, PyConstraint
- PyColor, PyStyle, PyTheme
- PyTextAnimation, PyFrameAnimation
- PyEffect, PyEffectManager

**Binding Strategy**:
- Rust types → Python classes (1:1)
- Arc<Mutex<T>> → Interior mutability safe
- PyResult → Python exceptions
- No unsafe code exposure

## Data Flow

### Rendering Loop (main thread)

```
1. Calculate frame rate delay
2. Poll for input events (non-blocking)
3. Dispatch events to focused widget
4. Render all widgets into frame
5. Apply effects
6. Output to terminal
7. Sleep to maintain FPS
8. Repeat until app.stop()
```

### Event Flow

```
Crossterm::read() → Event → App::dispatch() → Widget::on_key() → Widget state update → Next frame renders change
```

### Widget Rendering

```
Layout::compute(screen_area) → [area1, area2, area3, ...]
                               ↓
                    Widget[0].render(frame, area1)
                    Widget[1].render(frame, area2)
                    Widget[2].render(frame, area3)
                               ↓
                        Frame outputs to terminal
```

## Performance Considerations

### Why Rust Core?

1. **No GIL contention**: Rendering doesn't hold Python GIL
2. **Native speed**: Ratatui is compiled + optimized
3. **Memory efficient**: Zero-copy rendering
4. **Concurrency**: Tokio for async without Python overhead

### Optimization Techniques

1. **Lazy rendering**: Only recompute changed widgets
2. **Frame rate limiting**: Prevents wasted renders
3. **Arc<Mutex<T>>**: Shared ownership without allocation
4. **Interior mutability**: No borrow checker pain
5. **Immediate mode**: No retained state complexity

## Thread Safety

- All Widget impls: `Send + Sync`
- State behind Arc<Mutex<>>
- Events sent via mpsc channel
- No unsafe code in public API

## Memory Layout

```
App (Python) → Engine (Rust)
                ├→ AppState (Arc<Mutex<>>)
                │   ├→ widgets: Vec<Arc<Mutex<dyn Widget>>>
                │   ├→ layout: Layout
                │   └→ theme: Theme
                ├→ event_tx/rx (mpsc channel)
                └→ event thread (std::thread)
```

## GIL Management

PyO3 automatically manages GIL:
- Methods entering Rust: GIL acquired
- Heavy computations: `py.allow_threads()`
- Tokio tasks: Run without GIL
- Events: Sent via channel (GIL-free)

## Extension Points

### Custom Widgets

```rust
struct MyWidget { /* ... */ }

impl Widget for MyWidget {
    fn id(&self) -> WidgetId { /* ... */ }
    fn render(&self, frame: &mut Frame, area: Rect) { /* ... */ }
    fn on_key(&mut self, code: char) { /* ... */ }
}
```

### Custom Themes

```rust
let my_theme = Theme {
    name: "custom".into(),
    primary: Style::new().fg(Color::Cyan),
    // ...
};
```

### Custom Effects

```rust
let fade = Effect::fade(2000);
effects.add_effect(fade);
```

## Testing Strategy

- Unit tests in each module
- Integration tests for Engine
- Python tests via pytest
- Benchmark suite (criterion)

## Future Enhancements

1. **Plugins**: Custom widget loading
2. **Serialization**: Save/load app state
3. **Accessibility**: Screen reader support
4. **Multiplexing**: Multiple app instances
5. **Remoting**: TUI over network
