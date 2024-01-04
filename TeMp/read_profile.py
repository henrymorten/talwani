import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

def main():
    """
    
    """
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename()

    if file_path:
        #Read the contents of the file
        data = pd.read_csv(file_path,delimiter=',',header=None)
        
    #
    data.to_csv("TeMp/profile.csv",index=False,header=None)
    #
    filename = os.path.basename(file_path)
    #
    # Remove the file extension if needed
    filename_without_extension = os.path.splitext(filename)[0]
    #
    return data, filename_without_extension
