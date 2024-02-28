// script.js
function submitRule() {
    // Collect rule details from the form
    const ruleData = {
        ruleName: document.getElementById('ruleName').value,
        // Add logic to collect other rule details
    };

    // Send a POST request to the Flask API
    fetch('http://localhost:5000/submit_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(ruleData),
    })
    .then(response => response.json())
    .then(data => {
        // Display feedback to the user
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}