# ScrumBot-Agent

An AI agent built with Python that integrates with the Oxen AI platform for managing AI infrastructure.

## Prerequisites

Before running this program, ensure you have the following installed:

- **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
- **Git** - Download from [git-scm.com](https://git-scm.com/downloads)
- **OXEN_API_KEY** - You'll need an API key from [Oxen AI](https://hub.oxen.ai/)

## Installation Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ScrumBot-Agent
```

### Step 2: Set Up Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add your Oxen AI API key to the `.env` file:

```
OXEN_API_KEY=your_oxen_api_key_here
```

**Important:** Replace `your_oxen_api_key_here` with your actual Oxen AI API key.

## Running the Program

### Option 1: Run the Main Agent

```bash
python agent/agent.py
```

This will output: "Hello, Hackfrontier!"

### Option 2: Run the AI Chat Script

```bash
python scripts/execute.py
```

This script will:
- Connect to the Oxen AI platform using your API key
- Send a query to the GPT-4o-mini model
- Print the AI's response

## Project Structure

```
ScrumBot-Agent/
├── agent/
│   └── agent.py          # Main agent file
├── scripts/
│   └── execute.py        # AI chat execution script
├── utils/                # Utility functions (currently empty)
├── prompts/              # AI prompts (currently empty)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .venv/                # Virtual environment (created during setup)
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've activated the virtual environment and installed dependencies:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **API Key Error**: Ensure your `.env` file exists and contains the correct `OXEN_API_KEY`

3. **Permission Denied**: On macOS/Linux, you might need to make scripts executable:
   ```bash
   chmod +x scripts/execute.py
   ```

### Getting Help

If you encounter issues:

1. Check that all prerequisites are installed
2. Verify your virtual environment is activated
3. Ensure your API key is correctly set in the `.env` file
4. Check the Oxen AI documentation for API key setup

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

[Add your license information here]

## Support

For support, please [create an issue](link-to-issues) or contact the development team.
