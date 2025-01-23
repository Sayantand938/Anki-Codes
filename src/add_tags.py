import os
import requests
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Define the AnkiConnect server URL
ANKI_CONNECT_URL = 'http://localhost:8765'

# Define valid tag lists
valid_tags_eng = [
    "Spot-Error", "Sentence-Improvement", "Narration", "Voice-Change",
    "Parajumble", "Fill-Blanks", "Cloze-Test", "Comprehension",
    "One-Word-Substitution", "Synonym", "Antonym", "Homonym", "Idioms", "Spelling-Check", "Undefined"
]

valid_tags_math = [
    "Number-Systems", "Simple-Interest", "HCF-LCM", "Ratio", "Discount",
    "Time-Distance", "Profit-Loss", "Percentage", "Mixture", "Pipe-Cistern",
    "Height-Distance", "Compound-Interest", "Time-Work", "Average", "Boat-Stream",
    "Statistics", "Data-Interpretation", "Mensuration", "Trigonometry", "Geometry",
    "Simplification", "Algebra", "Probability", "Undefined"
]

valid_tags_gi = [
    "Analogy", "Odd-One-Out", "Coding-Decoding", "Series", "Missing-Numbers",
    "Statement-And-Conclusion", "Blood-Relation", "Venn-Diagram", "Dice",
    "Sitting-Arrangements", "Direction", "Mathematical-Operations", "Word-Arrangement",
    "Age", "Calendar", "Figure-Counting", "Paper-Cut", "Embedded-Figure", "Mirror-Image",
    "Undefined"
]

valid_tags_gk = [
    "History", "Geography", "Polity", "Economics", "Science",
    "Current-Affairs", "Static", "Undefined"
]

def get_note_ids(deck_name):
    """Fetch note IDs for a given deck."""
    payload = {
        'action': 'findNotes',
        'version': 6,
        'params': {'query': f'deck:"{deck_name}"'}
    }
    return send_anki_request(payload)

def get_notes_info(note_ids):
    """Fetch detailed note information using note IDs."""
    payload = {
        'action': 'notesInfo',
        'version': 6,
        'params': {'notes': note_ids}
    }
    return send_anki_request(payload)

def send_anki_request(payload):
    """Send a request to AnkiConnect and return the response."""
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response.raise_for_status()
        return response.json().get('result', [])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
        return []

def select_valid_tags(existing_tags):
    """Select the appropriate tag list based on existing tags."""
    if 'ENG' in existing_tags:
        return valid_tags_eng
    elif 'MATH' in existing_tags:
        return valid_tags_math
    elif 'GI' in existing_tags:
        return valid_tags_gi
    elif 'GK' in existing_tags:
        return valid_tags_gk
    else:
        return []

def get_openai_explanation(question, options, correct_option_index, valid_tags, existing_tags):
    """Fetch explanation and appropriate tag using OpenAI API."""
    correct_answer = options[correct_option_index]

    # Base prompt
    prompt = f"""
    Question: {question}
    Options:
      1: {options[0]}
      2: {options[1]}
      3: {options[2]}
      4: {options[3]}
    Correct Answer: {correct_answer}

    Choose the single best tag from the given tag list for this Question and output the tag in this format: {{}}

    Tag List:
    {valid_tags}
    """

    # Modify the prompt based on existing tags
    if 'ENG' in existing_tags:
        prompt += "\nIf there are multiple blanks in the question, then Cloze-Test should be the appropriate tag rather than Fill-Blanks."
    elif 'MATH' in existing_tags:
        prompt += "\nIf any question has a table or chart, then tag it as Data-Interpretation."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI model trained to classify questions."},
                {"role": "user", "content": prompt}
            ]
        )
        explanation = completion.choices[0].message.content
        return explanation
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Unable to fetch explanation"

def process_notes(notes_info, queue):
    """Process notes and add to queue, skip if there are 3 or more tags."""
    for index, note in enumerate(notes_info):
        tags = note.get('tags', [])
        
        # Process only if the note has less than 3 tags
        if len(tags) >= 3:
            print(f"Note {index + 1} ({note['noteId']}) skipped")
            continue

        fields = note['fields']
        question = fields.get('Question', {}).get('value', '')
        options = [fields.get(f'OP{i+1}', {}).get('value', '') for i in range(4)]
        correct_option_index = int(fields.get('Answer', {}).get('value', '0')) - 1
        
        valid_tags = select_valid_tags(tags)
        extra = get_openai_explanation(question, options, correct_option_index, valid_tags, tags)
        # Strip any '{' or '}' from the explanation and remove whitespaces
        cleaned_extra = extra.replace("{", "").replace("}", "").strip()

        queue.put((note['noteId'], cleaned_extra, index + 1))
        print(f"Note {index + 1} ({note['noteId']}) Processed")

def add_tag_to_anki(note_id, tag, note_index):
    """Add a tag to a note in Anki."""
    payload = {
        "action": "addTags",
        "version": 6,
        "params": {
            "notes": [note_id],
            "tags": tag
        }
    }
    response = send_anki_request(payload)
    if response is None:
        print(f"Note {note_index} ({note_id}) Tag Added: {tag}")
    elif isinstance(response, list) and len(response) == 0:
        print(f"Failed to add tag to note {note_index} ({note_id}): Anki returned an empty list (Possible AnkiConnect issue).")
    else:
        print(f"Failed to add tag to note {note_index} ({note_id}): {response}")
    return response

def process_queue_and_update(queue):
    """Process queue and add tags to Anki in parallel."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(add_tag_to_anki, note_id, tag, note_index)
                   for note_id, tag, note_index in iter(queue.get, None)]
        for future in futures:
            future.result() # No need to check result here, message is already printed in add_tag_to_anki

def main():
    """Main function."""
    deck_name = "Custom Study Session"
    queue = Queue()
    note_ids = get_note_ids(deck_name)

    if note_ids:
        notes_info = get_notes_info(note_ids)
        process_notes(notes_info, queue)
        queue.put(None)
        process_queue_and_update(queue)
        print("All notes have been processed and updated.")
    else:
        print(f"No notes found in deck '{deck_name}' or AnkiConnect Error.")

if __name__ == "__main__":
    main()
