#!/usr/bin/env python3
"""
Simple GUI test to verify Tkinter is working
"""

import tkinter as tk
from tkinter import messagebox

def test_gui():
    """Test basic GUI functionality"""
    root = tk.Tk()
    root.title("GUI Test - Visual AI Regression Module")
    root.geometry("400x300")
    
    # Test label
    label = tk.Label(root, text="✅ GUI is working!", font=("Arial", 16, "bold"))
    label.pack(pady=50)
    
    # Test button
    def on_button_click():
        messagebox.showinfo("Success", "✅ All GUI components are working!")
        
    button = tk.Button(root, text="Test Button", command=on_button_click, font=("Arial", 12))
    button.pack(pady=20)
    
    # Close button
    close_button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12))
    close_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("Starting GUI test...")
    test_gui()
    print("GUI test completed.")
