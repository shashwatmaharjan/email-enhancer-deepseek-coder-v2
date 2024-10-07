import os
import subprocess
import platform


def get_input_email_path():

    """
    Get the path to the 'input.txt' file located in the 'emails' directory.
    """

    # Get the absolute path of the current script
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory of the current script directory
    parent_script_directory = os.path.dirname(current_script_directory)

    # Construct the path to 'emails/input.txt' in the parent directory
    input_email_path = os.path.join(parent_script_directory, 'emails', 'input.txt')

    return input_email_path


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
        "Shashwat Maharjan"
    )

    # Insert the user's email body into the template
    return email_template.format(email_body=email_body)


def prepare_final_prompt(email_content):

    """
    Prepare the final prompt to send to the Llama model.
    """

    # Define instructions for the Llama model along with the email content
    final_prompt = (
        "Please proofread and enhance the following email for grammar, clarity, and professionalism. "
        "Rewrite it if necessary. Additionally, suggest an appropriate email subject line.\n\n"
        f"{email_content}"
    )

    return final_prompt


def run_llama_model(prompt, model_name="llama3.2"):

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
            stdin=subprocess.PIPE,   # Allow input to the subprocess
            stdout=subprocess.PIPE,  # Capture the output
            stderr=subprocess.PIPE,  # Capture any errors
            text=True                # Use text mode for input/output
        )

        # Communicate the prompt to the subprocess and capture output and errors
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

def clear_input_file(file_path):

    """
    Clear the contents of the specified file.
    """

    try:

        # Open the file in write mode to overwrite existing content
        with open(file_path, 'w', encoding='utf-8') as file:

            # Write an empty string to clear the file
            file.write('')

    except Exception as e:

        # Print an error message if unable to clear the file
        print(f"An error occurred while clearing your draft email: {e}")

def main():

    """
    Main function to orchestrate reading the email, processing it, and displaying the output.
    """

    # Step 0: Greet the user
    print("Hello! I'm your personal email assistant. I'm here to help you compose and polish your emails.\n")

    # Step 1: Get the input email path
    input_email_path = get_input_email_path()

    # Ensure the 'emails' directory exists
    os.makedirs(os.path.dirname(input_email_path), exist_ok=True)

    # Ensure the 'input.txt' file exists
    if not os.path.exists(input_email_path):

        # Create an empty 'input.txt' file if it doesn't exist
        with open(input_email_path, 'w', encoding='utf-8'):

            pass  # The 'pass' statement does nothing; file creation is enough

    # Step 2: Open 'input.txt' in nano editor and wait until it's closed
    open_text_editor(input_email_path)

    # Step 3: Read the email body from 'input.txt'
    email_body = read_email_body(input_email_path)

    # Check if the email body is empty or contains only whitespace
    if not email_body.strip():

        print("Hmm, it seems you didn't enter any content. Please make sure to write your email content.")
        
        return  # Exit the main function if no content is found

    # Step 4: Prepare the email template
    email_content = prepare_email_template(email_body)

    # Step 5: Prepare the final prompt for the Llama model
    final_prompt = prepare_final_prompt(email_content)

    # Step 6: Run the Llama model and get the output
    output = run_llama_model(final_prompt)

    # Step 7: Display the output
    print("----------------------------------------------------------------------------------------------------")
    print(output)

    # Step 8: Clear the contents of 'input.txt'
    clear_input_file(input_email_path)
    print("I've cleared your draft email from the input file for your privacy.")
    print("Your email is ready! Feel free to copy it to your email client and send it.\n")

if __name__ == "__main__":
    main()
