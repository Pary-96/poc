import sys
import os
import json


def is_valid_json(file_path):
    try:
        with open(file_path, "r") as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_json.py <base_sha> <head_sha>")
        sys.exit(1)

    base_sha = sys.argv[1]
    head_sha = sys.argv[2]

    # Get the list of changed files between the two commits
    changed_files = (
        os.popen(f"git diff --name-only {base_sha} {head_sha}").read().splitlines()
    )
    invalid_files = []

    for file in changed_files:
        if file.endswith(".json"):
            print(f"Validating {file}")
            if not is_valid_json(file):
                invalid_files.append(file)

    if invalid_files:
        print("Invalid JSON files detected:")
        for file in invalid_files:
            print(f" - {file}")
        sys.exit(1)
    else:
        print("All JSON files are valid")


if __name__ == "__main__":
    main()
