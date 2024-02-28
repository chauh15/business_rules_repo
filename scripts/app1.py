from flask import Flask, request, jsonify
import os
import yaml
import requests
import subprocess

app = Flask(__name__)
RULES_DIR = 'rules'
GITHUB_REPO = 'your_username/your_repo'  # Replace with your GitHub username and repository name
GITHUB_TOKEN = 'your_github_token'  # Replace with your GitHub token

@app.route('/submit_rule', methods=['POST'])
def submit_rule():
    rule_data = request.json
    rule_name = rule_data.get('rule_name')

    rule_file_path = os.path.join(RULES_DIR, f'{rule_name}_rule.yaml')
    with open(rule_file_path, 'w') as rule_file:
        yaml.dump(rule_data, rule_file)

    commit_and_push_to_github(rule_file_path, rule_name)

    return jsonify({"message": "Rule submitted successfully"}), 200

def commit_and_push_to_github(rule_file_path, rule_name):
    try:
        # Add the new rule file to the Git repository
        subprocess.run(['git', 'add', rule_file_path])

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', f'Add rule: {rule_name}'])

        # Push the changes to the GitHub repository
        subprocess.run(['git', 'push', 'origin', 'master'])

        # Optional: Update GitHub directly using GitHub API
        update_github_directly(rule_file_path, rule_name)

    except Exception as e:
        print(f"Error committing and pushing to GitHub: {e}")

def update_github_directly(rule_file_path, rule_name):
    try:
        with open(rule_file_path, 'r') as rule_file:
            rule_content = rule_file.read()

        github_api_url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{RULES_DIR}/{rule_name}_rule.yaml'
        headers = {
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Content-Type': 'application/json',
        }

        github_data = {
            'message': f'Add rule: {rule_name}',
            'content': rule_content,
        }

        # PUT request to update GitHub directly
        response = requests.put(github_api_url, headers=headers, json=github_data)
        response.raise_for_status()

    except Exception as e:
        print(f"Error updating GitHub directly: {e}")

if __name__ == '__main__':
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)
    app.run(debug=True)
