# PersonLookup Agent

A sophisticated AI agent powered by OpenAI's Agents SDK that researches and compiles comprehensive information about individuals based on natural language queries.

## Features

- **Natural Language Input**: Simply describe who you're looking for in plain English
- **Intelligent Search**: Automatically generates and executes multiple search queries
- **Comprehensive Reports**: Creates detailed, well-structured markdown reports
- **Source Verification**: Cross-references information from multiple credible sources
- **Privacy-Conscious**: Focuses only on publicly available information
- **Streaming Support**: Option to see results as they're generated

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd person-lookup-agent
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Set up your API keys:
```bash
# Create a .env file
cp env.example .env

# Edit .env and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # For NANDA deployment
DOMAIN_NAME=your-domain.com  # For NANDA deployment
```

## Usage

### Local Testing

Test the agent locally before deployment:

```bash
# Test with a query
python main.py --test "Tell me about Ada Lovelace"

# Show help
python main.py --help
```

### NANDA Deployment (Internet of Agents)

Deploy your PersonLookup agent to the global NANDA network:

1. **Set up SSL certificates** (required for NANDA):
```bash
# Generate certificates for your domain
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to project directory
sudo cp -L /etc/letsencrypt/live/your-domain.com/fullchain.pem .
sudo cp -L /etc/letsencrypt/live/your-domain.com/privkey.pem .
sudo chown $USER:$USER fullchain.pem privkey.pem
chmod 600 fullchain.pem privkey.pem
```

2. **Set environment variables**:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DOMAIN_NAME="your-domain.com"
```

3. **Start the NANDA-wrapped agent**:
```bash
# Run in foreground
python main.py

# Or run in background
nohup python main.py > agent.log 2>&1 &
```

4. **Get your enrollment link** from the logs:
```bash
cat agent.log | grep "enrollment"
```

Your agent will now be:
- **Persistent**: Runs continuously on your server
- **Discoverable**: Listed in the MIT NANDA Index
- **Interoperable**: Can communicate with other agents using @agent_id syntax

### Standalone Usage (without NANDA)

For local development or standalone usage:

```bash
# Direct query
python main.py "Tell me about Elon Musk"

# Demo mode with examples
python main.py --demo
```

### Python API

Use the agent in your own Python code:

```python
from person_lookup import PersonLookupAgent

# Initialize the agent
agent = PersonLookupAgent()

# Look up a person
result = agent.lookup_person("Find information about Tim Cook, CEO of Apple")

if result["success"]:
    print(result["report"])
else:
    print(f"Error: {result['error']}")
```

### Streaming Results

For streaming results (currently returns full result):

```python
agent = PersonLookupAgent()

for chunk in agent.lookup_person_stream("Tell me about Marie Curie"):
    print(chunk, end="", flush=True)
```

## Report Structure

The agent generates comprehensive reports with the following sections:

- **Personal Information**: Name, birth details, location
- **Professional Background**: Current and previous positions
- **Education**: Degrees, institutions, certifications
- **Notable Achievements**: Awards, recognitions, accomplishments
- **Publications and Works**: Books, papers, patents
- **Online Presence**: Official websites, social media
- **Recent Activities**: Latest news and developments
- **Sources**: All references used in the report

## Architecture

### Components

1. **PersonLookupAgent Class** (`person_lookup.py`)
   - Main agent implementation
   - Handles API initialization and prompt loading
   - Provides synchronous and streaming interfaces

2. **Prompt Template** (`prompts/person_lookup_prompt.jinja2`)
   - Detailed instructions for the agent
   - Structured report format
   - Search strategy guidelines

3. **Main Entry Point** (`main.py`)
   - CLI interface
   - Demo examples
   - Error handling

### Tools Used

- **WebSearchTool**: Built-in OpenAI Agents SDK tool for web searches
- **Jinja2**: Template engine for dynamic prompt generation
- **python-dotenv**: Secure environment variable management

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Override default model (optional, default: gpt-4o-mini)

### Customizing the Prompt

Edit `prompts/person_lookup_prompt.jinja2` to customize:
- Report format and sections
- Search strategies
- Information priorities
- Output style

## Best Practices

1. **Be Specific**: Include context like profession, company, or time period
2. **Handle Ambiguity**: The agent will ask for clarification if multiple people match
3. **Verify Information**: Reports include source citations for verification
4. **Respect Privacy**: The agent only uses publicly available information

## Examples

```bash
# Tech industry leaders
python main.py "Satya Nadella, CEO of Microsoft"

# Historical figures
python main.py "Ada Lovelace, the first computer programmer"

# Scientists and researchers
python main.py "Find information about Dr. Jane Goodall and her work with primates"

# Multiple people with same name
python main.py "John Smith who works at NASA as an engineer"
```

## Error Handling

The agent handles various error scenarios:
- Missing API key
- Network issues
- Invalid queries
- No results found
- Rate limiting

All errors are returned with descriptive messages and suggestions for resolution.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

[Your License Here]

## Acknowledgments

Built with:
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [OpenAI API](https://openai.com)
- [Jinja2](https://jinja.palletsprojects.com/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
