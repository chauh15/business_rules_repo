# app.py (continued)
from flask import Flask, request, jsonify

app = Flask(__name__)

# Placeholder for storing rules (in-memory storage, use a database in production)
rules = []

# GitHub repository information
github_repo_owner = 'chauh15'
github_repo_name = 'business_rules_repo'
github_token = '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'  # Replace with a valid GitHub personal access token

# GitHub API endpoint for updating files
# github_api_url = f'https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/amount_rule.yaml'
github_api_url = f'https://api.github.com/repos/chauh15/business_rules_repo/contents/amount_rule.yaml'


@app.route('/submit_rule', methods=['POST'])
def submit_rule():
    rule_data = request.json
    rules.append(rule_data)
    
    # TODO: Implement logic to update rules on GitHub
    # Update rules on GitHub
    update_rules_on_github()
    
    return jsonify({"message": "Rule submitted successfully"}), 200
    
def update_rules_on_github():
    # Convert the rules to YAML format
    yaml_content = rules_to_yaml()

    # Create a commit message
    commit_message = f'Update rules: {len(rules)} rules added/modified.'

    # Prepare headers with GitHub token
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json',
    }

    # Prepare data for the GitHub API request
    data = {
        'message': commit_message,
        'content': yaml_content,
        'sha': get_latest_sha_from_github(),
    }

    # Make a PUT request to update the file on GitHub
    response = requests.put(github_api_url, headers=headers, json=data)

    if response.status_code == 200:
        print('Rules updated on GitHub successfully.')
    else:
        print(f'Error updating rules on GitHub. Status Code: {response.status_code}, Response: {response.text}')

def get_latest_sha_from_github():
    # Make a GET request to fetch the latest commit SHA for the file
    response = requests.get(github_api_url, headers={'Authorization': f'Bearer {github_token}'})

    if response.status_code == 200:
        return response.json()['sha']
    else:
        print(f'Error fetching latest SHA from GitHub. Status Code: {response.status_code}, Response: {response.text}')
        return None

def rules_to_yaml():
    # Convert rules list to YAML format (simplified for demonstration)
    yaml_content = ''
    for rule in rules:
        yaml_content += f"rule_name: {rule['ruleName']}\n"
        # Add logic to convert other rule details to YAML format

    return yaml_content

@app.route('/webhook_receiver', methods=['POST'])
def webhook_receiver():
    # TODO: Process GitHub webhook payload and trigger StreamSets pipeline
    return jsonify({"message": "Webhook received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
