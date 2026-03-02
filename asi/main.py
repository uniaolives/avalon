#!/usr/bin/env python3
"""
Arkhe(n) – Artificial Substrate Intelligence (ASI)
Main entry point.
"""

import sys
import argparse
import os

# Add the current directory to sys.path to ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Arkhe(n) ASI System")
    parser.add_argument("--gui", action="store_true", help="Launch graphical interface")
    parser.add_argument("--cli", action="store_true", help="Launch command line interface (default)")
    args = parser.parse_args()

    if args.gui:
        from interface.gui import ArkheGUI
        app = ArkheGUI()
        app.run()
    else:
        from interface.cli import ArkheCLI
        ArkheCLI().cmdloop()

if __name__ == "__main__":
    main()
