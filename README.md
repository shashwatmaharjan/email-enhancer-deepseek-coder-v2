
# Email Composer and Grammar Checker

This Python script helps users compose and polish emails by providing grammar checks and subject line suggestions. It integrates with the Llama model using ollama to enhance the clarity and professionalism of the email content. Additionally, it now uses `figlet` to create a large ASCII art banner when the script starts.

## Prerequisites

- Python 3.9+
- Homebrew (for easy installation of dependencies)
- ollama installed and configured for running Llama models
- `figlet` for ASCII art (optional but adds a nice touch to the interface)

## Features

- Creates a temporary file for users to write their email content in the terminal using the nano editor.
- Enhances the email for grammar, clarity, and professionalism.
- Provides suggestions for a formal and concise subject line.
- Deletes temporary files for user privacy once processing is complete.
- Displays an ASCII art banner using `figlet` at the start of the script.

## Installation

### Step 1: Install Homebrew

If you do not have Homebrew installed, you can install it by running the following command:

\`\`\`bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
\`\`\`

For more information about Homebrew, visit [https://brew.sh/](https://brew.sh/).

### Step 2: Install Python 3.9 using Homebrew

To install Python 3.9 using Homebrew, use the following command:

\`\`\`bash
brew install python@3.9
\`\`\`

### Step 3: Install ollama

You will need to install the ollama CLI to run the Llama model. Follow these steps to install and set it up:

1. Run the following command to install ollama:

\`\`\`bash
brew install ollama
\`\`\`

2. Once installed, verify that ollama is working by checking the version:

\`\`\`bash
ollama --version
\`\`\`

### Step 4: Download the `gemma:7b` Model

After setting up ollama, download the gemma:7b model using the following command:

\`\`\`bash
ollama pull gemma:7b
\`\`\`

For more information about this model, you can visit the official [Gemma model page on Ollama's website](https://ollama.com/library/gemma).

### Step 5: Install `figlet` for ASCII Art (Optional)

To display a large ASCII art banner when the script starts, install `figlet` using Homebrew:

\`\`\`bash
brew install figlet
\`\`\`

### Step 6: Create and Activate a Virtual Environment (Optional but Recommended)

To keep your dependencies organized, it is recommended to create a Python virtual environment. Run the following commands:

\`\`\`bash
# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment named 'venv'
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Unix/macOS
# OR
venv\Scripts\activate  # For Windows
\`\`\`

## Usage

1. Clone or download this repository to your local machine.
2. Open the terminal and navigate to the project directory.
3. Activate your virtual environment (if you created one).
4. Run the script:

\`\`\`bash
python main.py
\`\`\`

5. The program will display a large ASCII art banner and open the nano text editor. Write your email and save the file.
6. The script will process your email, check it for grammar, and suggest an appropriate subject line.
7. The final email draft will be displayed in the terminal, ready for you to copy into your email client.

## Example Output
Hi, I'm Jarvis! I'm here to help you compose and polish your emails.

Processing your email to enhance it for grammar, clarity, and professionalism...
---------------------------------------------------------------------------------------------
[Enhanced Email Output with Subject Line]
---------------------------------------------------------------------------------------------
Your email is ready! Feel free to copy it to your email client and send it.
\`\`\`

## License

This project is licensed under the MIT License for the code developed in this repository. However, it also incorporates the use of the Gemma model via the `ollama` CLI, which is subject to a separate license. Users are required to follow the licensing terms associated with the Gemma model.

For more information on the Gemma model and its licensing, please refer to the official [Gemma model page on Ollama's website](https://ollama.com/library/gemma).
