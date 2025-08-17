import sys
import time
import math
import random
import os

def get_terminal_size():
    """Get terminal dimensions"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24

def clear_screen():
    """Clear terminal screen"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def spiral_void(text: str, duration=6.0):
    """
    Creates a spiral black hole that consumes text and ends with an explosion
    
    Args:
        text (str): Text to be consumed by the spiral void
        duration (float): Duration of the spiral animation in seconds
    """
    if not text:
        print("Please provide some text to consume!")
        return
    
    width, height = get_terminal_size()
    center_x, center_y = width // 2, height // 2
    
    try:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        
        fps = 25
        frame_time = 1.0 / fps
        total_frames = int(duration * fps)
        
        # Phase 1: Spiral consumption
        for frame in range(total_frames):
            start_time = time.perf_counter()
            clear_screen()
            
            progress = frame / total_frames
            
            # Create spiral
            for i in range(100):
                t = i * 0.3 + frame * 0.2
                r = i * 0.5 * (1 - progress * 0.8)
                
                if r > 0:
                    x = int(center_x + r * math.cos(t))
                    y = int(center_y + r * math.sin(t) * 0.5)
                    
                    if 0 <= x < width and 0 <= y < height:
                        intensity = 1 - (r / 50)
                        if intensity > 0.8:
                            sys.stdout.write(f"\033[{y+1};{x+1}H\033[33m*\033[0m")  # Yellow star
                        elif intensity > 0.5:
                            sys.stdout.write(f"\033[{y+1};{x+1}H\033[37m·\033[0m")  # White dot
                        else:
                            sys.stdout.write(f"\033[{y+1};{x+1}H.")  # Regular dot
            
            # Text spiraling into center
            chars_remaining = int(len(text) * (1 - progress))
            if chars_remaining > 0:
                spiral_text = text[:chars_remaining]
                text_radius = 15 * (1 - progress)
                text_angle = frame * 0.3
                
                text_x = int(center_x + text_radius * math.cos(text_angle) - len(spiral_text)//2)
                text_y = int(center_y + text_radius * math.sin(text_angle) * 0.5)
                
                if 0 <= text_y < height and 0 <= text_x < width:
                    # Text gets dimmer as it approaches center
                    if progress > 0.7:
                        sys.stdout.write(f"\033[{text_y+1};{text_x+1}H\033[2m{spiral_text}\033[0m")  # Dim
                    else:
                        sys.stdout.write(f"\033[{text_y+1};{text_x+1}H{spiral_text}")
            
            sys.stdout.flush()
            
            elapsed = time.perf_counter() - start_time
            time.sleep(max(0, frame_time - elapsed))
        
        # Phase 2: Explosion animation
        explosion_duration = 2.0
        explosion_frames = int(explosion_duration * fps)
        
        for frame in range(explosion_frames):
            start_time = time.perf_counter()
            clear_screen()
            
            explosion_progress = frame / explosion_frames
            
            # Create explosion effect
            max_explosion_radius = min(width//2, height) - 5
            current_radius = explosion_progress * max_explosion_radius
            
            # Multiple explosion rings
            for ring in range(3):
                ring_radius = current_radius - ring * 3
                if ring_radius > 0:
                    particles = int(ring_radius * 8)  # More particles for bigger rings
                    
                    for i in range(particles):
                        angle = (i / particles) * 2 * math.pi
                        # Add some randomness to explosion
                        rand_offset = random.uniform(-0.3, 0.3)
                        actual_radius = ring_radius + rand_offset
                        
                        x = int(center_x + actual_radius * math.cos(angle))
                        y = int(center_y + actual_radius * math.sin(angle) * 0.6)  # Slightly flattened
                        
                        if 0 <= x < width and 0 <= y < height:
                            # Different explosion characters and colors
                            if ring == 0:  # Inner ring - bright
                                chars = ['*', '✦', '✧', '●']
                                color = '\033[91m'  # Bright red
                            elif ring == 1:  # Middle ring
                                chars = ['*', '·', '○', '+']
                                color = '\033[93m'  # Bright yellow
                            else:  # Outer ring
                                chars = ['·', '.', '°', '˙']
                                color = '\033[97m'  # Bright white
                            
                            char = random.choice(chars)
                            sys.stdout.write(f"\033[{y+1};{x+1}H{color}{char}\033[0m")
            
            # Add some random sparks
            for _ in range(int(20 * (1 - explosion_progress))):
                spark_x = center_x + random.randint(-int(current_radius*1.5), int(current_radius*1.5))
                spark_y = center_y + random.randint(-int(current_radius*0.8), int(current_radius*0.8))
                
                if 0 <= spark_x < width and 0 <= spark_y < height:
                    spark_char = random.choice(['*', '·', '+', '˙'])
                    spark_color = random.choice(['\033[91m', '\033[93m', '\033[97m'])
                    sys.stdout.write(f"\033[{spark_y+1};{spark_x+1}H{spark_color}{spark_char}\033[0m")
            
            sys.stdout.flush()
            
            elapsed = time.perf_counter() - start_time
            time.sleep(max(0, frame_time - elapsed))
        
        # Final fade out
        fade_frames = 20
        for frame in range(fade_frames):
            start_time = time.perf_counter()
            clear_screen()
            
            fade_progress = frame / fade_frames
            particles_count = int(50 * (1 - fade_progress))
            
            for _ in range(particles_count):
                x = center_x + random.randint(-max_explosion_radius//2, max_explosion_radius//2)
                y = center_y + random.randint(-max_explosion_radius//3, max_explosion_radius//3)
                
                if 0 <= x < width and 0 <= y < height:
                    sys.stdout.write(f"\033[{y+1};{x+1}H\033[2m·\033[0m")  # Dim dots
            
            sys.stdout.flush()
            
            elapsed = time.perf_counter() - start_time
            time.sleep(max(0, frame_time - elapsed))
        
        # Clear and show completion message
        clear_screen()
        completion_msg = "Text consumed by the void."
        msg_x = center_x - len(completion_msg) // 2
        sys.stdout.write(f"\033[{center_y+1};{msg_x+1}H\033[2m{completion_msg}\033[0m")
        sys.stdout.write(f"\033[{height};1H")
        sys.stdout.flush()
        
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == "__main__":
    print("Spiral Void Text Animation")
    print("=" * 26)
    
    text = input("\nEnter text to be consumed by the void: ").strip()
    if not text:
        text = "to stare off into the distance"
    
    print(f"\nPreparing to consume: '{text}'")
    print("Starting in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    spiral_void(text, duration=6.0)