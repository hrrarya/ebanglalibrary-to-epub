document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scrape-form');
    const urlInput = document.getElementById('url');
    const errorMessage = document.getElementById('error-message');
    const submitBtn = document.getElementById('submit-btn');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result');
    const bookTitle = document.getElementById('book-title');
    const downloadBtn = document.getElementById('download-btn');

    // Pattern: https://www.ebanglalibrary.com/lessons//lesson-name
    // We allow any characters after the double slash
    // Pattern: https://www.ebanglalibrary.com/lessons/lesson-name
    // This is a valid example:
    // https://www.ebanglalibrary.com/lessons/%e0%a7%a6%e0%a7%a7-%e0%a6%ae%e0%a6%a8-%e0%a6%a8%e0%a6%bf%e0%a6%af%e0%a6%bc%e0%a6%a8%e0%a7%8d%e0%a6%a4%e0%a7%8d%e0%a6%b0%e0%a6%a3/
    // Require exactly one slash after /lessons/
    const urlPattern = /^https:\/\/www\.ebanglalibrary\.com\/lessons\/[^\/][^ ]*\/?$/;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();

        // Basic validation
        if (!urlPattern.test(url)) {
            errorMessage.classList.remove('error-hidden');
            urlInput.classList.add('invalid');
            return;
        }

        // Reset UI
        errorMessage.classList.add('error-hidden');
        urlInput.classList.remove('invalid');
        submitBtn.disabled = true;
        resultSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        // const api_url = 'http://23.94.117.217:23223'
        try {
            // Note: Adjust the API URL if the backend is on a different port/host
            const form_data = new FormData();
            form_data.append('url', url);
            const response = await fetch('/get-download-link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ url: url }),
            });

            console.log(response);

            const data = await response.json();

            if (data.success) {
                bookTitle.textContent = data.title;
                downloadBtn.href = data.download_link;
                
                loadingSection.classList.add('hidden');
                resultSection.classList.remove('hidden');
            } else {
                alert('Error: ' + (data.error || 'Failed to get download link'));
                loadingSection.classList.add('hidden');
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred while connecting to the server.');
            loadingSection.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    // Clear error message on input
    urlInput.addEventListener('input', () => {
        if (!errorMessage.classList.contains('error-hidden')) {
            errorMessage.classList.add('error-hidden');
            urlInput.classList.remove('invalid');
        }
    });
});
