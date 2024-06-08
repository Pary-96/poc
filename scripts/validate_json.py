import sys
import os
import json


def is_valid_json(file_path):
    try:
        with open(file_path, "r") as file:
            json.load(file)
        return True
    except json.JSONDecodeError as e:
        print(f"Error in {file_path}: {e}")
        return False


def main():
    pr_base_sha = os.getenv("GITHUB_BASE_SHA")
    pr_head_sha = os.getenv("GITHUB_HEAD_SHA")

    if not pr_base_sha or not pr_head_sha:
        print("Missing base or head SHA.")
        sys.exit(1)

    # Get the list of changed files between the two commits
    changed_files = (
        os.popen(f"git diff --name-only {pr_base_sha} {pr_head_sha}")
        .read()
        .splitlines()
    )
    print(f"Changed files: {changed_files}")  # Debug print
    invalid_files = []

    for file in changed_files:
        if file.endswith(".json"):
            print(f"Validating {file}")  # Debug print
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
