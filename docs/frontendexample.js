const username = 'admin';
const password = 'secret';

const base64Credentials = btoa(`${username}:${password}`);


const requestOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        // Include the base64-encoded credentials in the Authorization header
        'Authorization': `Basic ${base64Credentials}`
    },
    body: JSON.stringify({
        conversation_id: "12345",  // Example conversation_id
        query: "What's the API endpoint for transactions?"  // Example user query
    })
};


fetch('https://vbot.up.railway.app/chat', requestOptions)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
