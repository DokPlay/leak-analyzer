
[Ru version](README.md)
      


# Leak Analyzer (Trial Version)

**Leak Analyzer** is a minimal module for data breach analysis, including parsing public databases and Tor network forums. The module allows you to find credentials such as usernames and passwords, and export them to a text file for further analysis.

## Functionality

- **Public Database Parsing**: The program scans public websites for data breaches, such as email addresses and passwords. It supports working with several well-known data sources.

- **Onion Forum Parsing**: The program uses a Tor proxy for secure access to onion sites and searches for data breaches on them.

- **Export Data to TXT File**: All found credentials are saved to a text file for further use or analysis.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/leak-analyzer.git
Install dependencies:
To install the dependencies listed in requirements.txt, run the following command:


pip install -r requirements.txt
Run the parser:
To start parsing public sources and onion forums, execute the following command:


python main.py
Results will be saved in two files:

public_leaks.txt — contains data leaks from public sources.

onion_leaks.txt — contains data leaks from onion forums.

How It Works
Public Source Parsing: The module uses several popular websites to search for public pastes, such as Pastebin, Hastebin, and others. It searches for logins and passwords using regular expressions and saves the results.

Onion Source Parsing: A Tor proxy is used to access onion sites. This module connects to the Tor network and searches forums for data breaches by making asynchronous requests to the provided links.

Export to TXT File: After finding the leaks, the program saves the results to text files that can be used for further analysis.
