import requests
import pyperclip  # For copying to clipboard

# Define AnkiConnect API URL
anki_connect_url = "http://localhost:8765"

def fetch_note_ids_from_deck():
    """
    Fetches all note IDs from the "Custom Study Session" deck.
    """
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
        print("Error: Unable to fetch note IDs from the deck.")
        return []

def get_note_ids_in_range(note_ids, start, end=None):
    """
    Returns note IDs within the specified range.
    If `end` is None, only the note ID at `start` is returned.
    """
    if end is None:
        # Case 2: Single question (e.g., 10)
        if start < 1 or start > len(note_ids):
            print(f"Error: Question number {start} is out of range.")
            return None
        return [note_ids[start - 1]]  # Return the specific note ID
    else:
        # Case 1: Range of questions (e.g., 10-20)
        if start < 1 or end > len(note_ids) or start > end:
            print(f"Error: Invalid range {start}-{end}.")
            return None
        return note_ids[start - 1:end]  # Return note IDs in the range

def main():
    # Fetch all note IDs from the "Custom Study Session" deck
    note_ids = fetch_note_ids_from_deck()
    if not note_ids:
        print("No notes found in the 'Custom Study Session' deck.")
        return

    # Prompt the user for input
    user_input = input("Enter the question range (e.g., 10 or 10-20): ").strip()

    # Parse the input
    if "-" in user_input:
        # Case 1: Range input (e.g., 10-20)
        try:
            start, end = map(int, user_input.split("-"))
            result_note_ids = get_note_ids_in_range(note_ids, start, end)
        except ValueError:
            print("Invalid input. Please enter a valid range (e.g., 10-20).")
            return
    else:
        # Case 2: Single number input (e.g., 10)
        try:
            start = int(user_input)
            result_note_ids = get_note_ids_in_range(note_ids, start)
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 10).")
            return

    # Output the result in the specified format and copy to clipboard
    if result_note_ids:
        output = f"nid:{','.join(map(str, result_note_ids))}"
        pyperclip.copy(output)  # Copy the output to the clipboard
        if "-" in user_input:
            print(f"note id of the questions {start}-{end} has been copied to clipboard ✅")
        else:
            print(f"note id of the question {start} has been copied to clipboard ✅")
    else:
        print("No note IDs found for the specified range.")

if __name__ == "__main__":
    main()