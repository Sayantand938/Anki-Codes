# # prelims_notes_organizer.py
# import os
# from collections import defaultdict

# def organize_notes(file_path):
#     """
#     Organizes notes in the input file by sorting them based on their Prelims tag numbers.
    
#     Args:
#         file_path (str): Absolute path to the input/output file.
#     """
#     # Read the file
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
    
#     # Extract metadata (first 3 lines)
#     metadata = lines[:3]
    
#     # Extract notes (remaining lines)
#     notes = lines[3:]
    
#     # Function to extract the Prelims tag number from a note
#     def get_prelims_tag_number(note):
#         columns = note.strip().split('\t')
#         if len(columns) > 7:  # Ensure the Tags column exists
#             tags = columns[7].split()
#             for tag in tags:
#                 if tag.startswith("Prelims-"):
#                     try:
#                         return int(tag.split("-")[1])  # Extract the number after "Prelims-"
#                     except (IndexError, ValueError):
#                         pass
#         return float('inf')  # If no valid Prelims tag is found, place it at the end
    
#     # Group notes by their Prelims tag number
#     prelims_groups = defaultdict(list)
#     for note in notes:
#         prelims_tag_number = get_prelims_tag_number(note)
#         prelims_groups[prelims_tag_number].append(note)
    
#     # Sort the groups by Prelims tag number
#     sorted_groups = sorted(prelims_groups.items(), key=lambda x: x[0])
    
#     # Combine the sorted groups into a single list of notes
#     sorted_notes = []
#     for _, group_notes in sorted_groups:
#         sorted_notes.extend(group_notes)  # Preserve the original order within each group
    
#     # Write the organized notes back to the file
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.writelines(metadata)  # Write metadata first
#         file.writelines(sorted_notes)  # Write sorted notes
    
#     print(f"Notes in '{file_path}' have been organized successfully!")

# # Dynamically determine the base directory of the project
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Codes\Anki-Codes

# # Construct the absolute path to the input/output file
# file_path = os.path.join(base_dir, "txt", "Custom Study Session.txt")

# # Organize the notes
# organize_notes(file_path)


import os
import shutil
from collections import defaultdict

def create_backup(file_path):
    """
    Creates a backup of the file by copying it to a backup file.
    
    Args:
        file_path (str): Absolute path to the file to back up.
    
    Returns:
        str: Path to the backup file.
    """
    backup_file = os.path.join(os.path.dirname(file_path), "backup.txt")
    try:
        shutil.copy(file_path, backup_file)
        print(f"Backup created at: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Failed to create backup: {e}")
        return None

def organize_notes(file_path):
    """
    Organizes notes in the input file by sorting them based on their Prelims tag numbers.
    
    Args:
        file_path (str): Absolute path to the input/output file.
    """
    # Create a backup of the original file
    backup_file = create_backup(file_path)
    if not backup_file:
        return  # Exit if backup fails
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Extract metadata (first 3 lines)
    metadata = lines[:3]
    
    # Extract notes (remaining lines)
    notes = lines[3:]
    
    # Function to extract the Prelims tag number from a note
    def get_prelims_tag_number(note):
        columns = note.strip().split('\t')
        if len(columns) > 7:  # Ensure the Tags column exists
            tags = columns[7].split()
            for tag in tags:
                if tag.startswith("Prelims-"):
                    try:
                        return int(tag.split("-")[1])  # Extract the number after "Prelims-"
                    except (IndexError, ValueError):
                        pass
        return float('inf')  # If no valid Prelims tag is found, place it at the end
    
    # Group notes by their Prelims tag number
    prelims_groups = defaultdict(list)
    for note in notes:
        prelims_tag_number = get_prelims_tag_number(note)
        prelims_groups[prelims_tag_number].append(note)
    
    # Sort the groups by Prelims tag number
    sorted_groups = sorted(prelims_groups.items(), key=lambda x: x[0])
    
    # Combine the sorted groups into a single list of notes
    sorted_notes = []
    for _, group_notes in sorted_groups:
        sorted_notes.extend(group_notes)  # Preserve the original order within each group
    
    # Write the organized notes back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(metadata)  # Write metadata first
        file.writelines(sorted_notes)  # Write sorted notes
    
    print(f"Notes in '{file_path}' have been organized successfully!")

# Dynamically determine the base directory of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Codes\Anki-Codes

# Construct the absolute path to the input/output file
file_path = os.path.join(base_dir, "txt", "Custom Study Session.txt")

# Organize the notes
organize_notes(file_path)