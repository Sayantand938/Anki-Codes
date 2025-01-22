def generate_question_format(num_questions=100, output_file="output.txt"):
    """Generates the specified question format up to the given number of questions and saves it to the output file, with a blank line between each question block.

    Args:
        num_questions: The total number of questions to generate.
        output_file: The name of the output file.

    Returns:
        None
    """

    with open(output_file, "w") as f:
        for i in range(1, num_questions + 1):
            f.write(f"```Q-{i}\n")
            f.write("<===================={QUESTION}====================>\n")
            f.write("\n")
            f.write("<===================={EXTRA}====================>\n")
            f.write("\n")
            f.write("```\n\n")  # Add a blank line here

# Generate the format for 100 questions and save to output.txt
generate_question_format(100)