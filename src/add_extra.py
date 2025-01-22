import os
from openai import OpenAI
import requests
from queue import Queue
from markdown import Markdown
import htmlmin
from concurrent.futures import ThreadPoolExecutor

# Initialize OpenAI client
client = OpenAI()

# Define the AnkiConnect server URL
ANKI_CONNECT_URL = 'http://localhost:8765'

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

def get_openai_explanation(question, options, correct_option_index):
    """Fetch explanation from OpenAI using gpt-4o-mini model."""
    correct_answer = options[correct_option_index]

    prompt = f"""
    Question: {question}
    Options:
      1: {options[0]}
      2: {options[1]}
      3: {options[2]}
      4: {options[3]}
    Correct Answer: {correct_answer}

    Summarize the reasoning behind the correct answer in a compact and clear explanation. Give output in simple text format.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant specialized in providing concise and clear explanations."},
                {"role": "user", "content": prompt}
            ]
        )
        # Correctly access the content of the first message in the choices list
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Unable to fetch explanation"

def process_notes(notes_info, queue):
    """Process notes and add to queue, skip if note does not have 'ENG' tag or 'Extra' field is not empty."""
    md = Markdown()
    for index, note in enumerate(notes_info):
        fields = note['fields']
        extra_field = fields.get('Extra', {}).get('value', '')  # Get the value of the Extra field
        tags = note.get('tags', [])

        # Check if the note has 'ENG' tag and 'Extra' field is empty
        if 'ENG' in tags and not extra_field:
            question = fields.get('Question', {}).get('value', '')
            options = [fields.get(f'OP{i+1}', {}).get('value', '') for i in range(4)]
            correct_option_index = int(fields.get('Answer', {}).get('value', '0')) - 1

            extra = get_openai_explanation(question, options, correct_option_index)
            html_content = md.convert(extra)
            minified_html = htmlmin.minify(html_content)

            queue.put((note['noteId'], minified_html, index + 1))
            print(f"Note {index + 1} ({note['noteId']}) Processed")
        else:
            print(f"Note {index + 1} ({note['noteId']}) skipped")

def update_note_in_anki(note_id, minified_html, note_index):
    """Update note in Anki."""
    payload = {
        "action": "updateNote",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    "Extra": minified_html
                }
            }
        }
    }
    response = send_anki_request(payload)
    if response is None:
        print(f"Note {note_index} ({note_id}) Updated")
    elif isinstance(response, list) and len(response) == 0:
        print(f"Failed to update note {note_index} ({note_id}): Anki returned an empty list (Possible AnkiConnect issue).")
    else:
        print(f"Failed to update note {note_index} ({note_id}): {response}")
    return response

def process_queue_and_update(queue):
    """Process queue and update Anki in parallel."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(update_note_in_anki, note_id, html, note_index)
                   for note_id, html, note_index in iter(queue.get, None)]
        for future in futures:
            future.result()  # No need to check result here, message is already printed in update_note_in_anki

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
