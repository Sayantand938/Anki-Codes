# # prelims_tag_remover.py
# import os

# # Function to read notes from the .txt file
# def read_notes_from_txt(file_path):
#     """
#     Reads notes from the input file and extracts relevant data.
    
#     Args:
#         file_path (str): Absolute path to the input file.
    
#     Returns:
#         list: Extracted notes data.
#     """
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
    
#     # Skip the first 3 lines (metadata)
#     notes = lines[3:]
#     extracted_data = []
#     for line in notes:
#         columns = line.strip().split('\t')
#         if len(columns) < 8:  # Ensure there are enough columns
#             continue
#         question = columns[0]
#         op1 = columns[1]
#         op2 = columns[2]
#         op3 = columns[3]
#         op4 = columns[4]
#         answer_option_number = columns[5]
#         tags = columns[7].split()
#         extracted_data.append({
#             "Question": question,
#             "OP1": op1,
#             "OP2": op2,
#             "OP3": op3,
#             "OP4": op4,
#             "AnswerOptionNumber": answer_option_number,
#             "Tags": tags
#         })
#     return extracted_data

# # Function to clean tags (remove topic tags but keep Prelims and base subject tags)
# def clean_tags(tags):
#     """
#     Cleans tags by keeping only Prelims and base subject tags.
    
#     Args:
#         tags (list): List of tags for a note.
    
#     Returns:
#         list: Cleaned tags.
#     """
#     # Tags to preserve
#     preserved_tags = {"GK", "MATH", "GI", "ENG"}
#     cleaned_tags = []
#     for tag in tags:
#         # Keep Prelims tags (e.g., Prelims-1, Prelims-2, etc.)
#         if tag.startswith("Prelims-"):
#             cleaned_tags.append(tag)
#         # Keep base subject tags (GK, MATH, GI, ENG)
#         elif tag in preserved_tags:
#             cleaned_tags.append(tag)
    
#     return cleaned_tags

# # Function to write cleaned notes back to the original .txt file
# def write_cleaned_notes_to_txt(file_path, notes):
#     """
#     Writes cleaned notes back to the original .txt file.
    
#     Args:
#         file_path (str): Absolute path to the output file.
#         notes (list): Cleaned notes data.
#     """
#     with open(file_path, 'w', encoding='utf-8') as file:
#         # Write metadata (first 3 lines)
#         file.write("#separator:tab\n")
#         file.write("#html:true\n")
#         file.write("#tags column:8\n")
#         # Write cleaned notes
#         for note in notes:
#             line = "\t".join([
#                 note["Question"],
#                 note["OP1"],
#                 note["OP2"],
#                 note["OP3"],
#                 note["OP4"],
#                 note["AnswerOptionNumber"],
#                 "",  # Extra column (empty)
#                 " ".join(note["Tags"])  # Updated tags
#             ])
#             file.write(line + "\n")

# # Main processing function
# def main():
#     # Dynamically determine the base directory of the project
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Codes\Anki-Codes
    
#     # Construct the absolute path to the input/output file
#     input_file = os.path.join(base_dir, "txt", "Custom Study Session.txt")
    
#     # Read notes from the .txt file
#     notes_data = read_notes_from_txt(input_file)
#     if not notes_data:
#         print("No notes found in the file.")
#         return
    
#     # Clean tags for each note
#     for note in notes_data:
#         note["Tags"] = clean_tags(note["Tags"])
    
#     # Write cleaned notes back to the original .txt file
#     write_cleaned_notes_to_txt(input_file, notes_data)
    
#     print(f"Cleaned notes have been written back to '{input_file}'.")

# # Entry point of the script
# if __name__ == "__main__":
#     main()


import os
import shutil

# Function to read notes from the .txt file
def read_notes_from_txt(file_path):
    """
    Reads notes from the input file and extracts relevant data.
    
    Args:
        file_path (str): Absolute path to the input file.
    
    Returns:
        list: Extracted notes data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Skip the first 3 lines (metadata)
    notes = lines[3:]
    extracted_data = []
    for line in notes:
        columns = line.strip().split('\t')
        if len(columns) < 8:  # Ensure there are enough columns
            continue
        question = columns[0]
        op1 = columns[1]
        op2 = columns[2]
        op3 = columns[3]
        op4 = columns[4]
        answer_option_number = columns[5]
        tags = columns[7].split()
        extracted_data.append({
            "Question": question,
            "OP1": op1,
            "OP2": op2,
            "OP3": op3,
            "OP4": op4,
            "AnswerOptionNumber": answer_option_number,
            "Tags": tags
        })
    return extracted_data

# Function to clean tags (remove topic tags but keep Prelims and base subject tags)
def clean_tags(tags):
    """
    Cleans tags by keeping only Prelims and base subject tags.
    
    Args:
        tags (list): List of tags for a note.
    
    Returns:
        list: Cleaned tags.
    """
    # Tags to preserve
    preserved_tags = {"GK", "MATH", "GI", "ENG"}
    cleaned_tags = []
    for tag in tags:
        # Keep Prelims tags (e.g., Prelims-1, Prelims-2, etc.)
        if tag.startswith("Prelims-"):
            cleaned_tags.append(tag)
        # Keep base subject tags (GK, MATH, GI, ENG)
        elif tag in preserved_tags:
            cleaned_tags.append(tag)
    
    return cleaned_tags

# Function to write cleaned notes back to the original .txt file
def write_cleaned_notes_to_txt(file_path, notes):
    """
    Writes cleaned notes back to the original .txt file.
    
    Args:
        file_path (str): Absolute path to the output file.
        notes (list): Cleaned notes data.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write metadata (first 3 lines)
        file.write("#separator:tab\n")
        file.write("#html:true\n")
        file.write("#tags column:8\n")
        # Write cleaned notes
        for note in notes:
            line = "\t".join([
                note["Question"],
                note["OP1"],
                note["OP2"],
                note["OP3"],
                note["OP4"],
                note["AnswerOptionNumber"],
                "",  # Extra column (empty)
                " ".join(note["Tags"])  # Updated tags
            ])
            file.write(line + "\n")

# Function to create a backup of the file
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

# Main processing function
def main():
    # Dynamically determine the base directory of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:\Codes\Anki-Codes
    
    # Construct the absolute path to the input/output file
    input_file = os.path.join(base_dir, "txt", "Custom Study Session.txt")
    
    # Create a backup of the original file
    backup_file = create_backup(input_file)
    if not backup_file:
        return  # Exit if backup fails
    
    # Read notes from the .txt file
    notes_data = read_notes_from_txt(input_file)
    if not notes_data:
        print("No notes found in the file.")
        return
    
    # Clean tags for each note
    for note in notes_data:
        note["Tags"] = clean_tags(note["Tags"])
    
    # Write cleaned notes back to the original .txt file
    write_cleaned_notes_to_txt(input_file, notes_data)
    
    print(f"Cleaned notes have been written back to '{input_file}'.")

# Entry point of the script
if __name__ == "__main__":
    main()