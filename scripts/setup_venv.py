#!/usr/bin/env python3
"""
Setup Script for AI Attendance System
Automates virtual environment creation and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("AI Attendance System - Setup Script")
    print("=" * 60)
    print()
    
    # Check Python version
    print(f"Current Python version: {sys.version}")
    
    if sys.version_info[:2] != (3, 11):
        print()
        print("⚠️  WARNING: This script should be run with Python 3.11")
        print("Please use: py -3.11 scripts/setup_venv.py")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
            
    # Determine project root (parent directory of scripts/)
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print()
    print(f"Project root: {project_root}")
    print("Step 1: Creating virtual environment...")
    print("-" * 60)
    
    # Create venv in project root
    venv_path = project_root / "venv"
    if venv_path.exists():
        print("Virtual environment already exists. Skipping creation.")
    else:
        result = subprocess.run([sys.executable, "-m", "venv", "venv"])
        if result.returncode == 0:
            print("✓ Virtual environment created successfully")
        else:
            print("✗ Failed to create virtual environment")
            sys.exit(1)
    
    print()
    print("Step 2: Installing dependencies...")
    print("-" * 60)
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    # Upgrade pip
    print("Upgrading pip...")
    subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install dependencies
    if not (project_root / "requirements.txt").exists():
        print("✗ requirements.txt not found in project root!")
        sys.exit(1)

    print("\nInstalling requirements from requirements.txt...")
    result = subprocess.run([str(pip_path), "install", "-r", "requirements.txt"])
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print()
        print("To activate the virtual environment:")
        if os.name == 'nt':
            print("  venv\\Scripts\\activate")
        else:
            print("  source venv/bin/activate")
        print()
        print("Then run the application:")
        print("  python src/main.py") # Updated path
        print()
    else:
        print()
        print("✗ Installation failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
