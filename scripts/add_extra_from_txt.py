import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from openai import OpenAI

# Initialize OpenAI client
def initialize_openai_client():
    """Initialize the OpenAI client using the API key from environment variables."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=openai_api_key)

client = initialize_openai_client()

def read_notes_from_txt(file_path):
    """Read notes from a .txt file and extract metadata and notes."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    metadata = lines[:3]  # Extract metadata (first 3 lines)
    notes = [
        {
            "index": idx,
            "note": {
                "Question": columns[0],
                "OP1": columns[1],
                "OP2": columns[2],
                "OP3": columns[3],
                "OP4": columns[4],
                "AnswerOptionNumber": columns[5],
                "Explanation": "",  # Placeholder for explanation
                "Tags": columns[7].split()
            }
        }
        for idx, line in enumerate(lines[3:], start=0)
        if len(columns := line.strip().split('\t')) >= 8  # Ensure enough columns
    ]
    return metadata, notes

def write_notes_to_txt(file_path, metadata, notes_data):
    """Write updated notes back to the .txt file, including explanations."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(metadata)  # Write metadata
        for note in sorted(notes_data, key=lambda x: x["index"]):  # Sort by index
            file.write(
                "\t".join([
                    note["note"]["Question"],
                    note["note"]["OP1"],
                    note["note"]["OP2"],
                    note["note"]["OP3"],
                    note["note"]["OP4"],
                    note["note"]["AnswerOptionNumber"],
                    note["note"]["Explanation"],  # Add explanation
                    " ".join(note["note"]["Tags"])  # Tags
                ]) + "\n"
            )

def fetch_explanation_from_openai(question, options, answer):
    """Fetch an explanation from OpenAI for the given question, options, and answer."""
    prompt = (
        "You are an expert educator who provides concise, clear, and accurate explanations. Be as concise as possible. "
        "Avoid unnecessary details, introductions, or disclaimers. "
        "Focus solely on explaining why the correct answer is valid and briefly mention why other options are incorrect (if relevant). "
        "Provide the explanation as plain text without any line breaks, bullet points, or structured formatting. "
        "Explain as briefly as possible.\n\n"
        f"Question: {question}\n"
        f"Option 1: {options[0]}\n"
        f"Option 2: {options[1]}\n"
        f"Option 3: {options[2]}\n"
        f"Option 4: {options[3]}\n"
        f"Answer: {options[answer - 1]}\n\n"
        "Explanation:"
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        explanation = completion.choices[0].message.content.strip()
        return explanation
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

def process_single_note(note):
    """Process a single note to fetch and add an explanation."""
    question = note["note"]["Question"]
    options = [note["note"][f"OP{i}"] for i in range(1, 5)]
    answer = int(note["note"]["AnswerOptionNumber"])
    
    # Fetch explanation from OpenAI
    explanation = fetch_explanation_from_openai(question, options, answer)
    if explanation:
        note["note"]["Explanation"] = explanation
    return note

def process_notes_in_batches(notes_data, batch_size=10, max_workers=6):
    """Process notes in parallel batches."""
    processed_notes = []
    with tqdm(total=len(notes_data), desc="Processing Notes") as pbar:
        for batch in [notes_data[i:i + batch_size] for i in range(0, len(notes_data), batch_size)]:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(process_single_note, note) for note in batch]
                for future in as_completed(futures):
                    processed_notes.append(future.result())
                    pbar.update(1)
            time.sleep(1.5)  # Delay between batches to avoid rate limits
    return processed_notes

def main():
    """Main function to process notes and update the .txt file with explanations."""
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    txt_dir = os.path.join(project_root, "txt")
    input_file = os.path.join(txt_dir, "Custom Study Session.txt")
    
    # Create a backup of the original file
    backup_file = os.path.join(txt_dir, "backup.txt")
    try:
        shutil.copy(input_file, backup_file)
        print(f"Backup created at: {backup_file}")
    except Exception as e:
        print(f"Failed to create backup: {e}")
        return
    
    # Read notes from the .txt file
    try:
        metadata, notes_data = read_notes_from_txt(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found. Please check the path and try again.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return
    
    # Process notes in parallel
    processed_notes = process_notes_in_batches(notes_data)
    
    # Write updated notes back to the original file
    write_notes_to_txt(input_file, metadata, processed_notes)
    print(f"Explanations have been added to '{input_file}'. Original file overwritten.")

if __name__ == "__main__":
    main()