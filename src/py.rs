use pyo3::prelude::*;
use std::sync::{Arc, Mutex};
use parking_lot::RwLock;
use ratatui::style::{Color as RColor, Modifier, Style as RStyle};
use ratatui::layout::{Layout as RLayout, Constraint as RConstraint, Direction};
use ratatui::widgets::{Block, Borders, Paragraph as RParagraph};
use crossterm::terminal::{enable_raw_mode, disable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen};
use crossterm::execute;
use std::io;

// ============================================================================
// APP
// ============================================================================

#[pyclass]
pub struct App {
    running: Arc<RwLock<bool>>,
    fps: Arc<RwLock<u32>>,
    theme: Arc<RwLock<String>>,
}

#[pymethods]
impl App {
    #[new]
    fn new() -> Self {
        Self {
            running: Arc::new(RwLock::new(true)),
            fps: Arc::new(RwLock::new(30)),
            theme: Arc::new(RwLock::new("dark".to_string())),
        }
    }

    fn set_fps(&self, fps: u32) {
        *self.fps.write() = fps;
    }

    fn set_theme(&self, name: &str) {
        *self.theme.write() = name.to_string();
    }

    fn stop(&self) {
        *self.running.write() = false;
    }

    fn run(&self) -> PyResult<()> {
        let _ = enable_raw_mode();
        let mut stdout = io::stdout();
        let _ = execute!(stdout, EnterAlternateScreen);
        
        // Simple TUI loop
        println!("MaxTUI App Running!");
        println!("Press Ctrl+C to exit");
        std::thread::sleep(std::time::Duration::from_secs(3));
        
        let _ = execute!(stdout, LeaveAlternateScreen);
        let _ = disable_raw_mode();
        Ok(())
    }

    fn __repr__(&self) -> String {
        "App(fps={}, theme={})".to_string()
    }
}

// ============================================================================
// WIDGETS
// ============================================================================

#[pyclass]
pub struct Button {
    label: Arc<Mutex<String>>,
    focused: Arc<RwLock<bool>>,
}

#[pymethods]
impl Button {
    #[new]
    fn new(label: String) -> Self {
        Self {
            label: Arc::new(Mutex::new(label)),
            focused: Arc::new(RwLock::new(false)),
        }
    }

    fn set_focused(&self, focused: bool) {
        *self.focused.write() = focused;
    }

    fn __repr__(&self) -> String {
        format!("Button('{}')", self.label.lock().unwrap())
    }
}

#[pyclass]
pub struct Input {
    value: Arc<Mutex<String>>,
    placeholder: Arc<Mutex<String>>,
}

#[pymethods]
impl Input {
    #[new]
    fn new(placeholder: String) -> Self {
        Self {
            value: Arc::new(Mutex::new(String::new())),
            placeholder: Arc::new(Mutex::new(placeholder)),
        }
    }

    fn get_value(&self) -> String {
        self.value.lock().unwrap().clone()
    }

    fn set_value(&self, value: String) {
        *self.value.lock().unwrap() = value;
    }

    fn __repr__(&self) -> String {
        format!("Input('{}')", self.get_value())
    }
}

#[pyclass]
pub struct Paragraph {
    text: Arc<Mutex<String>>,
}

#[pymethods]
impl Paragraph {
    #[new]
    fn new(text: String) -> Self {
        Self {
            text: Arc::new(Mutex::new(text)),
        }
    }

    fn set_text(&self, text: String) {
        *self.text.lock().unwrap() = text;
    }

    fn __repr__(&self) -> String {
        "Paragraph".to_string()
    }
}

#[pyclass]
pub struct Gauge {
    label: Arc<Mutex<String>>,
    value: Arc<RwLock<f32>>,
}

#[pymethods]
impl Gauge {
    #[new]
    fn new(label: String, percent: f32) -> Self {
        Self {
            label: Arc::new(Mutex::new(label)),
            value: Arc::new(RwLock::new(percent)),
        }
    }

    fn set_percent(&self, percent: f32) {
        *self.value.write() = percent.max(0.0).min(100.0);
    }

    fn __repr__(&self) -> String {
        "Gauge".to_string()
    }
}

#[pyclass]
pub struct List {
    title: Arc<Mutex<String>>,
    items: Arc<Mutex<Vec<String>>>,
}

#[pymethods]
impl List {
    #[new]
    fn new(title: String) -> Self {
        Self {
            title: Arc::new(Mutex::new(title)),
            items: Arc::new(Mutex::new(Vec::new())),
        }
    }

    fn add_item(&self, item: String) {
        self.items.lock().unwrap().push(item);
    }

    fn __repr__(&self) -> String {
        "List".to_string()
    }
}

#[pyclass]
pub struct Table {
    title: Arc<Mutex<String>>,
}

#[pymethods]
impl Table {
    #[new]
    fn new(title: String) -> Self {
        Self {
            title: Arc::new(Mutex::new(title)),
        }
    }

    fn add_row(&self, _row: Vec<String>) -> PyResult<()> {
        Ok(())
    }

    fn __repr__(&self) -> String {
        "Table".to_string()
    }
}

#[pyclass]
pub struct Chart {
    title: Arc<Mutex<String>>,
}

#[pymethods]
impl Chart {
    #[new]
    fn new(title: String) -> Self {
        Self {
            title: Arc::new(Mutex::new(title)),
        }
    }

    fn add_point(&self, _x: f64, _y: f64) -> PyResult<()> {
        Ok(())
    }

    fn __repr__(&self) -> String {
        "Chart".to_string()
    }
}

#[pyclass]
pub struct Modal {
    title: Arc<Mutex<String>>,
    content: Arc<Mutex<String>>,
}

#[pymethods]
impl Modal {
    #[new]
    fn new(title: String, content: String) -> Self {
        Self {
            title: Arc::new(Mutex::new(title)),
            content: Arc::new(Mutex::new(content)),
        }
    }

    fn __repr__(&self) -> String {
        "Modal".to_string()
    }
}

#[pyclass]
pub struct Spinner {
    label: Arc<Mutex<String>>,
}

#[pymethods]
impl Spinner {
    #[new]
    fn new(label: String) -> Self {
        Self {
            label: Arc::new(Mutex::new(label)),
        }
    }

    fn __repr__(&self) -> String {
        "Spinner".to_string()
    }
}

// ============================================================================
// STYLE
// ============================================================================

#[pyclass]
pub struct Color;

#[pymethods]
impl Color {
    #[staticmethod]
    fn red() -> &'static str { "red" }
    #[staticmethod]
    fn green() -> &'static str { "green" }
    #[staticmethod]
    fn blue() -> &'static str { "blue" }
    #[staticmethod]
    fn white() -> &'static str { "white" }
    #[staticmethod]
    fn black() -> &'static str { "black" }
    #[staticmethod]
    fn cyan() -> &'static str { "cyan" }
    #[staticmethod]
    fn magenta() -> &'static str { "magenta" }
    #[staticmethod]
    fn yellow() -> &'static str { "yellow" }
    #[staticmethod]
    fn gray() -> &'static str { "gray" }
    #[staticmethod]
    fn rgb(r: u8, g: u8, b: u8) -> String {
        format!("rgb({},{},{})", r, g, b)
    }
}

#[pyclass]
pub struct Style {
    _private: (),
}

#[pymethods]
impl Style {
    #[new]
    fn new() -> Self {
        Self { _private: () }
    }
    fn bold(&self) -> Self { Self { _private: () } }
    fn italic(&self) -> Self { Self { _private: () } }
    fn underline(&self) -> Self { Self { _private: () } }
}

#[pyclass]
pub struct Theme;

#[pymethods]
impl Theme {
    #[staticmethod]
    fn dark() -> &'static str { "dark" }
    #[staticmethod]
    fn light() -> &'static str { "light" }
    #[staticmethod]
    fn monokai() -> &'static str { "monokai" }
}

// ============================================================================
// LAYOUT
// ============================================================================

#[pyclass]
pub struct Layout {
    _private: (),
}

#[pymethods]
impl Layout {
    #[staticmethod]
    fn vertical() -> Self { Self { _private: () } }
    #[staticmethod]
    fn horizontal() -> Self { Self { _private: () } }
}

#[pyclass]
pub struct Constraint;

#[pymethods]
impl Constraint {
    #[staticmethod]
    fn fixed(size: u16) -> String { format!("fixed({})", size) }
    #[staticmethod]
    fn percentage(p: u16) -> String { format!("percentage({})", p) }
    #[staticmethod]
    fn fill() -> &'static str { "fill" }
}

// ============================================================================
// ANIMATION
// ============================================================================

#[pyclass]
pub struct TextAnimation {
    _private: (),
}

#[pymethods]
impl TextAnimation {
    #[staticmethod]
    fn typewriter(_interval_ms: u64) -> Self { Self { _private: () } }
    #[staticmethod]
    fn scroll_left(_speed: u32) -> Self { Self { _private: () } }
    fn get_progress(&self) -> f32 { 0.5 }
}

#[pyclass]
pub struct FrameAnimation {
    frames: Arc<Mutex<Vec<String>>>,
}

#[pymethods]
impl FrameAnimation {
    #[new]
    fn new(frames: Vec<String>, _interval_ms: u64) -> Self {
        Self {
            frames: Arc::new(Mutex::new(frames)),
        }
    }
    fn get_current_frame(&self) -> Option<String> {
        self.frames.lock().unwrap().first().cloned()
    }
}

// ============================================================================
// EFFECTS
// ============================================================================

#[pyclass]
pub struct Effect;

#[pymethods]
impl Effect {
    #[staticmethod]
    fn fade(duration_ms: u64) -> String { format!("fade({}ms)", duration_ms) }
    #[staticmethod]
    fn slide(duration_ms: u64) -> String { format!("slide({}ms)", duration_ms) }
    #[staticmethod]
    fn blink(interval_ms: u64) -> String { format!("blink({}ms)", interval_ms) }
    #[staticmethod]
    fn pulse(duration_ms: u64) -> String { format!("pulse({}ms)", duration_ms) }
}

#[pyclass]
pub struct EffectManager {
    _private: (),
}

#[pymethods]
impl EffectManager {
    #[new]
    fn new() -> Self { Self { _private: () } }
    fn add_effect(&self, _effect: String) -> PyResult<()> { Ok(()) }
}
