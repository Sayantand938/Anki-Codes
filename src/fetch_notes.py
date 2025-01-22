import requests
import json

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

def print_notes_info(notes_info):
    # Print the detailed notes info
    for note in notes_info:
        note_id = note['noteId']
        fields = note['fields']
        
        # Extract the relevant fields (assuming the field names are correct)
        question = fields.get('Question', {}).get('value', '')
        op1 = fields.get('OP1', {}).get('value', '')
        op2 = fields.get('OP2', {}).get('value', '')
        op3 = fields.get('OP3', {}).get('value', '')
        op4 = fields.get('OP4', {}).get('value', '')
        answer = fields.get('Answer', {}).get('value', '')
        extra = fields.get('Extra', {}).get('value', '')
        tags = note.get('tags', [])
        
        # Print the note data
        print(f"Note ID: {note_id}")
        print(f"Question: {question}")
        print(f"OP1: {op1}")
        print(f"OP2: {op2}")
        print(f"OP3: {op3}")
        print(f"OP4: {op4}")
        print(f"Answer: {answer}")
        print(f"Extra: {extra}")
        print(f"Tags: {tags}")
        print("-" * 40)

deck_name = "Custom Study Session"
note_ids = get_note_ids(deck_name)

if note_ids:
    print(f"Found {len(note_ids)} notes in deck '{deck_name}'")
    
    # Get detailed information for each note
    notes_info = get_notes_info(note_ids)
    
    # Print all notes data
    print_notes_info(notes_info)
else:
    print(f"No notes found in deck '{deck_name}'")
