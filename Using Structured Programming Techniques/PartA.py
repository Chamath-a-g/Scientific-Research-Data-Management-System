import os
import datetime

# Function to add a research data entry
def add_entry(entries):
    while True:
        experiment_name = input("Enter the experiment name: ").strip()
        if experiment_name:
            break
        print("Experiment name cannot be blank. Please try again.")
    
    while True:
        date = input("Enter the date (YYYY-MM-DD): ").strip()
        if date:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        else:
            print("Date cannot be blank. Please try again.")
    
    while True:
        researcher = input("Enter the researcher's name: ").strip()
        if researcher:
            break
        print("Researcher's name cannot be blank. Please try again.")
    
    while True:
        data_points = input("Enter the data points (comma-separated): ").strip()
        if data_points:
            try:
                data_points = list(map(float, data_points.split(',')))
                break
            except ValueError:
                print("Invalid data points. Please enter numeric values separated by commas.")
        else:
            print("Data points cannot be blank. Please try again.")
    
    entry = {
        "experiment_name": experiment_name,
        "date": date,
        "researcher": researcher,
        "data_points": data_points
    }
    entries.append(entry)
    print("Entry added successfully.")

# Function to view all research data entries
def view_entries(entries):
    if not entries:
        print("No entries found.")
    else:
        for i, entry in enumerate(entries, start=1):
            print(f"\nEntry {i}:")
            print(f"Experiment Name: {entry['experiment_name']}")
            print(f"Date: {entry['date']}")
            print(f"Researcher: {entry['researcher']}")
            print(f"Data Points: {entry['data_points']}")

# Function to update a research data entry
def update_entry(entries):
    if not entries:
        print("No entries found to update.")
        return
    
    view_entries(entries)
    try:
        index = int(input("Enter the entry number you want to update: ")) - 1
        if index < 0 or index >= len(entries):
            print("Invalid entry number. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid entry number.")
        return
    
    while True:
        experiment_name = input("Enter the new experiment name (leave blank to keep current): ").strip()
        if experiment_name:
            entries[index]['experiment_name'] = experiment_name
            break
        print("Experiment name cannot be blank. Please try again.")
    
    while True:
        date = input("Enter the new date (YYYY-MM-DD, leave blank to keep current): ").strip()
        if date:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                entries[index]['date'] = date
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        else:
            break
    
    while True:
        researcher = input("Enter the new researcher's name (leave blank to keep current): ").strip()
        if researcher:
            entries[index]['researcher'] = researcher
            break
        print("Researcher's name cannot be blank. Please try again.")
    
    while True:
        data_points = input("Enter the new data points (comma-separated, leave blank to keep current): ").strip()
        if data_points:
            try:
                data_points = list(map(float, data_points.split(',')))
                entries[index]['data_points'] = data_points
                break
            except ValueError:
                print("Invalid data points. Please enter numeric values separated by commas.")
        else:
            break
    
    print("Entry updated successfully.")

# Function to delete a research data entry
def delete_entry(entries):
    if not entries:
        print("No entries found to delete.")
        return
    
    view_entries(entries)
    try:
        index = int(input("Enter the entry number you want to delete: ")) - 1
        if index < 0 or index >= len(entries):
            print("Invalid entry number. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid entry number.")
        return
    
    entries.pop(index)
    print("Entry deleted successfully.")

# Function to save entries to a text file
def save_entries_to_file(entries, filename):
    with open(filename, 'w') as file:
        for entry in entries:
            data_points = ','.join(map(str, entry['data_points']))
            file.write(f"{entry['experiment_name']},{entry['date']},{entry['researcher']},{data_points}\n")
    print(f"Entries saved to {filename}.")

# Function to load entries from a text file
def load_entries_from_file(filename):
    entries = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                experiment_name, date, researcher, data_points = line.strip().split('|')
                data_points = list(map(float, data_points.split(',')))
                entry = {
                    "experiment_name": experiment_name,
                    "date": date,
                    "researcher": researcher,
                    "data_points": data_points
                }
                entries.append(entry)
    return entries

# Function to calculate the average of a list of numbers
def calculate_average(data_points):
    return sum(data_points) / len(data_points)

# Function to calculate the standard deviation of a list of numbers
def calculate_stddev(data_points):
    mean = calculate_average(data_points)
    variance = sum((x - mean) ** 2 for x in data_points) / len(data_points)
    
    # Manual square root calculation (Newton's method)
    guess = variance / 2.0
    tolerance = 1e-10
    while abs(guess * guess - variance) > tolerance:
        guess = (guess + variance / guess) / 2.0
    
    return guess

# Function to calculate the median of a list of numbers
def calculate_median(data_points):
    sorted_points = sorted(data_points)
    n = len(sorted_points)
    if n % 2 == 0:
        median = (sorted_points[n//2 - 1] + sorted_points[n//2]) / 2
    else:
        median = sorted_points[n//2]
    return median

# Function to perform data analysis
def analyze_data(entries):
    if not entries:
        print("No entries found.")
        return
    
    for i, entry in enumerate(entries, start=1):
        data_points = entry['data_points']
        average = calculate_average(data_points)
        stddev = calculate_stddev(data_points)
        median = calculate_median(data_points)
        
        print(f"\nAnalysis for Entry {i}:")
        print(f"Experiment Name: {entry['experiment_name']}")
        print(f"Average: {average}")
        print(f"Standard Deviation: {stddev}")
        print(f"Median: {median}")

# Main function
def main():
    filename = "research_data.txt"
    entries = load_entries_from_file(filename)
    
    while True:
        print("\nMenu:")
        print("1. Add a research data entry")
        print("2. View all entries")
        print("3. Update an entry")
        print("4. Delete an entry")
        print("5. Analyze data")
        print("6. Save entries to file")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            add_entry(entries)
        elif choice == '2':
            view_entries(entries)
        elif choice == '3':
            update_entry(entries)
        elif choice == '4':
            delete_entry(entries)
        elif choice == '5':
            analyze_data(entries)
        elif choice == '6':
            save_entries_to_file(entries, filename)
        elif choice == '7':
            save_entries_to_file(entries, filename)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
