from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
from utils import analyze_tone, add_glow, apply_depth_of_field

def generate_thumbnail(title, headshot_path, output_path="thumbnail.png"):
    # Load and resize headshot
    headshot = Image.open(headshot_path).convert("RGBA").resize((400, 400))
    
    # Analyze tone and simulate expression (basic: add overlay)
    tone = analyze_tone(title)
    if tone == "positive":
        # Add a simple "excited" effect (e.g., overlay a smile)
        smile = Image.new("RGBA", (100, 100), (255, 255, 0, 128))  # Yellow circle for demo
        headshot.paste(smile, (150, 150), smile)  # Position on face
    # For realism, integrate AI here (e.g., use DeepFace to modify expression)
    
    # Create 1280x720 canvas with high-contrast background
    canvas = Image.new("RGBA", (1280, 720), (20, 20, 50, 255))  # Dark blue gradient base
    draw = ImageDraw.Draw(canvas)
    
    # Add vibrant color overlay
    overlay = Image.new("RGBA", (1280, 720), (255, 0, 100, 50))  # Semi-transparent red
    canvas = Image.alpha_composite(canvas, overlay)
    
    # Apply depth of field
    canvas = apply_depth_of_field(canvas)
    
    # Place headshot prominently (centered with glow)
    headshot_glow = add_glow(headshot, color=(255, 255, 0))
    canvas.paste(headshot_glow, (440, 160), headshot_glow)  # Center-ish
    
    # Add typography (bold, glowing, modern placement)
    font = ImageFont.truetype("fonts/BebasNeue-Bold.ttf", 80)  # Download and place font
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (1280 - text_width) // 2
    text_y = 550  # Bottom third for modern placement
    
    # Draw glowing text
    glow_color = (255, 255, 0, 128)
    for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        draw.text((text_x + offset[0], text_y + offset[1]), title, font=font, fill=glow_color)
    draw.text((text_x, text_y), title, font=font, fill=(255, 255, 255))  # White text
    
    # Save
    canvas.save(output_path)
    return output_path

# Simple GUI
root = tk.Tk()
root.title("Al Thumbnails Maker")

tk.Label(root, text="Video Title:").pack()
title_entry = tk.Entry(root, width=50)
title_entry.pack()

tk.Label(root, text="Headshot Photo:").pack()
photo_path = tk.StringVar()
def select_photo():
    photo_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")]))
tk.Button(root, text="Browse", command=select_photo).pack()

def generate():
    title = title_entry.get()
    photo = photo_path.get()
    if not title or not photo:
        messagebox.showerror("Error", "Please provide title and photo.")
        return
    output = generate_thumbnail(title, photo)
    messagebox.showinfo("Success", f"Thumbnail saved as {output}")

tk.Button(root, text="Generate Thumbnail", command=generate).pack()
root.mainloop()
