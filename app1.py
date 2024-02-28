from flask import Flask, request, jsonify
import os
import yaml

app = Flask(__name__)
RULES_DIR = 'rules'

@app.route('/submit_rule', methods=['POST'])
def submit_rule():
    rule_data = request.json
    rule_name = rule_data.get('rule_name')

    rule_file_path = os.path.join(RULES_DIR, f'{rule_name}_rule.yaml')
    with open(rule_file_path, 'w') as rule_file:
        yaml.dump(rule_data, rule_file)

    return jsonify({"message": "Rule submitted successfully"}), 200

if __name__ == '__main__':
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)
    app.run(debug=True)
