import os
import csv
from datetime import datetime
import yaml

RULES_DIR = 'rules'
PROCESSED_DIR = 'processed_data'

def load_rules():
    rules = []
    for filename in os.listdir(RULES_DIR):
        if filename.endswith('_rule.yaml'):
            rule_file_path = os.path.join(RULES_DIR, filename)
            with open(rule_file_path, 'r') as rule_file:
                rule = yaml.safe_load(rule_file)
                rules.append(rule)
    return rules

def apply_rules_to_data(input_data, rules):
    for rule in rules:
        if rule['rule_type'] == 'capitalize':
            input_data[rule['output_field']] = input_data[rule['input_field']].capitalize()
        elif rule['rule_type'] == 'add_timestamp':
            input_data[rule['output_field']] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return input_data

def process_csv_file(input_file, output_file, rules):
    with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
        reader = csv.DictReader(csv_input)
        fieldnames = reader.fieldnames + [rule['output_field'] for rule in rules]
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row = apply_rules_to_data(row, rules)
            writer.writerow(row)

if __name__ == '__main__':
    rules = load_rules()
    input_file_path = 'input_data/input_data.csv'
    output_file_path = os.path.join(PROCESSED_DIR, 'processed_data.csv')
    process_csv_file(input_file_path, output_file_path, rules)
