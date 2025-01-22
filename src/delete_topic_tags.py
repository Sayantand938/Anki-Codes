import requests
import json
from concurrent.futures import ThreadPoolExecutor

def get_note_ids(deck_name):
    # AnkiConnect request to find notes in the specified deck
    request_payload = {
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'deck:"{deck_name}"'
        }
    }

    response = requests.post('http://localhost:8765', json=request_payload)
    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def get_notes_info(note_ids):
    # AnkiConnect request to get detailed info (tags, fields, etc.) for the notes
    request_payload = {
        'action': 'notesInfo',
        'version': 6,
        'params': {
            'notes': note_ids
        }
    }

    response = requests.post('http://localhost:8765', json=request_payload)
    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def update_note_tags(note_id, tags):
    # AnkiConnect request to update the tags for a note
    request_payload = {
        'action': 'updateNote',
        'version': 6,
        'params': {
            'note': {
                'id': note_id,
                'tags': tags
            }
        }
    }

    response = requests.post('http://localhost:8765', json=request_payload)
    if response.status_code == 200:
        print(f"Updated note {note_id} with tags: {tags}")
    else:
        print(f"Failed to update note {note_id}. Error: {response.status_code}")

def process_notes(notes_info):
    # Define the relevant categories
    relevant_tags = ['GI', 'MATH', 'GK', 'ENG']
    
    # Create a list of tasks for updating tags
    tasks = []

    for note in notes_info:
        note_id = note['noteId']
        tags = note.get('tags', [])
        
        # Filter out tags:
        # 1. Include tags that start with "Prelims"
        # 2. Include tags that are in the relevant categories (GI, MATH, GK, ENG)
        filtered_tags = [tag for tag in tags if tag.startswith('Prelims') or tag in relevant_tags]
        
        if filtered_tags:
            tasks.append((note_id, filtered_tags))
    
    # Use ThreadPoolExecutor to run up to 2 concurrent workers for updating tags
    with ThreadPoolExecutor(max_workers=2) as executor:
        for note_id, tags in tasks:
            executor.submit(update_note_tags, note_id, tags)

deck_name = "Custom Study Session"
note_ids = get_note_ids(deck_name)

if note_ids:
    print(f"Found {len(note_ids)} notes in deck '{deck_name}'")
    
    # Get detailed information for each note
    notes_info = get_notes_info(note_ids)
    
    # Process and update tags for each note using 2 concurrent workers
    process_notes(notes_info)
else:
    print(f"No notes found in deck '{deck_name}'")
