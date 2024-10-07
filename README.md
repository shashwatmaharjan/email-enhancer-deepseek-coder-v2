
# Email Composer and Grammar Checker

This Python script helps users compose and polish emails by providing grammar checks and subject line suggestions. It integrates with the Llama model using `ollama` to enhance the clarity and professionalism of the email content.

## Prerequisites

- Python 3.9+
- Homebrew (for easy installation of dependencies)
- `ollama` installed and configured for running Llama models

## Features

- Creates a temporary file for users to write their email content in the terminal using the `nano` editor.
- Enhances the email for grammar, clarity, and professionalism.
- Provides suggestions for a formal and concise subject line.
- Deletes temporary files for user privacy once processing is complete.

## Installation

### Step 1: Install Homebrew

If you do not have Homebrew installed, you can install it by running the following command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

For more information about Homebrew, visit [https://brew.sh/](https://brew.sh/).

### Step 2: Install Python 3.9 using Homebrew

To install Python 3.9 using Homebrew, use the following command:

```bash
brew install python@3.9
```

### Step 3: Create and Activate a Virtual Environment

To keep your dependencies organized, it is recommended to create a Python virtual environment. Run the following commands:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment named 'venv'
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Unix/macOS
# OR
venv\Scripts\activate  # For Windows
```

### Step 4: Install Required Python Libraries

Make sure you install the required Python packages by running the following command in your virtual environment:

```bash
pip install -r requirements.txt
```

### Step 5: Install `ollama`

Install `ollama` to integrate with the Llama model by following the instructions from the [ollama website](https://ollama.ai/).

## Usage

1. Clone or download this repository to your local machine.
2. Open the terminal and navigate to the project directory.
3. Activate your virtual environment (see Step 3).
4. Run the script:

   ```bash
   python main.py
   ```

5. The program will open the `nano` text editor. Write your email and save the file.
6. The script will process your email, check it for grammar, and suggest an appropriate subject line.
7. The final email draft will be displayed in the terminal, ready for you to copy into your email client.

## Example Output

```
Hi Shashwat! I'm here to help you compose and polish your emails.

Processing your email to enhance it for grammar, clarity, and professionalism...
---------------------------------------------------------------------------------------------
[Enhanced Email Output with Subject Line]
---------------------------------------------------------------------------------------------
Your email is ready! Feel free to copy it to your email client and send it.
```

## License

This project is licensed under the MIT License.
