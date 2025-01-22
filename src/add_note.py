import os
import re
import requests
from markdown_it import MarkdownIt
from minify_html import minify
from pathlib import Path

# Initialize markdown-it-py parser
md = MarkdownIt()

# Path to your Markdown file
file_path = 'D:/OBSIDIAN/NOTES/Untitled.md'

# Read the content of the Markdown file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Convert all LaTeX $...$ to \( ... \) format
data = re.sub(r'\$(.*?)\$', r'\\\(\1\\\)', data)

# Define regular expressions for parsing different sections
tags_block_regex = r'```tags([\s\S]*?)```'
question_block_regex = r'```Q-(\d+)([\s\S]*?)```'

# Extract the tags block
tags_block_match = re.search(tags_block_regex, data)
tags = tags_block_match.group(1).strip() if tags_block_match else ''

# Initialize output list with header lines
output_data = [
    '#separator:tab',
    '#html:true',
    '#tags column:8',
]

# Parse each question block
for match in re.finditer(question_block_regex, data):
    question_number = match.group(1)
    question_content = match.group(2).strip()

    question_section_match = re.search(r'<====================\{QUESTION\}====================>([\s\S]*?)<====================\{EXTRA\}====================>([\s\S]*)', question_content)

    question_text = question_section_match.group(1).strip() if question_section_match else ''
    extra_text = question_section_match.group(2).strip() if question_section_match else ''

    lines = [line.strip() for line in question_text.split('\n') if line.strip()]
    options = lines[-4:]

    correct_option_index = None
    cleaned_options = []
    for index, option in enumerate(options):
        cleaned_option = re.sub(r'^\-+\s*', '', option.replace('✅', '').strip())
        if '✅' in option:
            correct_option_index = index + 1
        cleaned_options.append(cleaned_option)

    question_without_options = '\n'.join(lines[:-4]).strip()
    formatted_question = '<br>'.join(question_without_options.split('\n')).strip()
    clean_question = formatted_question.replace('**', '')

    question_html = md.render(clean_question).replace('<p>', '').replace('</p>', '')
    minified_question_html = minify(question_html, minify_js=True, minify_css=True)

    option_htmls = []
    for option in cleaned_options:
        option_html = md.render(option).replace('<p>', '').replace('</p>', '')
        minified_option_html = minify(option_html, minify_js=True, minify_css=True)
        option_htmls.append(minified_option_html)

    extra_html = md.render(extra_text)
    minified_extra_html = minify(extra_html, minify_js=True, minify_css=True)

    tsv_row = f'{minified_question_html}\t{"\t".join(option_htmls)}\t{correct_option_index or ""}\t{minified_extra_html}\t{tags}'
    output_data.append(tsv_row)

# Write the output to a TSV file
output_file_path = Path(__file__).parent / 'output.tsv'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write('\n'.join(output_data))

print('Output written to output.tsv')

# Define the AnkiConnect API endpoint
ANKI_CONNECT_URL = 'http://localhost:8765'

# Function to invoke the Import dialog
def invoke_import_dialog(file_path):
    payload = {
        "action": "guiImportFile",
        "version": 6,
        "params": {
            "path": file_path
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload)
    return response.json()

# Invoke the import function with the output TSV file
result = invoke_import_dialog(str(output_file_path))

# Check the result and print a success message if no error
if result.get('error') is None:
    print('New Notes Successfully Added')
else:
    print('Error:', result.get('error'))



