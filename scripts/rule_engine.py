import yaml

def load_rules(filename):
  with open(filename, 'r') as f:
    return yaml.safe_load(f)

def apply_rules(data, rules):
  for rule in rules:
    if evaluate_condition(data, rule['conditions']):
      data = apply_action(data, rule['actions'])
  return data

def evaluate_condition(data, conditions):
  # Implement logic to evaluate conditions based on field, operator, and value
  # (This example assumes simple comparison)
  field, operator, value = conditions[0]  # Assuming single condition for simplicity
  return data[field] if operator == ">" else 0  # Replace with actual comparison logic

def apply_action(data, actions):
  # Implement logic to apply actions (This example modifies a field)
  action = actions[0]
  data[action['field']] = eval(action['expression'])  # Replace with safe evaluation
  return data

# Example usage
if __name__ == "__main__":
  rules = load_rules("discount_rule.yaml")
  order_data = {"order_total": 120}
  processed_data = apply_rules(order_data.copy(), rules)
  print(f"Original order total: ${order_data['order_total']}")
  print(f"Processed order total: ${processed_data['order_total']}")
