from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yaml
import requests
import subprocess

app = Flask(__name__)
CORS(app)
RULES_DIR = 'rules'
GIT_DIR = 'business_rules_repo'
GITHUB_REPO = 'chauh15/business_rules_repo'  # Replace with your GitHub username and repository name
GITHUB_TOKEN = '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'  # Replace with your GitHub token
# GitHub API endpoint for updating files
# github_api_url = f'https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/amount_rule.yaml'
# github_api_url = f'https://api.github.com/repos/chauh15/business_rules_repo/contents/amount_rule.yaml'

@app.route('/submit_rule', methods=['POST'])
def submit_rule():
    rule_data = request.json
    rule_name = rule_data.get('ruleName')
    #print(rule_name)

    rule_file_path = os.path.join(RULES_DIR, f'{rule_name}_rule.yaml')
    #print("Rule File Path:", rule_file_path)
    with open(rule_file_path, 'w') as rule_file:
        yaml.dump(rule_data, rule_file)
        commit_and_push_to_github(rule_file_path, rule_name)
    return jsonify({"message": "Rule submitted successfully"}), 200

def commit_and_push_to_github(rule_file_path, rule_name):
    try:
        # Add the new rule file to the Git repository
        #subprocess.run(['git', 'add', rule_file_path])
        #subprocess.run(['git', 'add', GIT_DIR])

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', f'Add rule: {rule_name}'])

        # Push the changes to the GitHub repository
        subprocess.run(['git', 'push', 'origin', 'master'])

        # Optional: Update GitHub directly using GitHub API
        #update_github_directly(rule_file_path, rule_name)

    except Exception as e:
        print(f"Error committing and pushing to GitHub: {e}")

'''def update_github_directly(rule_file_path, rule_name):
    try:
        with open(rule_file_path, 'r') as rule_file:
            rule_content = rule_file.read()

        github_api_url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{RULES_DIR}/{rule_name}_rule.yaml'
        #github_api_url = f'https://api.github.com/chauh15/business_rules_repo/contents/{RULES_DIR}/{rule_name}_rule.yaml'
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
        print(f"Error updating GitHub directly: {e}")'''

if __name__ == '__main__':
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)
    app.run(debug=True)