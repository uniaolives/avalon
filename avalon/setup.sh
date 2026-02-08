#!/bin/bash

# Avalon Heartbeat - Quick Setup Script
# Run this to get started immediately

echo "🌊 AVALON HEARTBEAT - SETUP"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "❌ Python 3.9+ required"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.template .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
    echo "Get your keys from:"
    echo "  - Anthropic: https://console.anthropic.com/"
    echo "  - OpenAI: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press ENTER after you've added your API keys to .env..."
fi

# Create directories
echo "Creating data directories..."
mkdir -p data reports

# Run first pulse
echo ""
echo "🚀 Running first pulse..."
echo ""
python avalon_heartbeat.py

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "Your first report is in: reports/"
echo "Raw data is in: data/"
echo ""
echo "To run again: python avalon_heartbeat.py"
echo "To schedule daily: See README.md for cron/GitHub Actions setup"
echo ""
echo "🌊 The observation begins."
