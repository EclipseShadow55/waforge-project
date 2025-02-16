document.getElementById('adventure-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const params = new URLSearchParams();

    formData.forEach((value, key) => {
        params.append(key, value);
    });

    window.location.href = `page2.html?${params.toString()}`;
});