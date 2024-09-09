function askOracle() {
    const questionInput = document.getElementById('question');
    const responseDiv = document.getElementById('response');

    const question = questionInput.value; // Get the question value
    responseDiv.innerHTML = ''; // Clear any previous response
    
    // Add loading spinner with text
    responseDiv.innerHTML = '<div class="spinner"></div>The oracle is pondering...';

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        responseDiv.innerHTML = ''; // Clear any loading messages
        typeWriterEffect(data.response || 'The oracle remains silent...'); // Render the response with the typewriter effect
    })
    .catch(error => {
        responseDiv.innerHTML = 'The oracle encountered an error.';
        console.error('Error:', error);
    });

    // Clear the input field after sending the question
    questionInput.value = '';
}

function typeWriterEffect(text) {
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = ''; // Clear any existing content
    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            responseDiv.innerHTML += text.charAt(i);
            i++;
            responseDiv.scrollTop = responseDiv.scrollHeight; // Auto-scroll to the bottom
            setTimeout(typeWriter, 50); // Speed of the typewriter effect
        }
    }
    typeWriter();
}


