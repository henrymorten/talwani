import tkinter as tk

# Global variables to store the label and destruction task
global_label = None
destruction_task = None

# Function to create and manage the label
def main(self, text):
    """
    
    """
    global global_label, destruction_task

    # Cancel any pending destruction task
    if destruction_task:
        self.after_cancel(destruction_task)  # Cancel pending label destruction

    # Destroy the existing label if it exists
    if global_label:
        global_label.destroy()

    if text == "":
        return self, global_label 
    # Return the canvas without creating a new label if text is empty


    # Create the label with specified font
    font = ("Helvetica", 16)

    # Create a label widget with the text and font
    global_label = tk.Label(self, text=text, font=font)

    # Place the label at the bottom right corner of the canvas
    global_label.place(relx=1.0, rely=1.0, anchor="se")
    
    # Function to delete the label
    def delete_label():
        if global_label:
            global_label.destroy()
    
    # Schedule label destruction after 10,000 milliseconds (10 seconds)
    destruction_task = self.after(10_000, delete_label)


    return self, global_label