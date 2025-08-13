#!/usr/bin/env python3
"""
Simple test to verify GUI can be created and displayed
"""

import tkinter as tk
from tkinter import messagebox
import sys

def create_test_window():
    """Create a simple test window"""
    root = tk.Tk()
    root.title("Visual AI Regression - GUI Test")
    root.geometry("500x400")
    root.configure(bg='#f0f0f0')
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"500x400+{x}+{y}")
    
    # Make sure window is on top
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    # Test content
    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    title = tk.Label(
        frame, 
        text="🚀 GUI Test Successful!", 
        font=("Arial", 18, "bold"),
        bg='#f0f0f0',
        fg='#2c3e50'
    )
    title.pack(pady=20)
    
    subtitle = tk.Label(
        frame,
        text="If you can see this window, the GUI is working correctly!",
        font=("Arial", 12),
        bg='#f0f0f0',
        fg='#34495e'
    )
    subtitle.pack(pady=10)
    
    # Test button
    def on_test():
        messagebox.showinfo("Success", "✅ GUI components are working perfectly!")
    
    test_btn = tk.Button(
        frame,
        text="Test Button Click",
        command=on_test,
        font=("Arial", 12),
        bg='#3498db',
        fg='white',
        padx=20,
        pady=10
    )
    test_btn.pack(pady=20)
    
    # Info
    info = tk.Label(
        frame,
        text="This confirms that:\n• Tkinter is properly installed\n• Display is working\n• GUI can be created and shown",
        font=("Arial", 10),
        bg='#f0f0f0',
        fg='#7f8c8d',
        justify='left'
    )
    info.pack(pady=20)
    
    # Close button
    close_btn = tk.Button(
        frame,
        text="Close Test",
        command=root.quit,
        font=("Arial", 12),
        bg='#e74c3c',
        fg='white',
        padx=20,
        pady=5
    )
    close_btn.pack(pady=10)
    
    print("✅ Test window created successfully!")
    print("🔍 Looking for window on screen...")
    
    return root

def main():
    """Main test function"""
    try:
        print("🚀 Starting GUI test...")
        root = create_test_window()
        print("🎯 Entering main loop...")
        root.mainloop()
        print("✅ GUI test completed successfully!")
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Test failed!")
        sys.exit(1)
