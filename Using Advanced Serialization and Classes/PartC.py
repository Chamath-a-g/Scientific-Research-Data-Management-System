import os
import avro.schema
import avro.io
import io
import datetime

# Class to manage research data entries
class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.avro"
        self.schema = avro.schema.Parse(open("research_data_schema.avsc", "r").read())

    # Function to add a research data entry
    def add_entry(self):
        experiment_name = input("Enter the experiment name: ").strip()
        while not experiment_name:
            print("Experiment name cannot be blank.")
            experiment_name = input("Enter the experiment name: ").strip()

        date = input("Enter the date (YYYY-MM-DD): ").strip()
        while True:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                date = input("Enter the date (YYYY-MM-DD): ").strip()

        researcher = input("Enter the researcher's name: ").strip()
        while not researcher:
            print("Researcher's name cannot be blank.")
            researcher = input("Enter the researcher's name: ").strip()

        data_points_input = input("Enter data points (comma-separated): ").strip()
        while not data_points_input:
            print("Data points cannot be blank.")
            data_points_input = input("Enter data points (comma-separated): ").strip()

        try:
            data_points = [float(point) for point in data_points_input.split(',')]
            self.entries.append({
                'experiment_name': experiment_name,
                'date': date,
                'researcher': researcher,
                'data_points': data_points
            })
            print("Entry added successfully.")
        except ValueError:
            print("Invalid data points. Please enter numbers separated by commas.")

    # Function to view all research data entries
    def view_entries(self):
        if not self.entries:
            print("No entries found.")
        else:
            for i, entry in enumerate(self.entries, start=1):
                print(f"\nEntry {i}:")
                print(f"Experiment Name: {entry['experiment_name']}")
                print(f"Date: {entry['date']}")
                print(f"Researcher: {entry['researcher']}")
                print(f"Data Points: {entry['data_points']}")

    # Function to update a research data entry
    def update_entry(self):
        if not self.entries:
            print("No entries to update.")
            return

        self.view_entries()
        entry_index = int(input("Enter the entry number to update: ")) - 1
        if 0 <= entry_index < len(self.entries):
            experiment_name = input("Enter new experiment name (leave blank to keep current): ").strip()
            date = input("Enter new date (YYYY-MM-DD) (leave blank to keep current): ").strip()
            researcher = input("Enter new researcher's name (leave blank to keep current): ").strip()
            data_points_input = input("Enter new data points (comma-separated) (leave blank to keep current): ").strip()

            if experiment_name:
                self.entries[entry_index]['experiment_name'] = experiment_name
            if date:
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                    self.entries[entry_index]['date'] = date
                except ValueError:
                    print("Invalid date format. Keeping the current date.")
            if researcher:
                self.entries[entry_index]['researcher'] = researcher
            if data_points_input:
                try:
                    data_points = [float(point) for point in data_points_input.split(',')]
                    self.entries[entry_index]['data_points'] = data_points
                except ValueError:
                    print("Invalid data points. Keeping the current data points.")

            print("Entry updated successfully.")
        else:
            print("Invalid entry number.")

    # Function to delete a research data entry
    def delete_entry(self):
        if not self.entries:
            print("No entries to delete.")
            return

        self.view_entries()
        entry_index = int(input("Enter the entry number to delete: ")) - 1
        if 0 <= entry_index < len(self.entries):
            self.entries.pop(entry_index)
            print("Entry deleted successfully.")
        else:
            print("Invalid entry number.")

    # Function to save entries to a file
    def save_entries_to_file(self):
        with open(self.filename, 'wb') as file:
            writer = avro.io.DatumWriter(self.schema)
            buffer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(buffer)
            for entry in self.entries:
                writer.write(entry, encoder)
            file.write(buffer.getvalue())
        print("Entries saved to file successfully.")

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

    # Function to perform data analysis
    def analyze_data(self):
        if not self.entries:
            print("No entries found for analysis.")
            return

        entry_index = int(input("Enter the entry number to analyze: ")) - 1
        if 0 <= entry_index < len(self.entries):
            data_points = self.entries[entry_index]['data_points']
            if data_points:
                average = sum(data_points) / len(data_points)
                data_points.sort()
                median = data_points[len(data_points) // 2] if len(data_points) % 2 != 0 else (data_points[len(data_points) // 2 - 1] + data_points[len(data_points) // 2]) / 2
                variance = sum((x - average) ** 2 for x in data_points) / len(data_points)
                std_deviation = variance ** 0.5

                print(f"\nAnalysis for Entry {entry_index + 1}:")
                print(f"Average: {average}")
                print(f"Median: {median}")
                print(f"Standard Deviation: {std_deviation}")
            else:
                print("No data points available for analysis.")
        else:
            print("Invalid entry number.")

# Main function
def main():
    manager = ResearchDataManager()
    manager.load_entries_from_file()

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
            manager.add_entry()
        elif choice == '2':
            manager.view_entries()
        elif choice == '3':
            manager.update_entry()
        elif choice == '4':
            manager.delete_entry()
        elif choice == '5':
            manager.analyze_data()
        elif choice == '6':
            manager.save_entries_to_file()
        elif choice == '7':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
