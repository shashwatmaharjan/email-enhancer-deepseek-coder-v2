import os
import subprocess
import tempfile


def get_input_email_path():

    """
    Create a temporary file and return its path.
    """

    # Create a temporary file that won't be deleted upon closing
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name

    # Close the file so that the text editor can open it
    temp_file.close()

    return temp_file_path


def read_email_body(file_path):

    """
    Read the content of the email from the specified file path.
    """

    try:

        # Open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:

            # Read the entire content of the file
            email_body = file.read()

        return email_body

    except Exception as e:

        # Print an error message if something goes wrong
        print(f"Oops! I encountered an error while reading your email content: {e}")

        return ""


def prepare_email_template(email_body):

    """
    Prepare the email template by inserting the email body.
    """

    # Define a basic email template with placeholders
    email_template = (
        "Dear [Recipient's Name],\n\n"
        "{email_body}\n\n"
        "Thank you for your time.\n\n"
        "Best regards,\n"
        "[Your Name]"
    )

    # Insert the user's email body into the template
    formatted_email = email_template.format(email_body=email_body)

    return formatted_email


def prepare_final_prompt(email_content):

    """
    Prepare the final prompt to send to the Llama model.
    """

    # Define instructions for the Llama model along with the email content
    instructions = (
        "Check for grammar. Retain the original tone and structure of the email.\n"
        "Additionally, suggest an appropriate email subject line. Keep the subject line clear and short.\n"
        "---------------------------------------\n\n"
    )

    # Combine instructions and email content to form the final prompt
    final_prompt = f"{instructions}{email_content}"

    return final_prompt


def run_llama_model(prompt, model_name="deepseek-coder-v2:latest"):

    """
    Run the Llama model using the provided prompt and return the output.
    Assumes 'ollama' is installed and configured.
    """

    # Construct the command to run the Llama model
    command = f"ollama run {model_name}"

    try:

        # Inform the user that processing has started
        print("Processing your email to enhance it for grammar, clarity, and professionalism...")

        # Start the subprocess to run the command
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,    # Allow input to the subprocess
            stdout=subprocess.PIPE,   # Capture the output
            stderr=subprocess.PIPE,   # Capture any errors
            text=True                 # Use text mode for input/output
        )

        # Send the prompt to the subprocess and wait for it to finish
        output, error = process.communicate(input=prompt)

        # Check if any errors occurred during processing
        if error:

            print(f"Sorry, I encountered an error while processing your email: {error}")

        return output

    except Exception as e:


        # Handle exceptions that may occur during subprocess execution
        print(f"An error occurred while running the Llama model: {e}")
        return ""


def open_text_editor(file_path):

    """
    Open the specified file in the nano editor and wait until it's closed.
    """

    try:

        # Open the file using the nano text editor
        subprocess.call(['nano', file_path])

    except Exception as e:

        # Handle any exceptions that occur while opening the editor
        print(f"An error occurred while opening the text editor: {e}")

        # Prompt the user to press Enter after saving the file
        input("After saving the file, press Enter to continue...")


def delete_temporary_file(file_path):

    """
    Delete the specified file.
    """

    try:
        os.remove(file_path)

    except Exception as e:

        # Print an error message if unable to delete the file
        print(f"An error occurred while deleting the temporary file: {e}")


def main():
    """
    Main function to orchestrate reading the email, processing it, and displaying the output.
    """

    # Step 0: Greet the user
    # Use figlet to create a large ASCII art banner
    subprocess.call(['figlet', '-f', 'isometric3', 'jarvis'])
    print("Hi, I'm Jarvis! I'm here to help you compose and polish your emails.\n")

    # Step 1: Create a temporary input file
    input_email_path = get_input_email_path()

    # Step 2: Open the temporary file in nano editor and wait until it's closed
    open_text_editor(input_email_path)

    # Step 3: Read the email body from the temporary file
    email_body = read_email_body(input_email_path)

    # Check if the email body is empty or contains only whitespace
    if not email_body.strip():
        print("Hmm, it seems you didn't enter any content. Please make sure to write your email content.")

        # Delete the temporary file
        delete_temporary_file(input_email_path)

        return  # Exit the main function if no content is found

    # Step 4: Prepare the email template
    email_content = prepare_email_template(email_body)

    # Step 5: Prepare the final prompt for the Llama model
    final_prompt = prepare_final_prompt(email_content)

    # Step 6: Run the Llama model and get the output
    output = run_llama_model(final_prompt)

    # Step 7: Display the output
    print("---------------------------------------------------------------------------------------------")
    print(output)

    # Step 8: Delete the temporary input file
    delete_temporary_file(input_email_path)

    # Inform the user that the draft email has been deleted
    print("I've deleted your draft email from the input file for your privacy.")

    # Provide final message to the user
    print("Your email is ready! Feel free to copy it to your email client and send it.\n")


if __name__ == "__main__":

    # Clear the console screen (compatible with both Windows and Unix-based systems)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Call the main function to run the program
    main()
