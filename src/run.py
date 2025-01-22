from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a motivational quote."
        }
    ]
)

# Correctly access the content of the message
print(completion.choices[0].message.content)
