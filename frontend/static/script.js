/* script.js
    Behavior:
    - Upload & Preview posts file to /upload (unchanged)
    - On success we render preview and switch to "preview page" UI (history.pushState used)
    - Calculate posts file to /calculate (unchanged)
    - View map toggles the map view (no backend change required)
    - Reset clears state and returns to main page
*/

let uploadedFile = null;
let previewData = null;

// Render table (keeps your original logic but slightly hardened)
function renderTable(data) {
    const previewDiv = document.getElementById('preview');
    if (!previewDiv) return;

    if (!data) {
        previewDiv.innerHTML = `<p style="color:red">No data to preview.</p>`;
        return;
    }

    if (data.error) {
        previewDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
        return;
    }

    // message, rows, columns[], preview: [{col1:val, ...}, ...]
    let html = `<p style="color:#9ca3af; margin-bottom:8px">${data.message || 'Preview loaded'} (Rows: ${data.rows || (data.preview ? data.preview.length : 0)})</p>`;
    html += '<div class="preview-table-wrapper">';
    html += '<table><thead><tr>';
    (data.columns || []).forEach(col => html += `<th>${col}</th>`);
    html += '</tr></thead><tbody>';
    (data.preview || []).forEach(row => {
        html += '<tr>';
        (data.columns || []).forEach(col =>
            html += `<td>${(row[col] !== null && row[col] !== undefined) ? row[col] : ''}</td>`);
        html += '</tr>';
    });
    html += '</tbody></table></div>';
    previewDiv.innerHTML = html;
}

// Enable/disable the preview page buttons (and main page ones optionally)
function updateButtonStates(isUploaded) {
    // main page buttons
    const calculateBtn = document.getElementById('calculate-btn');
    const viewMapBtn = document.getElementById('view-map-btn');
    const resetBtn = document.getElementById('reset-btn');

    if (calculateBtn) calculateBtn.disabled = !isUploaded;
    if (viewMapBtn) viewMapBtn.disabled = !isUploaded;
    if (resetBtn) resetBtn.disabled = !isUploaded;

    // preview page buttons
    const calculateBtnPreview = document.getElementById('calculate-btn-preview');
    const viewMapBtnPreview = document.getElementById('view-map-btn-preview');
    const resetBtnPreview = document.getElementById('reset-btn-preview');

    if (calculateBtnPreview) calculateBtnPreview.disabled = !isUploaded;
    if (viewMapBtnPreview) viewMapBtnPreview.disabled = !isUploaded;
    if (resetBtnPreview) resetBtnPreview.disabled = !isUploaded;

    // show/hide preview-actions
    const previewActions = document.getElementById('preview-actions');
    if (previewActions) {
        if (isUploaded) previewActions.classList.remove('hidden');
        else previewActions.classList.add('hidden');
    }
}

// Switch UI view: "home", "preview", "map"
function setView(view) {
    // view: 'home' | 'preview' | 'map'
    if (view === 'preview') {
        document.body.classList.add('preview-mode');
        document.body.setAttribute('data-view', 'preview');
        history.pushState({view: 'preview'}, '', '?view=preview');
    } else if (view === 'map') {
        document.body.classList.add('preview-mode');
        document.body.setAttribute('data-view', 'map');
        history.pushState({view: 'map'}, '', '?view=map');
    } else {
        document.body.classList.remove('preview-mode');
        document.body.removeAttribute('data-view');
        history.pushState({view: 'home'}, '', window.location.pathname);
    }
}

// Upload & Preview handler
async function handleUploadPreview() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput || fileInput.files.length === 0) {
        alert("Please select a file to upload!");
        return;
    }

    uploadedFile = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
        document.getElementById('loading-spinner').classList.remove('hidden');
        document.getElementById('file-input-section').classList.add('hidden');

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        previewData = data;
        renderTable(data);
        updateButtonStates(true);

        // switch to preview-mode (no page reload — we keep uploadedFile so calculate works)
        setView('preview');
    } catch (error) {
        console.error('Upload failed:', error);
        document.getElementById('preview').innerHTML = `<p style="color:red">Upload failed. Please try again.</p>`;
        updateButtonStates(false);
    } finally {
        document.getElementById('loading-spinner').classList.add('hidden');
        document.getElementById('file-input-section').classList.remove('hidden');
    }
}

// Calculate handler (works whether on main or preview)
async function handleCalculate() {
    if (!uploadedFile) {
        alert("No file uploaded!");
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
        document.getElementById('loading-spinner').classList.remove('hidden');
        document.getElementById('file-input-section').classList.add('hidden');

        const response = await fetch('/calculate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        previewData = data;
        renderTable(data);
        updateButtonStates(true);

        // If user presses calculate from main, move to preview view to show results
        setView('preview');
    } catch (error) {
        console.error('Calculation failed:', error);
        document.getElementById('preview').innerHTML = `<p style="color:red">Calculation failed. Please try again.</p>`;
    } finally {
        document.getElementById('loading-spinner').classList.add('hidden');
        document.getElementById('file-input-section').classList.remove('hidden');
    }
}

// View Map handler: switches to map view and keeps previewData available for mapping
function handleViewMap() {
    window.open('/map', '_blank')
}

// Reset handler: clears uploaded file and preview and returns to home
function handleReset() {
    uploadedFile = null;
    previewData = null;

    // clear file input and preview DOM
    const fileInput = document.getElementById('fileInput');
    if (fileInput) fileInput.value = '';

    const previewDiv = document.getElementById('preview');
    if (previewDiv) previewDiv.innerHTML = '';

    document.getElementById('status-message').innerHTML = '';

    updateButtonStates(false);
    setView('home');
}

// On popstate (back/forward), restore UI based on state or url param
window.addEventListener('popstate', (e) => {
    const state = e.state;
    if (state && state.view) {
        if (state.view === 'preview') {
            // If we have previewData, show preview; otherwise go home
            if (previewData) {
                renderTable(previewData);
                updateButtonStates(true);
                document.body.classList.add('preview-mode');
                document.body.setAttribute('data-view', 'preview');
            } else {
                handleReset();
            }
        } else if (state.view === 'map') {
            if (previewData) {
                document.body.classList.add('preview-mode');
                document.body.setAttribute('data-view', 'map');
            } else {
                handleReset();
            }
        } else {
            handleReset();
        }
    } else {
        // no state (e.g. fresh load) — check url
        const params = new URLSearchParams(location.search);
        const view = params.get('view');
        if (view === 'preview' && previewData) {
            setView('preview');
            renderTable(previewData);
            updateButtonStates(true);
        } else if (view === 'map' && previewData) {
            setView('map');
        } else {
            setView('home');
        }
    }
});

// wire up listeners (including both main and preview buttons)
document.addEventListener('DOMContentLoaded', () => {
    // initial state
    updateButtonStates(false);

    // main page buttons
    const uploadBtn = document.getElementById('upload-preview-btn');
    if (uploadBtn) uploadBtn.addEventListener('click', handleUploadPreview);

    const calcBtn = document.getElementById('calculate-btn');
    if (calcBtn) calcBtn.addEventListener('click', handleCalculate);

   

    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) resetBtn.addEventListener('click', handleReset);

    // preview page buttons
    const calcBtnPreview = document.getElementById('calculate-btn-preview');
    if (calcBtnPreview) calcBtnPreview.addEventListener('click', handleCalculate);

    const viewBtnPreview = document.getElementById('view-map-btn-preview');
    if (viewBtnPreview) viewBtnPreview.addEventListener('click', handleViewMap);

    const resetBtnPreview = document.getElementById('reset-btn-preview');
    if (resetBtnPreview) resetBtnPreview.addEventListener('click', handleReset);

    // If the page was loaded with ?view=preview (rare) and previewData exists, show preview
    const params = new URLSearchParams(location.search);
    const view = params.get('view');
    if (view === 'preview' && previewData) {
        setView('preview');
        renderTable(previewData);
        updateButtonStates(true);
    }
});