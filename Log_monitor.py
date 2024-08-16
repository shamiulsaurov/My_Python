import os
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_directory():
    directory = filedialog.askdirectory()
    log_directory_entry.delete(0, tk.END)
    log_directory_entry.insert(0, directory)

def monitor_logs():
    log_directory = log_directory_entry.get().strip()
    search_term = search_term_entry.get().strip()

    if not log_directory:
        messagebox.showwarning("Input Error", "Please provide the log directory.")
        return

    if not search_term:
        messagebox.showwarning("Input Error", "Please provide a search term.")
        return

    errors_found = False
    log_text.delete(1.0, tk.END)  # Clear previous results
    
    # Search for all .log files in the directory
    for file_name in os.listdir(log_directory):
        if file_name.endswith('.log'):
            file_path = os.path.join(log_directory, file_name)
            
            try:
                # Open the file with a specified encoding and handle errors
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    for line in file:
                        if search_term in line:
                            # Determine color based on log type
                            if "ERROR" in line:
                                color = 'error'
                            elif "DEBUG" in line:
                                color = 'debug'
                            elif "INFO" in line:
                                color = 'info'
                            else:
                                color = None
                            
                            # Insert the highlighted file name in bold yellow
                            log_text.insert(tk.END, f"{file_name}: ", ('filename',))
                            
                            # Insert the log content with corresponding color
                            log_text.insert(tk.END, f"{line.strip()}\n", (color,))
                            errors_found = True
            
            except FileNotFoundError:
                messagebox.showerror("File Not Found", f"Log file {file_path} not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    if not errors_found:
        messagebox.showinfo("No Results", f"No occurrences of '{search_term}' found in the log files.")

def close_application():
    root.quit()  # Closes the application

# Create the main window
root = tk.Tk()
root.title("Log Monitor")

# Set full-screen mode
root.attributes('-fullscreen', True)

# Configure grid layout to expand widgets
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create a label and entry for log directory
log_directory_label = tk.Label(root, text="Log Directory:", bg="black", fg="white")
log_directory_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

log_directory_entry = tk.Entry(root, width=70)
log_directory_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

browse_directory_button = tk.Button(root, text="Browse", command=browse_directory)
browse_directory_button.grid(row=0, column=2, padx=10, pady=5)

# Create a label and entry for search term
search_term_label = tk.Label(root, text="Search Term:", bg="black", fg="white")
search_term_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

search_term_entry = tk.Entry(root, width=70)
search_term_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Create a button to start monitoring the logs
monitor_button = tk.Button(root, text="Monitor Logs", command=monitor_logs)
monitor_button.grid(row=2, columnspan=3, padx=10, pady=10)

# Create a Text widget to display errors found
log_text = tk.Text(root, width=100, height=30, bg="black", fg="white", wrap="word")
log_text.grid(row=3, columnspan=3, padx=10, pady=10, sticky="nsew")

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(root, command=log_text.yview)
scrollbar.grid(row=3, column=3, sticky="ns")
log_text.config(yscrollcommand=scrollbar.set)

# Configure text tags for coloring
log_text.tag_configure('error', foreground='light coral')
log_text.tag_configure('debug', foreground='light yellow')
log_text.tag_configure('info', foreground='light blue')
log_text.tag_configure('filename', foreground='yellow', font=('Helvetica', 10, 'bold'))  # File name styling

# Create a button to close the application
close_button = tk.Button(root, text="Close Application", command=close_application)
close_button.grid(row=4, columnspan=3, padx=10, pady=10)

# Add owner information at the bottom
owner_info_label = tk.Label(root, text="Prepared By: Shamiul Saurov | Version: 0.1", bg="black", fg="white")
owner_info_label.grid(row=5, columnspan=3, pady=10)

# Run the application
root.mainloop()
