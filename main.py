import tkinter as tk
import numpy as np
from tkinter import ttk, filedialog
from PIL import Image, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint Program")
        
        self.toolbar = tk.Frame(self.root, padx=5, pady=5)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.shapes_var = tk.StringVar(value="DDA Line")
        self.shapes_menu = ttk.Combobox(self.toolbar, textvariable=self.shapes_var, values=[
            "DDA Line", "Bresenham Line", "Circle Midpoint", "Ellips Midpoint"
        ])
        self.shapes_menu.pack(side=tk.LEFT, padx=5)
        
        self.transform_var = tk.StringVar(value="None")
        self.transform_menu = ttk.Combobox(self.toolbar, textvariable=self.transform_var, values=[
            "None", "Translate", "Rotate", "Scale", "Reflect"
        ])
        self.transform_menu.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def on_mouse_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.delete("temp_shape")
        self.draw_shape(self.start_x, self.start_y, self.end_x, self.end_y, "temp_shape")
    
    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.delete("temp_shape")
        self.draw_shape(self.start_x, self.start_y, self.end_x, self.end_y)
    
    def draw_shape(self, x1, y1, x2, y2, tag=None):
        shape = self.shapes_var.get()
        if shape == "DDA Line":
            self.draw_dda_line(x1, y1, x2, y2, tag)
        elif shape == "Bresenham Line":
            self.draw_bresenham_line(x1, y1, x2, y2, tag)
        elif shape == "Circle Midpoint":
            self.draw_circle_midpoint(x1, y1, x2, y2, tag)
        elif shape == "Ellips Midpoint":
            self.draw_ellips_midpoint(x1, y1, x2, y2, tag)
    
    def draw_dda_line(self, x1, y1, x2, y2, tag):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(steps):
            self.canvas.create_oval(x, y, x+1, y+1, fill="black", tags=tag)
            x += x_inc
            y += y_inc
    
    def draw_bresenham_line(self, x1, y1, x2, y2, tag):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.canvas.create_oval(x1, y1, x1+1, y1+1, fill="black", tags=tag)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def draw_circle_midpoint(self, x1, y1, x2, y2, tag):
        r = int(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        x, y = 0, r
        d = 1 - r
        self._draw_circle_points(x1, y1, x, y, tag)
        while y > x:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_circle_points(x1, y1, x, y, tag)
    
    def _draw_circle_points(self, cx, cy, x, y, tag):
        points = [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
                  (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)]
        for (px, py) in points:
            self.canvas.create_oval(px, py, px+1, py+1, fill="black", tags=tag)
    
    def draw_ellips_midpoint(self, x1, y1, x2, y2, tag):
        rx = abs(x2 - x1)
        ry = abs(y2 - y1)
        rx2 = rx ** 2
        ry2 = ry ** 2
        x, y = 0, ry
        px = 0
        py = 2 * rx2 * y
        self._draw_ellipse_points(x1, y1, x, y, tag)
        p = ry2 - (rx2 * ry) + (0.25 * rx2)
        while px < py:
            x += 1
            px += 2 * ry2
            if p < 0:
                p += ry2 + px
            else:
                y -= 1
                py -= 2 * rx2
                p += ry2 + px - py
            self._draw_ellipse_points(x1, y1, x, y, tag)
        p = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
        while y > 0:
            y -= 1
            py -= 2 * rx2
            if p > 0:
                p += rx2 - py
            else:
                x += 1
                px += 2 * ry2
                p += rx2 - py + px
            self._draw_ellipse_points(x1, y1, x, y, tag)
    
    def _draw_ellipse_points(self, cx, cy, x, y, tag):
        points = [(cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y)]
        for (px, py) in points:
            self.canvas.create_oval(px, py, px+1, py+1, fill="black", tags=tag)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self._save_canvas_as_image(file_path)

    def _save_canvas_as_image(self, file_path):
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Create a new image with the same dimensions as the canvas
        image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(image)
        
        # Copy canvas content to the image
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if len(coords) == 4:
                x1, y1, x2, y2 = coords
                draw.ellipse([x1, y1, x2, y2], fill="black", outline="black")
        
        # Save the image
        image.save(file_path)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
