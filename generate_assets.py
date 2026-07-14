# generate_assets.py
"""Asset generator script. Programmatically generates the assets/ directory
and fills it with synthetic audio (WAV) and splash graphics (PNG).
"""
import os
import wave
import struct
import math
from PIL import Image, ImageDraw

def generate_wav(filepath: str, frequencies: list, durations: list, volume: float = 0.3):
    """Generates a WAV audio file containing consecutive sine-wave notes."""
    sample_rate = 44100
    try:
        with wave.open(filepath, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            
            for freq, duration in zip(frequencies, durations):
                num_samples = int(sample_rate * duration)
                for i in range(num_samples):
                    t = float(i) / sample_rate
                    # Simple envelope to prevent pop sounds at start/end of notes
                    envelope = 1.0
                    attack_samples = int(sample_rate * 0.01)
                    decay_samples = int(sample_rate * 0.02)
                    if i < attack_samples:
                        envelope = float(i) / attack_samples
                    elif i > num_samples - decay_samples:
                        envelope = float(num_samples - i) / decay_samples
                    
                    value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * t) * envelope)
                    data = struct.pack("<h", value)
                    w.writeframesraw(data)
        print(f"[Assets] Generated audio: {filepath}")
    except Exception as e:
        print(f"[Assets] Failed to generate audio {filepath}: {e}")

def generate_splash(filepath: str):
    """Generates a premium, gradient splash screen image."""
    try:
        # Create a premium gradient image (600x400)
        width, height = 600, 400
        img = Image.new("RGB", (width, height), color="#0F172A")
        draw = ImageDraw.Draw(img)
        
        # Draw a subtle background grid
        grid_color = "#1E293B"
        grid_size = 40
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)
            
        # Draw decorative glowing circles/accents
        draw.ellipse([(width//2 - 120, height//2 - 120), (width//2 + 120, height//2 + 120)], outline="#3B82F6", width=2)
        draw.ellipse([(width//2 - 130, height//2 - 130), (width//2 + 130, height//2 + 130)], outline="#1D4ED8", width=1)
        
        # Draw a custom stylized Tic-Tac-Toe grid in the center
        box_size = 50
        cx, cy = width // 2, height // 2
        draw.line([(cx - box_size//2, cy - box_size*1.5), (cx - box_size//2, cy + box_size*1.5)], fill="#64748B", width=3)
        draw.line([(cx + box_size//2, cy - box_size*1.5), (cx + box_size//2, cy + box_size*1.5)], fill="#64748B", width=3)
        draw.line([(cx - box_size*1.5, cy - box_size//2), (cx + box_size*1.5, cy - box_size//2)], fill="#64748B", width=3)
        draw.line([(cx - box_size*1.5, cy + box_size//2), (cx + box_size*1.5, cy + box_size//2)], fill="#64748B", width=3)
        
        # Add styled X and O indicators
        # X mark in top-left
        draw.line([(cx - box_size, cy - box_size), (cx - box_size//2, cy - box_size//2)], fill="#3B82F6", width=5)
        draw.line([(cx - box_size, cy - box_size//2), (cx - box_size//2, cy - box_size)], fill="#3B82F6", width=5)
        # O mark in center
        draw.ellipse([(cx - box_size//3, cy - box_size//3), (cx + box_size//3, cy + box_size//3)], outline="#EF4444", width=5)
        
        img.save(filepath, "PNG")
        print(f"[Assets] Generated splash image: {filepath}")
    except Exception as e:
        print(f"[Assets] Failed to generate splash image {filepath}: {e}")

if __name__ == "__main__":
    # Get paths relative to script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Generate sounds
    # click: short high beep
    generate_wav(os.path.join(assets_dir, "click.wav"), [880.0], [0.05], volume=0.2)
    # win: nice three-note major chord (C5 - E5 - G5)
    generate_wav(os.path.join(assets_dir, "win.wav"), [523.25, 659.25, 783.99], [0.12, 0.12, 0.3], volume=0.25)
    # lose: descending flat tone (G4 - E4 - C4)
    generate_wav(os.path.join(assets_dir, "lose.wav"), [392.0, 329.63, 261.63], [0.15, 0.15, 0.45], volume=0.25)
    # draw: dual neutral tone
    generate_wav(os.path.join(assets_dir, "draw.wav"), [440.0, 440.0], [0.15, 0.25], volume=0.2)
    
    # Generate splash image
    generate_splash(os.path.join(assets_dir, "splash.png"))
