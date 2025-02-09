import tkinter as tk
from tkinter import ttk, messagebox
import avro.schema
import avro.io
import io
import os
import datetime

# Class to manage research data entries
class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.avro"
        self.schema = avro.schema.Parse(open("research_data_schema.avsc", "r").read())
        self.load_entries_from_file()

    # Function to add a research data entry
    def add_entry(self, experiment_name, date, researcher, data_points):
        self.entries.append({
            'experiment_name': experiment_name,
            'date': date,
            'researcher': researcher,
            'data_points': data_points
        })

    # Function to update a research data entry
    def update_entry(self, index, experiment_name, date, researcher, data_points):
        if 0 <= index < len(self.entries):
            self.entries[index] = {
                'experiment_name': experiment_name,
                'date': date,
                'researcher': researcher,
                'data_points': data_points
            }

    # Function to delete a research data entry
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]

    def get_entries(self):
        return self.entries

    # Function to save entries to a file
    def save_entries_to_file(self):
        with open(self.filename, 'wb') as file:
            writer = avro.io.DatumWriter(self.schema)
            buffer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(buffer)
            for entry in self.entries:
                writer.write(entry, encoder)
            file.write(buffer.getvalue())

    # Function to load entries from a file
    def load_entries_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                buffer = io.BytesIO(file.read())
                decoder = avro.io.BinaryDecoder(buffer)
                reader = avro.io.DatumReader(self.schema)
                
                self.entries = []
                while buffer.tell() < len(buffer.getvalue()):
                    entry = reader.read(decoder)
                    self.entries.append(entry)

    def calculate_average(self, data_points):
        if not data_points:
            return None
        return sum(data_points) / len(data_points)

    def calculate_standard_deviation(self, data_points):
        if not data_points:
            return None
        mean = self.calculate_average(data_points)
        variance = sum((x - mean) ** 2 for x in data_points) / len(data_points)
        return variance ** 0.5

    def calculate_median(self, data_points):
        if not data_points:
            return None
        sorted_points = sorted(data_points)
        n = len(sorted_points)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_points[mid - 1] + sorted_points[mid]) / 2.0
        else:
            return sorted_points[mid]

# Function to validate user input before adding or updating an entry
def validate_input(experiment_name, date, researcher, data_points):
    if not experiment_name:
        return "Experiment name cannot be empty."
    if not date:
        return "Date cannot be empty."
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "Date must be in the format YYYY-MM-DD."
    if not researcher:
        return "Researcher name cannot be empty."
    try:
        list(map(float, data_points.split(',')))
    except ValueError:
        return "Data points must be a comma-separated list of numbers."
    return None

# Function to handle adding a new entry
def add_entry(manager, tree):
    def submit():
        experiment_name = experiment_name_var.get().strip()
        date = date_var.get().strip()
        researcher = researcher_var.get().strip()
        data_points = data_points_var.get().strip()

        error_message = validate_input(experiment_name, date, researcher, data_points)
        if error_message:
            messagebox.showerror("Input Error", error_message)
            return

        manager.add_entry(experiment_name, date, researcher, list(map(float, data_points.split(','))))
        manager.save_entries_to_file()
        refresh_table(manager, tree)
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Research Entry")

    tk.Label(add_window, text="Experiment Name:").grid(row=0, column=0, padx=10, pady=5)
    experiment_name_var = tk.StringVar()
    tk.Entry(add_window, textvariable=experiment_name_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
    date_var = tk.StringVar()
    tk.Entry(add_window, textvariable=date_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Researcher:").grid(row=2, column=0, padx=10, pady=5)
    researcher_var = tk.StringVar()
    tk.Entry(add_window, textvariable=researcher_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Data Points (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
    data_points_var = tk.StringVar()
    tk.Entry(add_window, textvariable=data_points_var).grid(row=3, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

# Function to handle updating an existing entry
def update_entry(manager, tree):
    selected_item = tree.selection()
    if not selected_item:
        return

    item_index = tree.index(selected_item[0])
    entry = manager.get_entries()[item_index]

    def submit():
        experiment_name = experiment_name_var.get().strip()
        date = date_var.get().strip()
        researcher = researcher_var.get().strip()
        data_points = data_points_var.get().strip()

        error_message = validate_input(experiment_name, date, researcher, data_points)
        if error_message:
            messagebox.showerror("Input Error", error_message)
            return

        manager.update_entry(item_index, experiment_name, date, researcher, list(map(float, data_points.split(','))))
        manager.save_entries_to_file()
        refresh_table(manager, tree)
        update_window.destroy()

    update_window = tk.Toplevel()
    update_window.title("Update Research Entry")

    tk.Label(update_window, text="Experiment Name:").grid(row=0, column=0, padx=10, pady=5)
    experiment_name_var = tk.StringVar(value=entry['experiment_name'])
    tk.Entry(update_window, textvariable=experiment_name_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
    date_var = tk.StringVar(value=entry['date'])
    tk.Entry(update_window, textvariable=date_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Researcher:").grid(row=2, column=0, padx=10, pady=5)
    researcher_var = tk.StringVar(value=entry['researcher'])
    tk.Entry(update_window, textvariable=researcher_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(update_window, text="Data Points (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
    data_points_var = tk.StringVar(value=','.join(map(str, entry['data_points'])))
    tk.Entry(update_window, textvariable=data_points_var).grid(row=3, column=1, padx=10, pady=5)

    tk.Button(update_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

# Function to handle deleting an entry
def delete_entry(manager, tree):
    selected_item = tree.selection()
    if not selected_item:
        return

    item_index = tree.index(selected_item[0])
    manager.delete_entry(item_index)
    manager.save_entries_to_file()
    refresh_table(manager, tree)

# Function to refresh the table
def refresh_table(manager, tree):
    for i in tree.get_children():
        tree.delete(i)
    for entry in manager.get_entries():
        tree.insert('', 'end', values=(entry['experiment_name'], entry['date'], entry['researcher'], ','.join(map(str, entry['data_points']))))

# Function to sort the table
def sort_by_column(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)
    tree.heading(col, command=lambda: sort_by_column(tree, col, not descending))

# Function to analyze the entries
def analyze_entry(manager, tree):
    selected_item = tree.selection()
    if not selected_item:
        return

    item_index = tree.index(selected_item[0])
    entry = manager.get_entries()[item_index]
    data_points = entry['data_points']

    if not data_points:
        messagebox.showinfo("Analysis", "No data points available for analysis.")
        return

    average = manager.calculate_average(data_points)
    std_dev = manager.calculate_standard_deviation(data_points)
    median = manager.calculate_median(data_points)

    analysis_message = (
        f"Analysis of {entry['experiment_name']}:\n\n"
        f"Average: {average:.2f}\n"
        f"Standard Deviation: {std_dev:.2f}\n"
        f"Median: {median:.2f}"
    )
    messagebox.showinfo("Analysis Results", analysis_message)

# Main function
def main():
    manager = ResearchDataManager()

    root = tk.Tk()
    root.title("Research Data Manager")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    search_var = tk.StringVar()
    tk.Label(frame, text="Search:").pack(side=tk.LEFT)
    tk.Entry(frame, textvariable=search_var).pack(side=tk.LEFT, padx=10)

    tree = ttk.Treeview(frame, columns=("Experiment", "Date", "Researcher", "Data Points"), show="headings")
    tree.heading("Experiment", text="Experiment", command=lambda: sort_by_column(tree, "Experiment", False))
    tree.heading("Date", text="Date", command=lambda: sort_by_column(tree, "Date", False))
    tree.heading("Researcher", text="Researcher", command=lambda: sort_by_column(tree, "Researcher", False))
    tree.heading("Data Points", text="Data Points", command=lambda: sort_by_column(tree, "Data Points", False))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def search(*args):
        query = search_var.get().strip().lower()
        for i in tree.get_children():
            tree.delete(i)
        for entry in manager.get_entries():
            if query in entry['experiment_name'].lower() or query in entry['date'].lower() or query in entry['researcher'].lower():
                tree.insert('', 'end', values=(entry['experiment_name'], entry['date'], entry['researcher'], ','.join(map(str, entry['data_points']))))

    search_var.trace('w', search)
    
    tk.Button(root, text="Add Entry", command=lambda: add_entry(manager, tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Update Entry", command=lambda: update_entry(manager, tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Delete Entry", command=lambda: delete_entry(manager, tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Analyze Entry", command=lambda: analyze_entry(manager, tree)).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Refresh", command=lambda: refresh_table(manager, tree)).pack(side=tk.LEFT, padx=10)

    refresh_table(manager, tree)

    root.mainloop()

if __name__ == "__main__":
    main()
