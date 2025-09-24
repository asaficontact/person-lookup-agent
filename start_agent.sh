#!/bin/bash

# Kill any existing processes
echo "Cleaning up existing processes..."
pkill -f "python.*main.py"
pkill -f "nanda"
sleep 2

# Source virtual environment
source .venv/bin/activate

# Load environment variables
source .env

# Export them explicitly
export OPENAI_API_KEY=""  # ADD YOUR OPENAI API KEY HERE
export ANTHROPIC_API_KEY=""  # ADD YOUR ANTHROPIC API KEY HERE
export DOMAIN_NAME="person-lookup-agent.agents.tawab.dev"  # ADD YOUR DOMAIN NAME HERE

# Start the agent
echo "Starting PersonLookup agent..."
nohup python main.py > out.log 2>&1 &
echo "Agent started in background. Check out.log for enrollment link."
tail -f out.log
