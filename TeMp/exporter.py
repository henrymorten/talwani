import tkinter as tk
import text_to_screen
from PIL import Image, ImageTk, ImageGrab
import os 

def main(self, extension, filename):
    """
    Export all of the canvas to either .jpg, .png or .pdf 
    """
    text_to_screen.main(self,text="")
    #This destroys any current labels on the canvas.

    #Rest of the exporter
    self.update()
    x = self.winfo_rootx() + self.canvas.winfo_x()
    y = self.winfo_rooty() + self.canvas.winfo_y()
    x1 = x + self.canvas.winfo_width()
    y1 = y + self.canvas.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).convert("RGB").save(f"exports/{filename}{extension}")
    


   