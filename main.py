import tkinter as tk
from tkinter import messagebox, filedialog
from unlock_pdf import unlock_pdf

def brute_force_unlock():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file or not output_file:
        messagebox.showwarning("Input Error", "Please specify input and output PDF files.")
        return

    for i in range(10000000000):  # From 0000000000 to 9999999999
        candidate_password = str(i).zfill(10)  # Pad with zeros to make it 10 digits
        if unlock_pdf(candidate_password, input_file, output_file):
            messagebox.showinfo("Success", f"Unlocked with password: {candidate_password}")
            return

    messagebox.showwarning("Failed", "Failed to unlock PDF with provided passwords.")

# Function to select input PDF file
def select_input_file():
    filename = filedialog.askopenfilename(title="Select Input PDF", filetypes=[("PDF files", "*.pdf")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, filename)

# Function to select output PDF file
def select_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", title="Select Output PDF", filetypes=[("PDF files", "*.pdf")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, filename)

# Create the main window
root = tk.Tk()
root.title("PDF Unlocker")

# Input for the PDF file
input_file_label = tk.Label(root, text="Input PDF File:")
input_file_label.pack()
input_file_entry = tk.Entry(root)
input_file_entry.pack()
input_file_button = tk.Button(root, text="Browse", command=select_input_file)
input_file_button.pack()

# Output for the PDF file
output_file_label = tk.Label(root, text="Output PDF File:")
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()
output_file_button = tk.Button(root, text="Browse", command=select_output_file)
output_file_button.pack()

# Start button
start_button = tk.Button(root, text="Unlock PDF", command=brute_force_unlock)
start_button.pack()

# Run the GUI event loop
root.mainloop()
