import os
import subprocess

import tkinter as tk
from tkinter import filedialog

import json
import re
import PyPDF2

def extract_text_from_pdf(pdf_file_path):

    """
    Extract text from a PDF file.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """

    # Open the PDF file in binary read mode
    with open(pdf_file_path, 'rb') as file:

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        extracted_text = ""

        # Iterate over all pages in the PDF
        for page in pdf_reader.pages:

            # Extract text from the current page and append to extracted_text
            extracted_text += page.extract_text()

    # Return the combined extracted text from all pages
    return extracted_text


def send_chunk_to_llama_model(text_chunk):

    """
    Send a text chunk to the Llama model for processing.

    Args:
        text_chunk (str): The text to be processed.

    Returns:
        str: The model's output or an error message.
    """

    # Command to run the Llama model (assumes 'ollama' is installed and configured)
    command = "ollama run llama3:70b"

    # Start the subprocess to run the Llama model
    process = subprocess.Popen(
        command,
        shell=True,  # Using shell=True to run the command in the shell
        stdin=subprocess.PIPE,  # Provide input to the process via stdin
        stdout=subprocess.PIPE,  # Capture the output from stdout
        stderr=subprocess.PIPE   # Capture any errors from stderr
    )

    # Communicate with the process: send the text chunk and get the output and error
    output, error = process.communicate(input=text_chunk.encode('utf-8'))

    # Check if the process completed successfully
    if process.returncode == 0:

        # Return the model's output decoded from bytes to string
        return output.decode('utf-8')
    
    else:

        # Return the error message decoded from bytes to string
        return f"Error: {error.decode('utf-8')}"


def extract_json_from_response(response):

    """
    Attempt to extract JSON content from the model's response.

    Args:
        response (str): The raw response from the model.

    Returns:
        dict or None: The extracted sections as a dictionary, or None if parsing fails.
    """

    # Use a regular expression to find JSON content in the response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)

    if json_match:

        # Extract the JSON string from the match
        json_str = json_match.group(0)

        try:
            # Parse the JSON string into a dictionary
            sections = json.loads(json_str)
            return sections
        
        except json.JSONDecodeError:

            # Handle JSON parsing errors
            print("Failed to parse JSON from extracted content.")

            return None
        
    else:

        # Handle the case where no JSON content is found
        print("No JSON content found in the model's response.")

        return None


def identify_sections_with_llama(text):

    """
    Use the Llama model to identify sections within the text by processing it in chunks.

    Args:
        text (str): The full text extracted from the PDF.

    Returns:
        dict: A dictionary with section titles as keys and corresponding text as values.
    """

    sections = {}  # Initialize a dictionary to store sections
    max_chunk_size = 3000  # Adjust based on your model's token limit

    # Split the text into chunks to avoid exceeding the model's input limit
    for i in range(0, len(text), max_chunk_size):

        chunk = text[i:i + max_chunk_size]

        # Construct the prompt for the Llama model
        prompt = (
            "Please extract the section titles and their corresponding text from the following content. "
            "Output the result strictly in JSON format without any additional text or explanations.\n\n"
            f"Content:\n{chunk}\n\n"
            "Output format:\n"
            "{\n"
            "  \"Section Title\": \"Section Content\",\n"
            "  ...\n"
            "}\n"
        )

        # Send the prompt to the Llama model and get the response
        response = send_chunk_to_llama_model(prompt)

        # print("Model's Response:")
        # print(response)

        # Attempt to extract JSON content from the model's response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]

        try:

            # Parse the JSON string into a dictionary
            chunk_sections = json.loads(json_str)

            # Update the sections dictionary with the new sections
            sections.update(chunk_sections)

        except json.JSONDecodeError:

            # Handle JSON parsing errors
            print("Failed to parse JSON from the model's response.")

            continue

    if not sections:

        print("I couldn't identify any sections. I think I have more work to do.")

    else:

        print("I have successfully identified sections.")

    # Return the dictionary containing all identified sections
    return sections


def select_pdf_file():

    """
    Open a file dialog for the user to select a PDF file.

    Returns:
        str: The path to the selected PDF file.
    """

    # Create a hidden root window
    root = tk.Tk()

    root.withdraw()  # Hide the root window

    # Open the file dialog to select a PDF file
    pdf_file_path = filedialog.askopenfilename(
        title="Select PDF to Summarize",
        filetypes=[("PDF Files", "*.pdf")]  # Only allow selection of PDF files
    )

    # Return the selected file path
    return pdf_file_path


def main():

    """
    Main function to orchestrate the summarization of a research paper PDF.
    """

    # Prompt the user to select a PDF file
    pdf_file_path = select_pdf_file()

    if not pdf_file_path:

        print("No file selected. Exiting...")
        return

    # Extract text from the selected PDF file
    extracted_text = extract_text_from_pdf(pdf_file_path)

    # Identify sections within the extracted text using the Llama model
    sections = identify_sections_with_llama(extracted_text)

    if not sections:
        print("I could not identify any sections. Sorry!")
        return

    # Define sections to exclude from summarization
    sections_to_exclude = ["References", "Work Cited", "Appendix"]

    # Iterate over each identified section
    for section, content in sections.items():

        # Check if the section should be excluded
        if section not in sections_to_exclude:

            print(f"Summarizing section: {section}")

            # Construct the prompt for summarizing the section
            final_prompt = (
                "Please summarize the following research paper section. Ignore references and citations.\n\n"
                f"Section Title: {section}\n\n"
                f"Section Text: {content}\n\n"
                "Summary:"
            )

            # Send the prompt to the Llama model and get the summary
            summary = send_chunk_to_llama_model(final_prompt)

            # Print the summary for the section
            print(f"Summary of {section}:\n{summary}\n")
            print(f"{summary}\n")


if __name__ == "__main__":

    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Run the main function
    main()
