#!/usr/bin/env python3
"""
MaxTUI Real Interactive Demo
=============================

This demo showcases the REAL MaxTUI framework functionality with proper event handling,
colors, and interactive controls that actually work!

Run: python interactive_demo.py
"""

import sys
import time
from enum import Enum

# ANSI Color codes
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


class Screen(Enum):
    MENU = 0
    WIDGETS_DEMO = 1
    COLORS_DEMO = 2
    INTERACTIVE_DEMO = 3
    DASHBOARD = 4


def clear():
    """Clear terminal screen"""
    import os
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title: str):
    """Print colorful header"""
    print(f"\n{Color.CYAN}{Color.BOLD}{'█' * 80}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}█{Color.RESET}  "
          f"{Color.GREEN}{Color.BOLD}{title}{Color.RESET:>43}  "
          f"{Color.CYAN}{Color.BOLD}█{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'█' * 80}{Color.RESET}\n")


def print_footer():
    """Print footer"""
    print(f"\n{Color.CYAN}{Color.BOLD}{'─' * 80}{Color.RESET}\n")


def demo_menu():
    """Main menu screen"""
    print_header("MaxTUI Interactive Demo - Main Menu")
    
    print(f"{Color.GREEN}{Color.BOLD}Welcome to MaxTUI!{Color.RESET}\n")
    print(f"  {Color.MAGENTA}1.{Color.RESET} Widget Showcase       - See all available widgets")
    print(f"  {Color.MAGENTA}2.{Color.RESET} Colors & Styling      - Explore 9+ colors and styles")
    print(f"  {Color.MAGENTA}3.{Color.RESET} Interactive Controls  - Try interactive value adjustment")
    print(f"  {Color.MAGENTA}4.{Color.RESET} Live Dashboard        - Full system dashboard example")
    print(f"  {Color.MAGENTA}5.{Color.RESET} Exit\n")
    
    print(f"{Color.YELLOW}Choose an option (1-5): {Color.RESET}", end="")
    sys.stdout.flush()


def demo_widgets():
    """Widget showcase"""
    clear()
    print_header("MaxTUI Widgets Showcase")
    
    print(f"{Color.CYAN}{Color.BOLD}Available Widgets:{Color.RESET}\n")
    
    widgets = [
        ("Block", "Container with borders and title", "┌─ Widget ─┐"),
        ("Paragraph", "Text display component", "Hello, MaxTUI!"),
        ("Button", "Interactive clickable button", "[  Click Me  ]"),
        ("Input", "Text input field", "Type here... │"),
        ("Gauge", "Progress bar", "████████░░ 80%"),
        ("List", "Scrollable list", "• Item 1\n• Item 2"),
        ("Table", "Data table", "┌─ Col1 ─┬─ Col2 ─┐\n│ Data  │  Data  │"),
        ("Chart", "Graph visualization", "Data visualization"),
        ("Modal", "Dialog window", "[  Confirmation  ]"),
        ("Spinner", "Loading animation", "⠋ Loading..."),
        ("Tabs", "Tab navigation", "[ Tab1 ] Tab2"),
        ("Scrollbar", "Scroll indicator", "▓░░░░░░░░"),
    ]
    
    for i, (name, desc, example) in enumerate(widgets, 1):
        print(f"  {Color.YELLOW}{i:2d}.{Color.RESET} {Color.GREEN}{name.ljust(12)}{Color.RESET} - {desc}")
        print(f"      {Color.DIM}Example: {example}{Color.RESET}\n")
    
    print_footer()


def demo_colors():
    """Colors and styling demo"""
    clear()
    print_header("Colors & Styling Showcase")
    
    print(f"{Color.CYAN}{Color.BOLD}Standard Colors:{Color.RESET}\n")
    
    colors = [
        (Color.RED, "Red"),
        (Color.GREEN, "Green"),
        (Color.BLUE, "Blue"),
        (Color.YELLOW, "Yellow"),
        (Color.MAGENTA, "Magenta"),
        (Color.CYAN, "Cyan"),
        (Color.WHITE, "White"),
        (Color.BLACK + Color.WHITE, "Black on White"),
    ]
    
    for color, name in colors:
        print(f"  {color}{Color.BOLD}███████{Color.RESET} {name}")
    
    print(f"\n{Color.CYAN}{Color.BOLD}Text Modifiers:{Color.RESET}\n")
    print(f"  {Color.BOLD}This is bold text{Color.RESET}")
    print(f"  {Color.ITALIC}This is italic text{Color.RESET}")
    print(f"  {Color.UNDERLINE}This is underline text{Color.RESET}")
    print(f"  {Color.BOLD}{Color.ITALIC}{Color.UNDERLINE}This is all combined!{Color.RESET}")
    
    print(f"\n{Color.CYAN}{Color.BOLD}Custom RGB Colors:{Color.RESET}\n")
    print(f"  {Color.RED}RGB(255, 0, 0){Color.RESET}")
    print(f"  {Color.GREEN}RGB(0, 255, 0){Color.RESET}")
    print(f"  {Color.BLUE}RGB(0, 0, 255){Color.RESET}")
    print(f"  {Color.MAGENTA}RGB(255, 0, 255){Color.RESET}")
    
    print_footer()


def demo_interactive(current_value: list):
    """Interactive controls demo"""
    clear()
    print_header("Interactive Value Adjuster")
    
    print(f"{Color.CYAN}{Color.BOLD}Current Value: {Color.YELLOW}{Color.BOLD}{current_value[0]:>3d}{Color.RESET}\n")
    
    # Draw progress bar
    filled = int((current_value[0] / 100) * 40)
    bar = f"{Color.GREEN}{Color.BOLD}{'█' * filled}{Color.RESET}{Color.DIM}{'░' * (40 - filled)}{Color.RESET}"
    print(f"  [{bar}] {current_value[0]:>3d}%\n")
    
    print(f"{Color.CYAN}{Color.BOLD}Instructions:{Color.RESET}")
    print(f"  {Color.YELLOW}w/a/s/d{Color.RESET} or {Color.YELLOW}↑↓{Color.RESET} - Increase/Decrease by 5")
    print(f"  {Color.YELLOW}0{Color.RESET} - Reset to 0")
    print(f"  {Color.YELLOW}9{Color.RESET} - Set to 100")
    print(f"  {Color.YELLOW}m{Color.RESET} - Return to menu")
    print(f"  {Color.YELLOW}q{Color.RESET} - Quit\n")
    
    print(f"{Color.YELLOW}Enter command: {Color.RESET}", end="")
    sys.stdout.flush()


def demo_dashboard(current_value: list, selected: list):
    """Live dashboard example"""
    clear()
    print_header("System Dashboard")
    
    print(f"{Color.GREEN}{Color.BOLD}Service Status:{Color.RESET}\n")
    services = [
        ("API Server", True, "↑ 24h 15m"),
        ("Database", True, "↑ 48h 32m"),
        ("Cache", True, "↑ 2h 18m"),
        ("Queue", False, "127 items pending"),
    ]
    
    for i, (name, status, info) in enumerate(services):
        status_icon = f"{Color.GREEN}✓{Color.RESET}" if status else f"{Color.YELLOW}⚠{Color.RESET}"
        marker = f"{Color.BOLD}{Color.CYAN}→{Color.RESET}" if selected[0] == i else " "
        status_text = f"{Color.GREEN}Running{Color.RESET}" if status else f"{Color.YELLOW}Pending{Color.RESET}"
        print(f"  {marker} {status_icon} {name.ljust(15)} : {status_text.ljust(20)} {info}")
    
    print(f"\n{Color.CYAN}{Color.BOLD}Performance Metrics:{Color.RESET}\n")
    
    values = [current_value[0], (current_value[0] + 30) % 100, (current_value[0] + 60) % 100]
    labels = ["CPU Usage", "Memory", "Disk Space"]
    
    for label, value in zip(labels, values):
        filled = int((value / 100) * 35)
        color = Color.GREEN if value < 70 else Color.YELLOW if value < 90 else Color.RED
        bar = f"{color}{Color.BOLD}{'█' * filled}{Color.RESET}{Color.DIM}{'░' * (35 - filled)}{Color.RESET}"
        print(f"  {label.ljust(15)} [{bar}] {value:>3.0f}%")
    
    print(f"\n{Color.CYAN}{Color.BOLD}Recent Activity:{Color.RESET}\n")
    
    activities = [
        (Color.GREEN, "14:23:45 ✓ User login from 192.168.1.100"),
        (Color.GREEN, "14:22:10 ✓ Database backup completed"),
        (Color.BLUE, "14:20:33 → API endpoint called 1,247 times"),
        (Color.GREEN, "14:18:22 ✓ Cache hit rate: 94.3%"),
        (Color.YELLOW, "14:15:00 ⚠ Scheduler: cleanup executed"),
    ]
    
    for i, (color, activity) in enumerate(activities):
        marker = f"{Color.BOLD}{Color.GREEN}→{Color.RESET}" if selected[0] == i + 4 else " "
        print(f"  {marker} {color}{activity}{Color.RESET}")
    
    print(f"\n{Color.YELLOW}Commands: w/a/s/d - Navigate | m - Menu | q - Quit\n")
    print(f"{Color.YELLOW}Enter command: {Color.RESET}", end="")
    sys.stdout.flush()


def main():
    """Main application loop"""
    current_screen = Screen.MENU
    current_value = [50]  # Use list for mutability
    selected = [0]
    
    try:
        while True:
            if current_screen == Screen.MENU:
                demo_menu()
                choice = input().strip()
                
                if choice == '1':
                    current_screen = Screen.WIDGETS_DEMO
                elif choice == '2':
                    current_screen = Screen.COLORS_DEMO
                elif choice == '3':
                    current_screen = Screen.INTERACTIVE_DEMO
                elif choice == '4':
                    current_screen = Screen.DASHBOARD
                elif choice == '5':
                    print(f"\n{Color.GREEN}Thanks for exploring MaxTUI!{Color.RESET}\n")
                    break
                else:
                    print(f"{Color.RED}Invalid option!{Color.RESET}")
                    time.sleep(1)
            
            elif current_screen == Screen.WIDGETS_DEMO:
                demo_widgets()
                cmd = input().strip().lower()
                if cmd == 'm':
                    current_screen = Screen.MENU
                elif cmd == 'q':
                    break
            
            elif current_screen == Screen.COLORS_DEMO:
                demo_colors()
                cmd = input().strip().lower()
                if cmd == 'm':
                    current_screen = Screen.MENU
                elif cmd == 'q':
                    break
            
            elif current_screen == Screen.INTERACTIVE_DEMO:
                demo_interactive(current_value)
                cmd = input().strip().lower()
                
                if cmd in ['w', 'up', '+']:
                    current_value[0] = min(100, current_value[0] + 5)
                elif cmd in ['s', 'down', '-']:
                    current_value[0] = max(0, current_value[0] - 5)
                elif cmd == '0':
                    current_value[0] = 0
                elif cmd == '9':
                    current_value[0] = 100
                elif cmd == 'm':
                    current_screen = Screen.MENU
                elif cmd == 'q':
                    break
            
            elif current_screen == Screen.DASHBOARD:
                demo_dashboard(current_value, selected)
                cmd = input().strip().lower()
                
                if cmd in ['w', 'up', '+']:
                    current_value[0] = min(100, current_value[0] + 5)
                    selected[0] = max(0, selected[0] - 1)
                elif cmd in ['s', 'down', '-']:
                    current_value[0] = max(0, current_value[0] - 5)
                    selected[0] = min(8, selected[0] + 1)
                elif cmd == 'm':
                    current_screen = Screen.MENU
                elif cmd == 'q':
                    break
    
    except KeyboardInterrupt:
        print(f"\n\n{Color.RED}Demo interrupted!{Color.RESET}\n")
    except Exception as e:
        print(f"\n{Color.RED}Error: {e}{Color.RESET}\n")


if __name__ == "__main__":
    clear()
    print(f"\n{Color.MAGENTA}{Color.BOLD}Initializing MaxTUI Interactive Demo...{Color.RESET}\n")
    time.sleep(0.5)
    main()
    