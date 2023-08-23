document.addEventListener('DOMContentLoaded', function () {
    const output = document.getElementById('output');
    const apiKey = 'O5CIQQTPV1PC2QZM';
    let recognition;
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        recognition = new (webkitSpeechRecognition || SpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (event) {
            const result = event.results[0][0].transcript;
            const firstWord = result.split(' ')[0];
            output.textContent = `You said: ${firstWord}`;
            fetchStockSymbolData(apiKey, firstWord);
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
        };
    } else {
        output.textContent = 'Speech recognition is not supported in your browser.';
    }
    if (recognition) {
        recognition.start();
        output.textContent = 'Listening for voice input...';
    } else {
        output.textContent = 'Speech recognition is not available.';
    }
    function displayStockSymbolData(data) {
        output.innerHTML += '<hr>';
        output.innerHTML += '<h2>Stock Symbol Data:</h2>';
        data.bestMatches.forEach(match => {
            output.innerHTML += `<p>Symbol: ${match['1. symbol']}</p>`;
            output.innerHTML += `<p>Name: ${match['2. name']}</p>`;
            output.innerHTML += `<p>Type: ${match['3. type']}</p>`;
            output.innerHTML += `<p>Region: ${match['4. region']}</p>`;
            output.innerHTML += `<p>Market Open: ${match['5. marketOpen']}</p>`;
            output.innerHTML += `<p>Market Close: ${match['6. marketClose']}</p>`;
            output.innerHTML += `<p>Timezone: ${match['7. timezone']}</p>`;
            output.innerHTML += `<p>Currency: ${match['8. currency']}</p>`;
            output.innerHTML += `<p>Match Score: ${match['9. matchScore']}</p>`;
            output.innerHTML += '<hr>';
        });
    }
    window.fetchStockSymbolData = function (apiKey, keyword) {
        const apiUrl = `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${keyword}&apikey=${apiKey}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                displayStockSymbolData(data);
            })
            .catch(error => {
                console.error('Error fetching stock symbol data:', error);
                output.textContent = 'An error occurred while fetching stock symbol data.';
            });
    }
});
