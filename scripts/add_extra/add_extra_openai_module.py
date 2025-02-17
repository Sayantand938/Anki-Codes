from openai import OpenAI

# Initialize OpenAI client (API key is automatically picked up from the environment variable)
client = OpenAI()

# Function to send data to OpenAI's GPT-4 API and return the explanation
def process_with_openai(note_details):
    # Create the multi-line string for the prompt
    prompt_text = (
        f"Question: {note_details['Question']}\n"
        f"Option 1: {note_details['OP1']}\n"
        f"Option 2: {note_details['OP2']}\n"
        f"Option 3: {note_details['OP3']}\n"
        f"Option 4: {note_details['OP4']}\n"
        f"Answer: {note_details['Answer']}\n"
        f"Prompt: Provide a concise explanation for the correct answer.\n"
        f"Output Format: <required explanation>"
    )
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert educator who provides concise, clear, and accurate explanations. Be as concise as possible. "
                        "Avoid unnecessary details, introductions, or disclaimers. "
                        "Focus solely on explaining why the correct answer is valid and briefly mention why other options are incorrect (if relevant). "
                        "Provide the explanation as plain text without any line breaks, bullet points, or structured formatting."
                        "Explain as briefly as possible."
                    )
                },
                {"role": "user", "content": prompt_text}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return None  # Silently fail if there's an error with OpenAI