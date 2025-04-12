# Project: Extracting Blog URL and Global-ID from Website URLs

## Overview

This project consists of Python scripts to extract blog URLs and Global-IDs from a list of website URLs provided in `Website_URLs.csv`. The script `Find_GlobalID.py` reads the list of base URLs, identifies corresponding blog URLs, and then retrieves the Global-ID from those blog pages.

## Project Structure

```
exercise-scripting/
├── Find_GlobalID.py      # Main script to find Global-IDs
├── get_last_char.py      # Utility script to get the last characters from a string
├── README.md             # Project documentation (this file)
├── requirements.txt      # List of project dependencies
└── Website_URLs.csv      # CSV file containing the list of website URLs
```

## Setup Instructions

### Windows

1.  **Install Python:** If you don't have Python installed, download the latest version from the [official Python website](https://www.python.org/downloads/windows/). Make sure to add Python to your PATH during installation.
2.  **Install pip:** Pip is usually included with Python installations. You can verify by opening Command Prompt and running `pip --version`. If not installed, follow the instructions on the official pip documentation.
3.  **Install Dependencies:** Navigate to the `exercise-scripting` directory in Command Prompt and run the following command to install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### MacOS/Linux

1.  **Install Python:** Most MacOS and Linux distributions come with Python pre-installed. You can check the version by opening Terminal and running `python3 --version` or `python --version`. If not installed or if you need a specific version, you can download it from the [official Python website](https://www.python.org/downloads/mac-osx/) or use your distribution's package manager.
2.  **Install pip:** Similar to Windows, pip is usually included with Python. Verify with `pip3 --version` or `pip --version` in Terminal. If not installed, follow the instructions on the official pip documentation for your distribution.
3.  **Install Dependencies:** Open Terminal, navigate to the `exercise-scripting` directory, and run the following command to install the necessary libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Execution Instructions

1.  **Navigate to the Project Directory:** Open your Command Prompt (Windows) or Terminal (MacOS/Linux) and navigate to the `exercise-scripting` folder.
2.  **Run the Script:** Execute the `Find_GlobalID.py` script using the Python interpreter:
    ```bash
    python Find_GlobalID.py
    ```
    or
    ```bash
    python3 Find_GlobalID.py
    ```
3.  **Check the Output:** The script will print the progress and any errors encountered during execution in the console. Two CSV files will be created in the same directory:
    * `Output.CSV`: Contains the base URLs and their corresponding Global-IDs.
    * `Output_blog.CSV`: Contains the extracted blog URLs and their Global-IDs.
    The script will also print the execution time for different parts of the process and the total execution time at the end, displayed in minutes.

**Note:** Ensure that the `Website_URLs.csv` file is present in the same directory as the script before running it. This file contains the list of website URLs that the script will process.