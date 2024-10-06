# Importing necessary libraries
import os
import PyPDF2
import subprocess
import tkinter as tk
from tkinter import filedialog

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):

    """
    Extracts text from a PDF file.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """

    # Open the PDF file in binary mode (reading it as raw bytes)
    with open(pdf_file_path, 'rb') as file:
        # Initialize a PDF reader to read the PDF content
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store the text extracted from the PDF
        extracted_text = ""
        
        # Loop through each page of the PDF and extract its text
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()  # Concatenate the extracted text from each page
    
    # Return the fully extracted text from the PDF
    return extracted_text

# Function to split the extracted text into smaller sections
def split_text_into_chunks(text, chunk_size=1024):

    """
    Splits a large text into smaller sections to avoid exceeding token limits.

    Args:
        text (str): The full text to be split.
        chunk_size (int): The size of each section in characters (default: 1024).

    Returns:
        list: A list of text sections.
    """

    # Use list comprehension to divide the text into sections of a specified size
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to send a section of text to the Llama model using a subprocess
def send_chunk_to_llama_model(text_chunk):

    """
    Sends a section of text to the Llama model using subprocess.

    Args:
        text_chunk (str): A section of text to be sent.

    Returns:
        str: The response from the Llama model for the text section.
    """

    # Define the command to run the Llama model (in this case, "ollama run llama3")
    command = "ollama run llama3"
    
    # Run the command using subprocess and pass the section of text as input
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Capture the output (result) and error from the subprocess
    output, error = process.communicate(input=text_chunk.encode('utf-8'))
    
    # Check if the subprocess was successful (return code 0 indicates success)
    if process.returncode == 0:
        return output.decode('utf-8')  # Return the model's output as a decoded string
    else:
        return f"Error: {error.decode('utf-8')}"  # Return any error message if the subprocess fails

# Function to open a file dialog and let the user select a PDF file
def select_pdf_file():

    """
    Opens a file dialog for the user to select a PDF file.
    
    Returns:
        str: The path to the selected PDF file.
    """

    # Create a hidden Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window as we only need the file dialog

    # Open a file dialog that allows the user to select a PDF file
    pdf_file_path = filedialog.askopenfilename(
        title="Select PDF to Summarize",
        filetypes=[("PDF Files", "*.pdf")]  # Restrict file selection to PDF files only
    )

    return pdf_file_path  # Return the selected file path

# Main function to handle the entire process of PDF extraction and text processing
def main():

    """
    Main function to manage the process of extracting text from a PDF
    and sending it to the Llama model for summarization.
    """

    # Step 1: Open a file dialog to allow the user to select a PDF file
    pdf_file_path = select_pdf_file()

    # If the user did not select a file, exit the program
    if not pdf_file_path:
        print("No file selected. Exiting...")
        return  # Exit if no file is chosen

    # Step 2: Extract the text from the selected PDF file
    print(f"Extracting text from {pdf_file_path}...")
    extracted_text = extract_text_from_pdf(pdf_file_path)

    # Step 3: Split the extracted text into smaller sections to manage token limits
    text_chunks = split_text_into_chunks(extracted_text)
    print(f"Split the extracted text into {len(text_chunks)} sections.")

    # Step 4: Process each text section individually and accumulate all responses
    all_text = ""
    for i, chunk in enumerate(text_chunks):
        print(f"Reading section {i + 1}...")
        all_text += chunk  # Combine all sections of text into a single string

    # Step 5: Prepare a structured prompt for summarizing the extracted text
    final_prompt = (
        f"Summarize the following text under these sections:\n\n"
        f"1. Introduction and Background\n"
        f"2. Methodology\n"
        f"3. Results\n"
        f"4. Discussion and Interpretation\n"
        f"5. Conclusion and Future Work\n\n"
        f"----------------------------------\n\n"
        f"Text:\n{all_text}"
    )
    
    # Step 6: Send the combined text to the Llama model for summarization
    print("Summarization...")
    summary = send_chunk_to_llama_model(final_prompt)
    
    # Step 7: Print the final summarized output from the model
    print("\nSummary:\n")
    print(summary)

# Entry point of the program
if __name__ == "__main__":

    # Clear the console screen (compatible with both Windows and Unix-based systems)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Call the main function to run the program
    main()
