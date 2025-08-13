#!/usr/bin/env python3
"""
Setup script for AI Menu Intelligence Widget Python Backend
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# OpenAI Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("OPENAI_MODEL=gpt-3.5-turbo\n")
            f.write("\n# Server Configuration\n")
            f.write("PORT=8000\n")
        print("✅ .env file created!")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up AI Menu Intelligence Widget Python Backend...")
    print()
    
    install_requirements()
    create_env_file()
    
    print()
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python main.py")
    print("3. Open: http://localhost:8000/docs for API documentation")
    print("4. Frontend will connect to: http://localhost:8000")

if __name__ == "__main__":
    main()
