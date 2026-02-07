"""
MAXTUI - High-Performance Terminal UI Framework
Python API Layer
"""

from . import maxtui as _maxtui

class App(_maxtui.PyApp):
    """Main application class"""
    def __init__(self):
        super().__init__()
    
    def set_fps(self, fps: int) -> 'App':
        super().set_fps(fps)
        return self
    
    def set_theme(self, name: str) -> 'App':
        super().set_theme(name)
        return self
    
    def run(self) -> None:
        super().run()

class Paragraph(_maxtui.PyParagraph):
    """Text widget"""
    def __init__(self, text: str):
        super().__init__(text)

class Button(_maxtui.PyButton):
    """Button widget"""
    def __init__(self, label: str):
        super().__init__(label)

class Input(_maxtui.PyInput):
    """Input widget"""
    def __init__(self, placeholder: str):
        super().__init__(placeholder)

class Gauge(_maxtui.PyGauge):
    """Progress bar"""
    def __init__(self, label: str, percent: float):
        super().__init__(label, percent)

class List(_maxtui.PyList):
    """List widget"""
    def __init__(self, title: str):
        super().__init__(title)

class Table(_maxtui.PyTable):
    """Table widget"""
    def __init__(self, title: str):
        super().__init__(title)

class Chart(_maxtui.PyChart):
    """Chart widget"""
    def __init__(self, title: str):
        super().__init__(title)

class Divider(_maxtui.PyDivider):
    """Divider widget"""
    def __init__(self):
        super().__init__()

class Modal(_maxtui.PyModal):
    """Modal widget"""
    def __init__(self, title: str, content: str):
        super().__init__(title, content)

class Spinner(_maxtui.PySpinner):
    """Loading spinner"""
    def __init__(self, label: str):
        super().__init__(label)

class Layout(_maxtui.PyLayout):
    """Layout container"""
    @staticmethod
    def vertical() -> 'Layout':
        return _maxtui.PyLayout.vertical()
    
    @staticmethod
    def horizontal() -> 'Layout':
        return _maxtui.PyLayout.horizontal()

class Constraint:
    """Layout constraints"""
    @staticmethod
    def fixed(size: int):
        return _maxtui.PyConstraint.fixed(size)
    
    @staticmethod
    def percentage(p: int):
        return _maxtui.PyConstraint.percentage(p)
    
    @staticmethod
    def fill():
        return _maxtui.PyConstraint.fill()

class Color:
    """Color definitions"""
    @staticmethod
    def red():
        return _maxtui.PyColor.red()
    
    @staticmethod
    def green():
        return _maxtui.PyColor.green()
    
    @staticmethod
    def blue():
        return _maxtui.PyColor.blue()
    
    @staticmethod
    def white():
        return _maxtui.PyColor.white()
    
    @staticmethod
    def black():
        return _maxtui.PyColor.black()
    
    @staticmethod
    def rgb(r: int, g: int, b: int):
        return _maxtui.PyColor.rgb(r, g, b)

class Style(_maxtui.PyStyle):
    """Text styling"""
    def __init__(self):
        super().__init__()

class Theme:
    """Theme definitions"""
    @staticmethod
    def dark():
        return _maxtui.PyTheme.dark()
    
    @staticmethod
    def light():
        return _maxtui.PyTheme.light()
    
    @staticmethod
    def monokai():
        return _maxtui.PyTheme.monokai()

class TextAnimation:
    """Text animations"""
    @staticmethod
    def typewriter(interval_ms: int):
        return _maxtui.PyTextAnimation.typewriter(interval_ms)
    
    @staticmethod
    def scroll_left(speed: int):
        return _maxtui.PyTextAnimation.scroll_left(speed)

class FrameAnimation(_maxtui.PyFrameAnimation):
    """Frame animations"""
    def __init__(self, frames: list, interval_ms: int):
        super().__init__(frames, interval_ms)

class Effect:
    """Visual effects"""
    @staticmethod
    def fade(duration_ms: int):
        return _maxtui.PyEffect.fade(duration_ms)
    
    @staticmethod
    def slide(duration_ms: int):
        return _maxtui.PyEffect.slide(duration_ms)
    
    @staticmethod
    def blink(interval_ms: int):
        return _maxtui.PyEffect.blink(interval_ms)
    
    @staticmethod
    def pulse(duration_ms: int):
        return _maxtui.PyEffect.pulse(duration_ms)

class EffectManager(_maxtui.PyEffectManager):
    """Effect manager"""
    def __init__(self):
        super().__init__()

__version__ = "0.1.0"
__all__ = [
    "App", "Paragraph", "Button", "Input", "Gauge", "List", "Table", "Chart",
    "Divider", "Modal", "Spinner", "Layout", "Constraint", "Color", "Style",
    "Theme", "TextAnimation", "FrameAnimation", "Effect", "EffectManager"
]
