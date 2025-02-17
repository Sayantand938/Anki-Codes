import requests
from tqdm import tqdm
from add_extra_openai_module import process_with_openai 
from add_extra_gemini_module import process_with_gemini

# Define AnkiConnect API URL
anki_connect_url = "http://localhost:8765"

# Function to fetch note IDs from the filtered deck
def fetch_note_ids():
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": "deck:\"Custom Study Session\""
        }
    }
    response = requests.post(anki_connect_url, json=payload)
    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        print("Error: Unable to fetch note IDs")
        return []

# Function to fetch detailed note information using notesInfo
def fetch_notes_info(note_ids):
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post(anki_connect_url, json=payload)
    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        print("Error: Unable to fetch notes info")
        return []

# Function to extract required fields and filter out notes with non-empty Extra fields
def extract_notes_data(notes_info):
    extracted_data = []
    for note in notes_info:
        note_id = note.get("noteId")
        fields = note.get("fields", {})
        
        question = fields.get("Question", {}).get("value", "")
        op1 = fields.get("OP1", {}).get("value", "")
        op2 = fields.get("OP2", {}).get("value", "")
        op3 = fields.get("OP3", {}).get("value", "")
        op4 = fields.get("OP4", {}).get("value", "")
        answer_option_number = fields.get("Answer", {}).get("value", "")
        extra = fields.get("Extra", {}).get("value", "")  # Get the Extra field value
        
        # Skip notes with non-empty Extra fields
        if extra.strip():  # Check if Extra field is not empty
            continue
        
        options = [op1, op2, op3, op4]
        try:
            answer_index = int(answer_option_number) - 1
            answer = options[answer_index] if 0 <= answer_index < len(options) else ""
        except (ValueError, IndexError):
            answer = ""
        
        extracted_data.append({
            "noteId": note_id,
            "Question": question,
            "OP1": op1,
            "OP2": op2,
            "OP3": op3,
            "OP4": op4,
            "Answer": answer
        })
    return extracted_data

# Function to update the 'Extra' field of a note with the explanation
def update_note_with_explanation(note_id, explanation):
    payload = {
        "action": "updateNote",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    "Extra": explanation  # Update the 'Extra' field with the explanation
                }
            }
        }
    }
    response = requests.post(anki_connect_url, json=payload)
    return response.status_code == 200  # Return True if successful, False otherwise

# Main processing function
def process_notes(json_data):
    total_notes_to_process = len(json_data)
    if total_notes_to_process == 0:
        print("All notes already have explanations in their Extra fields. Nothing to process.")
        return
    print(f"Processing {total_notes_to_process} notes...")
    for item in tqdm(json_data, desc="Progress", unit="note"):
        note_id = item["noteId"]
        note_details = {
            "Question": item["Question"],
            "OP1": item["OP1"],
            "OP2": item["OP2"],
            "OP3": item["OP3"],
            "OP4": item["OP4"],
            "Answer": item["Answer"]
        }
        # SWITCH THIS
        explanation = process_with_openai(note_details)
        # explanation = process_with_gemini(note_details)
        if explanation:
            # Update the note's 'Extra' field with the explanation
            update_note_with_explanation(note_id, explanation)

# Entry point of the script
if __name__ == "__main__":
    # Step 1: Fetch note IDs
    note_ids = fetch_note_ids()
    if not note_ids:
        print("No notes found in the 'Custom Study Session' filtered deck.")
        exit()
    
    # Step 2: Fetch detailed note information
    notes_info = fetch_notes_info(note_ids)
    if not notes_info:
        print("No notes info found.")
        exit()
    
    # Step 3: Extract fields and filter out notes with non-empty Extra fields
    json_data = extract_notes_data(notes_info)
    
    # Step 4: Process notes
    process_notes(json_data)