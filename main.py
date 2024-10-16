import tkinter as tk
from tkinter import messagebox, filedialog
from unlock_pdf import unlock_pdf

def brute_force_unlock():
    input_file = input_file_entry.get()
    output_file_name = output_file_name_entry.get()
    output_file_path = output_file_path_entry.get()

    if not input_file or not output_file_name:
        messagebox.showwarning("Input Error", "Please specify input PDF file and output file name.")
        return

    output_file = output_file_path + output_file_name + ".pdf"

    try:
        start_range = int(start_range_entry.get())
        end_range = int(end_range_entry.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numbers for the password range.")
        return

    for i in range(start_range, end_range + 1):
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

# Input for output file name
output_file_name_label = tk.Label(root, text="Output File Name (without extension):")
output_file_name_label.pack()
output_file_name_entry = tk.Entry(root)
output_file_name_entry.pack()

# Input for output file path
output_file_path_label = tk.Label(root, text="Output File Path:")
output_file_path_label.pack()
output_file_path_entry = tk.Entry(root)
output_file_path_entry.pack()

# Input for password range
start_range_label = tk.Label(root, text="Start Password (e.g. 0000000000):")
start_range_label.pack()
start_range_entry = tk.Entry(root)
start_range_entry.pack()

end_range_label = tk.Label(root, text="End Password (e.g. 9999999999):")
end_range_label.pack()
end_range_entry = tk.Entry(root)
end_range_entry.pack()

# Start button
start_button = tk.Button(root, text="Unlock PDF", command=brute_force_unlock)
start_button.pack()

# Run the GUI event loop
root.mainloop()
