import tkinter as tk
import customtkinter
from PIL import Image, ImageTk, ImageGrab
from tktooltip import ToolTip
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
from pynput import keyboard, mouse

### Other functions
import read_profile
import exporter
import remove
import plot_profile
import text_to_screen
import load_model

#Define global variables:
global xlabel, ylabel, legend, label_width

ylabel = "Gravity (mGal)"
xlabel = "Distance along profile (km)"
legend = "Profile"
label_width = 0

folder_path = "TeMp/"
remove.remove_folder_contents(folder_path)

customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("PYtalwani")
        self.geometry(f"{1100}x{580}")
        #Define the pop-up descriptors:
        
        # Load the .png image
        redo_image = Image.open("images/redo.png")
        #Done this as the two images I had before had different resolutions
        undo_image = redo_image.transpose(Image.FLIP_LEFT_RIGHT)


        # Convert the image to Tkinter format
        undo_logo = customtkinter.CTkImage(undo_image)
        redo_logo = customtkinter.CTkImage(redo_image)

        #Set it to 0.7, as forwhatever reason thats the default when loading
        customtkinter.set_widget_scaling(0.7)

        # Define column for sidebar
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(11, weight=1)
        #
        #Undo / Redo
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.undo_button,image=undo_logo, text="Undo")
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=5,sticky="n")
        #ToolTip(self.sidebar_button_1, msg="Undo", follow=True)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.redo_button,image=redo_logo, text="Redo")
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=5,sticky="n")
        #ToolTip(self.sidebar_button_2, msg="Redo", follow=True)
        #
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.load_profie,text="Load Profile")
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.new_model, text="New Model")
        self.sidebar_button_4.grid(row=4, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=self.load_model, text="Load Model")
        self.sidebar_button_5.grid(row=5, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_6 = customtkinter.CTkOptionMenu(self.sidebar_frame, command=self.save_model, values=["Save Model", "Save Model as"])
        self.sidebar_button_6.grid(row=6, column=0, padx=10, pady=5,sticky="n")
        self.sidebar_button_6.set("Save model")
        #
        self.sidebar_button_7 = customtkinter.CTkOptionMenu(self.sidebar_frame, command=self.export_as, values=[".jpg", ".png", ".pdf"])
        self.sidebar_button_7.grid(row=7, column=0, padx=10, pady=5,sticky="n")
        self.sidebar_button_7.set("Export as")
        #
        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, command=self.create_body, text="Create Body")
        self.sidebar_button_8.grid(row=8, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_9 = customtkinter.CTkButton(self.sidebar_frame, command=self.auto_edit_body, text="Auto Create Body")
        self.sidebar_button_9.grid(row=9, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_10 = customtkinter.CTkButton(self.sidebar_frame, command=self.edit_body, text="Edit Body")
        self.sidebar_button_10.grid(row=10, column=0, padx=10, pady=5,sticky="n")
        #
        self.sidebar_button_11 = customtkinter.CTkButton(self.sidebar_frame, command=self.edit_parameters, text="Edit Parameters")
        self.sidebar_button_11.grid(row=11, column=0, padx=10, pady=5,sticky="n")
        #
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=12, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set(customtkinter.get_appearance_mode())
        self.appearance_mode_optionemenu.grid(row=13, column=0, padx=10, pady=(5, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=14, column=0, padx=10, pady=(5, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["70%","80%", "90%", "100%", "110%", "120%", "130%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=15, column=0, padx=10, pady=(5, 20))

        
        # Create a canvas next to the side bar
        # Create a canvas next to the side bar
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)  # Create a canvas widget
        self.canvas.grid(row=0, column=1, rowspan=11, sticky="nsew", padx=(0, 1), pady=(0, 1))  # Span multiple rows and fill the remaining space with adjusted padx and pady values


        # Set the weights for the rows and columns to make them expand and fill the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    ####
    #All of the buttons functionality

    def undo_button(self):
        command = "Undo"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

    def redo_button(self):
        command = "Redo"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

    def load_profie(self):
        command = "Loading profile..."
        print(command)
        [self, label] = text_to_screen.main(self,text=command)
        
        try:
            global profile, filename
            [profile, filename] = read_profile.main()
            self.plot_profile_data()
            command = f"Sucessfully loaded: {filename}"
            print(command)
            [self, label] = text_to_screen.main(self,text=command)
        except NameError:
            command = "Loading of profile cancelled."
            print(command)
            [self, label] = text_to_screen.main(self,text=command)
        except:
            command = "Can't plot the selected file. Please check the file type, and the data formating."
            print(command)
            [self, label] = text_to_screen.main(self,text=command)
        
    def new_model(self):
        command = "Getting new model"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

    def load_model(self):
        command = "Loading the model..."
        print(command)
        [self,label] = text_to_screen.main(self,text=command)
        try:
            global profile, model_name
            [profile, model_name] = load_model.main()        
        except NameError:
            command = "Loading of profile cancelled."
            print(command)
            [self,label] = text_to_screen.main(self,text=command)
        except:
            command = "Can't plot the selected file. Please check the file type, and the data formating."
            print(command)
            [self,label] = text_to_screen.main(self,text=command)
    
    def save_model(self, option):
        command = "Saving model:"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)
    
    def export_as(self, extension):
        command = f"Exporting as: {filename}{extension}"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)
        try:
            exporter.main(self, extension, filename)
            command = f"Exported as {filename}{extension}"
            print(command)
            [self,label] = text_to_screen.main(self,text=command)
        except NameError:
            command = "Please load a profile first!"
            print(command)
            [self, label] = text_to_screen.main(self,text=command)
        except:
            command = "An unknown error has occured, please try again"
            print(command)
            [self, label] = text_to_screen.main(self,text=command)
        self.sidebar_button_7.set("Export as")

    def create_body(self):
        command = "Left click to place vertices in any order. Right click to finish. Press 'Escape' to cancel."
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

    
    def edit_body(self):
        command = "Click on a body to edit:"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

        edit_body_window = EditBodyWindow()
        edit_body_window.mainloop()

    def auto_edit_body(self):
        command = "Automaticallyy create a body, please define parameters."
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

        auto_edit_body_window = AutoCreateBodyWindow()
        auto_edit_body_window.mainloop()
    
    def edit_parameters(self):
        command = "Edit modelling parameters:"
        print(command)
        [self, label] = text_to_screen.main(self,text=command)

        edit_parameter_window = EditParametersWindow()
        edit_parameter_window.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def plot_profile_data(self):
            if profile is not None:
                try:
                    global canvas 
                    plot_profile.main(profile, self,ylabel, xlabel, legend)
                except:
                    print("Couldn't plot the profile - please check the formatting of the data.")

###
## Create separate windows for specific tasks
class AutoCreateBodyWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Auto Create Body")
        self.geometry("400x300")
        self.resizable(False,False)

        #Add a slide bar for misfit:
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="ns") 
        self.slider_progressbar_frame.grid_rowconfigure(0, weight=1)  # Adjusted row weight

        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=15,orientation="vertical")  # Added orient parameter
        self.slider_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ns")  # Adjusted row, column, and sticky values

        label_text = "Slider Label"
        self.slider_label = tk.Label(self.slider_progressbar_frame, text=label_text)
        self.slider_label.grid(row=0, column=1, padx=(10, 20), pady=(10, 10), sticky="ns")
        

class EditBodyWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Edit Body")
        self.geometry("400x300")

class EditParametersWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Edit Parameters")
        self.geometry("400x300")

if __name__ == "__main__":
    app = App()

    app.mainloop()
