
document.addEventListener('DOMContentLoaded', function () {
    // --- Element References ---
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileUpload = document.getElementById('file-upload');
    const resultsSection = document.getElementById('results-section');
    const resultsContainer = document.getElementById('results-container');
    const spinner = document.getElementById('spinner');

    // --- Event Listeners ---
    fileUploadArea.addEventListener('click', () => fileUpload.click());
    fileUpload.addEventListener('change', handleFileAnalysis);

    // --- Core Functions ---

    /**
     * Handles the file selection and triggers the analysis process.
     */
    async function handleFileAnalysis() {
        if (fileUpload.files.length === 0) return;

        const file = fileUpload.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // --- Update UI for loading state ---
        spinner.classList.remove('d-none');
        resultsSection.classList.add('d-none');
        resultsContainer.innerHTML = '';

        try {
            const response = await fetch('/api/detect_tumor', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData,
            });

            const result = await response.json();

            if (!response.ok || result.error) {
                throw new Error(result.error || 'Terjadi kesalahan saat menganalisis gambar.');
            }
            
            displayDetectionResults(result);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            // --- Reset UI from loading state ---
            spinner.classList.add('d-none');
            // Reset file input to allow re-uploading the same file if needed
            fileUpload.value = null;
        }
    }

    /**
     * Displays the detection results in a new card.
     * @param {object} data The result data from the API.
     */
    function displayDetectionResults(data) {
        const confidencePercentage = data.confidence.toFixed(2);
        let alertClass = 'alert-info';
        if (data.prediction.toLowerCase().includes('no tumor')) {
            alertClass = 'alert-success';
        } else if (data.prediction.toLowerCase().includes('tumor')) {
            alertClass = 'alert-danger';
        }

        const resultCardHTML = `
            <div class="card shadow-lg">
                <div class="card-header">
                    <h4 class="mb-0">Hasil Deteksi</h4>
                </div>
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-6 text-center">
                            <h5 class="mb-3">Gambar yang Dianalisis</h5>
                            <img src="${data.image_url}" alt="Uploaded MRI Scan" class="img-fluid rounded shadow-sm" style="max-height: 400px;">
                        </div>
                        <div class="col-md-6">
                            <div class="alert ${alertClass} text-center py-3">
                                <h3 class="mb-0">${data.prediction}</h3>
                            </div>
                            <h5 class="mt-4">Tingkat Kepercayaan (Confidence)</h5>
                            <div class="progress" style="height: 30px;">
                                <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: ${confidencePercentage}%;" aria-valuenow="${confidencePercentage}" aria-valuemin="0" aria-valuemax="100">
                                    <strong>${confidencePercentage}%</strong>
                                </div>
                            </div>
                            <div class="text-muted mt-3">
                                <p><strong>Model:</strong> ${data.model_used}</p>
                                <p class="small">
                                    <strong>Disclaimer:</strong> Hasil ini dibuat oleh model AI dan tidak menggantikan diagnosis medis profesional.
                                    Selalu konsultasikan dengan dokter atau ahli radiologi untuk konfirmasi.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = resultCardHTML;
        resultsSection.classList.remove('d-none');
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});
