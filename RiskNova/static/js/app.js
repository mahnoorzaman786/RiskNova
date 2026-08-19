document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const predictBtn = document.getElementById('predictBtn');
    const resultContainer = document.getElementById('prediction-result');

    function setLoadingState() {
        if (predictBtn) {
            predictBtn.disabled = true;
            predictBtn.innerHTML = '🔄 Processing...';
            predictBtn.classList.add('loading');
        }

        if (form) {
            form.classList.add('is-submitting');
        }
    }

    function restoreButtonState() {
        if (predictBtn) {
            predictBtn.disabled = false;
            predictBtn.innerHTML = '🔮 Predict Project Risk';
            predictBtn.classList.remove('loading');
        }

        if (form) {
            form.classList.remove('is-submitting');
        }
    }

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            setLoadingState();

            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
            const formData = new FormData(form);

            try {
                const response = await fetch(form.action || window.location.href, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken || '',
                    },
                    credentials: 'same-origin',
                });

                const html = await response.text();

                if (response.ok) {
                    if (resultContainer) {
                        resultContainer.innerHTML = html;
                    }
                    if (form) {
                        form.style.display = 'none';
                    }
                    return;
                }

                if (resultContainer) {
                    resultContainer.innerHTML = html;
                }
            } catch (error) {
                if (resultContainer) {
                    resultContainer.innerHTML = '<div class="alert alert-danger">Prediction failed. Please try again.</div>';
                }
            } finally {
                restoreButtonState();
            }
        });
    }
});
