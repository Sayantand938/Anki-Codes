# prelims_tag_counter.py
from rich.table import Table
from rich.console import Console
from rich.style import Style
import os

# Function to process the file and generate the table
def process_file_and_generate_table(file_path):
    """
    Processes the input file to count tags starting with "Prelims" and generates a table.
    
    Args:
        file_path (str): Absolute path to the input file.
    """
    # Dictionary to store tag counts
    tag_counts = {}
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Skip the first 3 lines (metadata) and process the rest
    for line in lines[3:]:
        # Split the line into columns (TSV format)
        columns = line.strip().split('\t')
        
        # Extract the Tags column (8th column, index 7)
        tags = columns[7].split() if len(columns) > 7 else []
        
        # Filter tags that start with "Prelims"
        for tag in tags:
            if tag.startswith("Prelims"):
                # Increment the count for this tag
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Create a Rich table
    table = Table(title="Tag Statistics", style="white")
    table.add_column("Tag", justify="left", style="white", no_wrap=True)
    table.add_column("No of Notes", justify="right", style="white")
    
    # Add rows to the table with conditional styling
    for tag, count in sorted(tag_counts.items()):  # Sort tags alphabetically
        style = Style(color="green" if count == 25 else "red")
        table.add_row(tag, str(count), style=style)
    
    # Display the table
    console = Console()
    console.print(table)

# Dynamically determine the base directory of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Codes\Anki-Codes

# Construct the absolute path to the input file
file_path = os.path.join(base_dir, "txt", "Custom Study Session.txt")

# Process the file and generate the table
process_file_and_generate_table(file_path)