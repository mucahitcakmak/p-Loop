import sys
import time
import math

def loop(text: str, delay=0.02, wave_speed=3):
    """
    Creates a smooth wave highlight animation that flows through text.
    
    The animation starts from the second character and flows to the second-to-last character,
    then returns back. Each cycle narrows the animation area until it reaches the center.
    
    Args:
        text (str): The text to animate
        delay (float): Delay between frames in seconds
        wave_speed (float): Speed of the wave effect
    """
    if not text or len(text) < 10:
        print("Seriously?! You should try writing something. (at least 10 characters)")
        return -1
    
    n = len(text)
    
    try:
        # Hide cursor
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        
        start_offset = 1  # Start from 2nd character
        end_offset = n - 1  # End at second-to-last character
        
        # Continue until the animation area narrows to the center
        while start_offset < end_offset:
            # Left to right animation
            for i in range(start_offset, end_offset):
                t0 = time.perf_counter()
                
                output = "\r"
                for pos, char in enumerate(text):
                    if start_offset <= pos <= i:
                        # Calculate wave effect
                        wave_pos = (pos - start_offset) / max(1, i - start_offset)
                        wave_intensity = math.sin(wave_pos * math.pi * wave_speed) * 0.5 + 0.5
                        
                        if wave_intensity > 0.7:
                            output += f"\033[43m\033[30m{char}\033[0m"  # Bright yellow
                        elif wave_intensity > 0.4:
                            output += f"\033[103m\033[30m{char}\033[0m"  # Light yellow
                        else:
                            output += f"\033[107m\033[30m{char}\033[0m"  # White
                    else:
                        output += char
                
                sys.stdout.write(output)
                sys.stdout.flush()
                
                elapsed = time.perf_counter() - t0
                time.sleep(max(0, delay - elapsed))
            
            # Right to left animation
            for i in range(end_offset - 1, start_offset - 1, -1):
                t0 = time.perf_counter()
                
                output = "\r"
                for pos, char in enumerate(text):
                    if i <= pos < end_offset:
                        # Calculate wave effect
                        wave_pos = (end_offset - 1 - pos) / max(1, end_offset - 1 - i)
                        wave_intensity = math.sin(wave_pos * math.pi * wave_speed) * 0.5 + 0.5
                        
                        if wave_intensity > 0.7:
                            output += f"\033[43m\033[30m{char}\033[0m"  # Bright yellow
                        elif wave_intensity > 0.4:
                            output += f"\033[103m\033[30m{char}\033[0m"  # Light yellow
                        else:
                            output += f"\033[107m\033[30m{char}\033[0m"  # White
                    else:
                        output += char
                
                sys.stdout.write(output)
                sys.stdout.flush()
                
                elapsed = time.perf_counter() - t0
                time.sleep(max(0, delay - elapsed))
            
            # Narrow the animation area for next cycle
            start_offset += 1
            end_offset -= 1
        
        # Show final text without highlighting
        sys.stdout.write(f"\r{text}")
        sys.stdout.flush()
        print()
        
    finally:
        # Show cursor
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == "__main__":
    # Example usage
    loop("to stare off into the distance", delay=0.03, wave_speed=1.5)