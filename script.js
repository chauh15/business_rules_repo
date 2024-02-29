// script.js
function submitRule() {
    // Collect rule details from the form
    const ruleData = {
        ruleName: document.getElementById('ruleName').value,
        // Add logic to collect other rule details
		input_field: document.getElementById('inputField').value,
        output_field: document.getElementById('outputField').value,
        rule_type: document.getElementById('ruleType').value
    };

    // Send a POST request to the Flask API
    fetch('http://localhost:5000/submit_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(ruleData)
    })
    .then(response => response.json())
    .then(data => {
        // Display feedback to the user
        alert(data.message);
		// Optionally, update UI or perform additional actions after successful submission
    })
    .catch(error => {
        console.error('Error submitting rule:', error);
        alert('Error submitting rule. Check console for details.');
    });
}