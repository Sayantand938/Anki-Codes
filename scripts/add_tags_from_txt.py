# add_tags_from_txt.py
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from openai import OpenAI

# Predefined tag lists
TAG_LISTS = {
    "ENG": [
        "Spot-Error", "Sentence-Improvement", "Narration", "Voice-Change",
        "Parajumble", "Fill-Blanks", "Cloze-Test", "Comprehension",
        "One-Word-Substitution", "Synonym", "Antonym", "Homonym", "Idioms", "Spelling-Check", "Undefined"
    ],
    "MATH": [
        "Number-Systems", "Simple-Interest", "HCF-LCM", "Ratio", "Discount",
        "Time-Distance", "Profit-Loss", "Percentage", "Mixture", "Pipe-Cistern",
        "Height-Distance", "Compound-Interest", "Time-Work", "Average", "Boat-Stream",
        "Statistics", "Data-Interpretation", "Mensuration", "Trigonometry", "Geometry",
        "Simplification", "Algebra", "Probability", "Undefined"
    ],
    "GI": [
        "Analogy", "Odd-One-Out", "Coding-Decoding", "Series", "Missing-Numbers",
        "Statement-And-Conclusion", "Blood-Relation", "Venn-Diagram", "Dice",
        "Sitting-Arrangements", "Direction", "Mathematical-Operations", "Word-Arrangement",
        "Age", "Calendar", "Figure-Counting", "Paper-Cut", "Embedded-Figure", "Mirror-Image",
        "Undefined"
    ],
    "GK": [
        "History", "Geography", "Polity", "Economics", "Science",
        "Current-Affairs", "Static", "Undefined"
    ]
}

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
                "Tags": columns[7].split()
            }
        }
        for idx, line in enumerate(lines[3:], start=0)
        if len(columns := line.strip().split('\t')) >= 8  # Ensure enough columns
    ]
    return metadata, notes

def write_notes_to_txt(file_path, metadata, notes_data):
    """Write updated notes back to the .txt file."""
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
                    "",  # Extra column (empty)
                    " ".join(note["note"]["Tags"])  # Updated tags
                ]) + "\n"
            )

def fetch_tag_from_openai(prompt, tag_list):
    """Fetch a tag from OpenAI's GPT-4 API."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert tagger who provides a single concise and relevant tag for questions. "
                        "Choose ONLY ONE tag from the provided list that best describes the topic or category of the question. "
                        "Avoid unnecessary details or explanations."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        tag = completion.choices[0].message.content.strip()
        return tag if tag in tag_list else None
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

def build_prompt(question, options, answer, tag_list, additional_instructions):
    """Build the prompt for OpenAI based on the question and additional instructions."""
    return (
        f"Question: {question}\n"
        f"Option 1: {options[0]}\n"
        f"Option 2: {options[1]}\n"
        f"Option 3: {options[2]}\n"
        f"Option 4: {options[3]}\n"
        f"Answer: {answer}\n"
        f"Prompt: Provide a single relevant tag for this question. Choose ONLY ONE tag from the following list:\n"
        f"Additional Instructions: {additional_instructions}"
        f"Valid Tag List: {', '.join(tag_list)}\n"
        f"Output Format: <single tag>"
    )

def get_additional_instructions(existing_tags):
    """Generate additional instructions based on existing tags."""
    additional_instructions = ""
    if "ENG" in existing_tags:
        additional_instructions += "If the question has multiple blank lines, then tag it as Cloze-Test.\n"
    if "MATH" in existing_tags:
        additional_instructions += "If the question has some table/chart, then tag it as Data-Interpretation.\n"
    if "GK" in existing_tags:
        additional_instructions += (
            "If a question is about dance or culture, tag it as Static.\n"
            "If a question concerns an event from the last 10 years, tag it as Current-Affairs.\n"
            "Use the History tag only for questions that are genuinely about history.\n"
            "Use the Static tag for General Knowledge questions about facts that don’t change over time.\n"
            "Use the Current-Affairs tag if a question is about sports.\n"
        )
    return additional_instructions

def process_single_note(note, tag_lists):
    """Process a single note to fetch and add a relevant tag."""
    # Skip notes with more than 2 tags
    if len(note["note"]["Tags"]) > 2:
        return note
    
    question = note["note"]["Question"]
    options = [note["note"][f"OP{i}"] for i in range(1, 5)]
    answer = note["note"]["AnswerOptionNumber"]
    existing_tags = note["note"]["Tags"]
    
    # Determine the tag list based on existing tags
    tag_list = next((predefined_tags for base_tag, predefined_tags in tag_lists.items() if base_tag in existing_tags), None)
    if not tag_list:
        return note  # Skip notes without a valid tag list
    
    # Dynamically adjust the prompt based on existing tags
    additional_instructions = get_additional_instructions(existing_tags)
    
    # Create the prompt
    prompt_text = build_prompt(question, options, answer, tag_list, additional_instructions)
    
    # Fetch the tag from OpenAI
    tag = fetch_tag_from_openai(prompt_text, tag_list)
    if tag:
        note["note"]["Tags"].append(tag)  # Add the new tag to the existing tags
    return note

def process_notes_in_batches(notes_data, tag_lists, batch_size=10, max_workers=6):
    """Process notes in parallel batches."""
    processed_notes = []
    with tqdm(total=len(notes_data), desc="Processing Notes") as pbar:
        for batch in [notes_data[i:i + batch_size] for i in range(0, len(notes_data), batch_size)]:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(process_single_note, note, tag_lists) for note in batch]
                for future in as_completed(futures):
                    processed_notes.append(future.result())
                    pbar.update(1)
            time.sleep(1.5)  # Delay between batches
    return processed_notes

def main():
    """Main function to process notes and update the .txt file."""
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
    processed_notes = process_notes_in_batches(notes_data, TAG_LISTS)
    
    # Write updated notes back to the original file
    write_notes_to_txt(input_file, metadata, processed_notes)
    print(f"Tagged notes have been written to '{input_file}'. Original file overwritten.")

if __name__ == "__main__":
    main()