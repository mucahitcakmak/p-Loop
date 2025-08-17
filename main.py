import sys
import time
import os

# Import animation functions
try:
    from loop import loop as wave_highlight
except ImportError:
    print("Error: wave_highlight.py not found in current directory!")
    sys.exit(1)

try:
    from black_hole import spiral_void
except ImportError:
    print("Error: spiral_void.py not found in current directory!")
    sys.exit(1)

def print_banner():
    """Display welcome banner"""
    print("Welcome to the number one black hole of the universe.")
    print("─" * 22)

def get_user_input():
    """Get text input from user with validation"""
    print("\nEnter text to process:")
    
    text = input("> ").strip()
    
    if not text:
        text = "to stare off into the distance"
        print(f"Using: {text}")
    
    return text

def countdown(seconds=3):
    """Display countdown before starting animation"""
    print(f"\nInitializing...")
    for i in range(seconds, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Starting.\n")

def phase_transition():
    """Display transition between phases"""
    print("\nAnalysis complete.")
    time.sleep(2)

def main():
    """Main animation controller"""
    try:
        # Clear screen and show banner
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        
        # Get user input
        text = get_user_input()
        
        # Countdown
        countdown(3)
        
        # Phase 1: Wave Analysis
        print("Analyzing text...")
        time.sleep(1)
        
        # Run wave highlight animation
        if (wave_highlight(text, delay=0.025, wave_speed=2.0) == -1):
            return
        
        # Transition between phases
        phase_transition()
        
        # Phase 2: Spiral Void
        print("Processing...")
        time.sleep(1)
        
        # Run spiral void animation
        spiral_void(text, duration=6.0)
        
        # Final message
        print("\nProcess completed.")
        print("Text has been consumed.")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted.")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        
    finally:
        # Ensure cursor is visible
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == "__main__":
    main()