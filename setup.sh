#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Math Tutor...${NC}"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update the .env file with your email configuration.${NC}"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

# Create data directory
mkdir -p data

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "To start the application, run: ${YELLOW}python main.py${NC}"
echo -e "Access the web interface at: ${YELLOW}http://localhost:5000${NC}"
