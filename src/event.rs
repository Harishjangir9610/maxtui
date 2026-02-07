//! Event handling module for keyboard, mouse, and terminal resize events
//! 
//! Uses crossterm for cross-platform event reading

use std::time::Duration;
use crossterm::event::{self, KeyCode, KeyModifiers as CrosstermModifiers};

#[derive(Debug, Clone, Copy)]
pub enum KeyCode {
    Char(char),
    F(u8),
    Enter,
    Escape,
    Backspace,
    Tab,
    Delete,
    Insert,
    Home,
    End,
    PageUp,
    PageDown,
    Up,
    Down,
    Left,
    Right,
    Media(MediaKey),
}

#[derive(Debug, Clone, Copy)]
pub enum MediaKey {
    Play,
    Pause,
    PlayPause,
    Mute,
    VolumeDown,
    VolumeUp,
    Next,
    Previous,
}

#[derive(Debug, Clone, Copy)]
pub struct KeyModifiers {
    pub shift: bool,
    pub ctrl: bool,
    pub alt: bool,
}

#[derive(Debug, Clone)]
pub struct KeyEvent {
    pub code: KeyCode,
    pub modifiers: KeyModifiers,
    pub kind: KeyEventKind,
}

#[derive(Debug, Clone, Copy)]
pub enum KeyEventKind {
    Press,
    Release,
    Repeat,
}

#[derive(Debug, Clone)]
pub struct MouseEvent {
    pub kind: MouseEventKind,
    pub column: u16,
    pub row: u16,
    pub modifiers: KeyModifiers,
}

#[derive(Debug, Clone)]
pub enum MouseEventKind {
    Down(MouseButton),
    Up(MouseButton),
    Drag(MouseButton),
    Moved,
    ScrollDown,
    ScrollUp,
    ScrollLeft,
    ScrollRight,
}

#[derive(Debug, Clone, Copy)]
pub enum MouseButton {
    Left,
    Right,
    Middle,
}

#[derive(Debug, Clone)]
pub enum Event {
    Key(KeyEvent),
    Mouse(MouseEvent),
    Resize(u16, u16),
    Focus(bool),
    Paste(String),
}

impl Event {
    pub fn poll(timeout: Duration) -> std::io::Result<Option<Self>> {
        if event::poll(timeout)? {
            Ok(Some(Self::read()?))
        } else {
            Ok(None)
        }
    }

    pub fn read() -> std::io::Result<Self> {
        match event::read()? {
            event::Event::Key(k) => Ok(Event::Key(convert_key_event(k))),
            event::Event::Mouse(m) => Ok(Event::Mouse(convert_mouse_event(m))),
            event::Event::Resize(w, h) => Ok(Event::Resize(w, h)),
            event::Event::FocusGained => Ok(Event::Focus(true)),
            event::Event::FocusLost => Ok(Event::Focus(false)),
            #[cfg(feature = "bracketed-paste")]
            event::Event::Paste(s) => Ok(Event::Paste(s)),
            _ => Event::read(),
        }
    }
}

fn convert_key_event(k: event::KeyEvent) -> KeyEvent {
    let modifiers = KeyModifiers {
        shift: k.modifiers.contains(CrosstermModifiers::SHIFT),
        ctrl: k.modifiers.contains(CrosstermModifiers::CONTROL),
        alt: k.modifiers.contains(CrosstermModifiers::ALT),
    };

    let code = match k.code {
        KeyCode::Char(c) => KeyCode::Char(c),
        KeyCode::F(f) => KeyCode::F(f),
        KeyCode::Enter => KeyCode::Enter,
        KeyCode::Esc => KeyCode::Escape,
        KeyCode::Backspace => KeyCode::Backspace,
        KeyCode::Tab => KeyCode::Tab,
        KeyCode::Delete => KeyCode::Delete,
        KeyCode::Insert => KeyCode::Insert,
        KeyCode::Home => KeyCode::Home,
        KeyCode::End => KeyCode::End,
        KeyCode::PageUp => KeyCode::PageUp,
        KeyCode::PageDown => KeyCode::PageDown,
        KeyCode::Up => KeyCode::Up,
        KeyCode::Down => KeyCode::Down,
        KeyCode::Left => KeyCode::Left,
        KeyCode::Right => KeyCode::Right,
        _ => KeyCode::Char(' '),
    };

    KeyEvent {
        code,
        modifiers,
        kind: KeyEventKind::Press,
    }
}

fn convert_mouse_event(m: event::MouseEvent) -> MouseEvent {
    let modifiers = KeyModifiers {
        shift: m.modifiers.contains(CrosstermModifiers::SHIFT),
        ctrl: m.modifiers.contains(CrosstermModifiers::CONTROL),
        alt: m.modifiers.contains(CrosstermModifiers::ALT),
    };

    let kind = match m.kind {
        event::MouseEventKind::Down(btn) => MouseEventKind::Down(convert_mouse_button(btn)),
        event::MouseEventKind::Up(btn) => MouseEventKind::Up(convert_mouse_button(btn)),
        event::MouseEventKind::Drag(btn) => MouseEventKind::Drag(convert_mouse_button(btn)),
        event::MouseEventKind::Moved => MouseEventKind::Moved,
        event::MouseEventKind::ScrollDown => MouseEventKind::ScrollDown,
        event::MouseEventKind::ScrollUp => MouseEventKind::ScrollUp,
        event::MouseEventKind::ScrollLeft => MouseEventKind::ScrollLeft,
        event::MouseEventKind::ScrollRight => MouseEventKind::ScrollRight,
    };

    MouseEvent {
        kind,
        column: m.column,
        row: m.row,
        modifiers,
    }
}

fn convert_mouse_button(btn: event::MouseButton) -> MouseButton {
    match btn {
        event::MouseButton::Left => MouseButton::Left,
        event::MouseButton::Right => MouseButton::Right,
        event::MouseButton::Middle => MouseButton::Middle,
    }
}
