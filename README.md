# SFDC Brewery Salesforce Developer Agent 🍻🤖

Welcome to the **SFDC Brewery Salesforce Developer Agent**! This project leverages **Microsoft Autogen** to create a conversational AI agent that generates and executes Salesforce code based on user input or Jira tasks. Whether you're a Salesforce developer or administrator, this tool will help you automate repetitive tasks and boost productivity.

## Features

- **Conversational Interface**: Describe your task in plain English, and the agent will generate and execute the required Salesforce code.
- **Jira Integration**: Automatically parse Jira tasks and generate code to implement them.
- **Code Execution**: Execute Salesforce code directly from the interface.
- **Modern UI**: Built with Streamlit for a clean and interactive user experience.

## Getting Started

### Prerequisites

- Python 3.8+
- Salesforce credentials (username, password, security token)
- Azure OpenAI API key (for Autogen)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sfdcbrewery/Salesforce-AI-Developer-Agent.git
   cd Salesforce-AI-Developer-Agent
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file in the root directory and add your credentials:

   ```plaintext
   SF_USERNAME=your-salesforce-username
   SF_PASSWORD=your-salesforce-password
   SF_SECURITY_TOKEN=your-salesforce-security-token
   AZURE_API_KEY=your-azure-openai-api-key
   AZURE_BASE_URL=your-azure-openai-base-url
   AZURE_API_VERSION=your-azure-openai-api-version
   ```

4. **Run the app**:

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Open the app** in your browser.
2. **Describe your Salesforce JIRA task or generic Salesforce action** in the chat input 
```plaintext
   As a: Salesforce Administrator
   I want to: Clone any five existing accounts in Salesforce, creating new accounts with the same details as the originals.
   So that: I can quickly replicate these successful account configurations without manually re-entering the same information.
```
3. **The agent will generate and execute the required code**.
4. **View the execution results** in the chat interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. 

Made with ❤️ by [Sri Kolagani](https://www.linkedin.com/in/sriharideep/) at [SFDC Brewery](https://sfdcbrewery.github.io/).

