document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const exportBtn = document.getElementById('export-btn');
    const fileInput = document.getElementById('file-input');
    const clinicalNotes = document.getElementById('clinical-notes');
    const resultsContainer = document.getElementById('extracted-data');
    const statusIndicator = document.getElementById('status-indicator');
    const alertBar = document.getElementById('critical-alert-bar');

    // Tab Navigation Logic
    const tabs = ['mdu', 'safety', 'registry'];
    tabs.forEach(tab => {
        document.getElementById(`nav-${tab}`).addEventListener('click', () => {
            // Update Nav UI
            tabs.forEach(t => {
                document.getElementById(`nav-${t}`).classList.remove('active');
                document.getElementById(`section-${t}`).classList.remove('active');
            });
            document.getElementById(`nav-${tab}`).classList.add('active');
            document.getElementById(`section-${tab}`).classList.add('active');

            if (tab === 'registry') renderRegistry();
        });
    });

    let currentSessionData = null;
    let localRecords = JSON.parse(localStorage.getItem('medgemma_records') || '[]');

    // Copy to Clipboard (FHIR-like JSON)
    exportBtn.addEventListener('click', () => {
        if (!currentSessionData) return;
        navigator.clipboard.writeText(JSON.stringify(currentSessionData, null, 2));
        exportBtn.innerText = '✅ Copiado!';
        setTimeout(() => exportBtn.innerText = '📋 Copy FHIR JSON', 2000);
    });

    // Text Analysis
    analyzeBtn.addEventListener('click', async () => {
        const text = clinicalNotes.value.trim();
        if (!text) {
            alert('Por favor, insira uma nota clínica para análise.');
            return;
        }
        processRequest('http://localhost:8001/analyze', { text });
    });

    // File Upload Trigger
    uploadBtn.addEventListener('click', () => fileInput.click());

    // File Upload Handler
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        processRequest('http://localhost:8001/upload', formData, true);
    });

    async function processRequest(url, body, isFile = false) {
        // UI Loading State
        analyzeBtn.disabled = true;
        uploadBtn.disabled = true;
        exportBtn.disabled = true;
        alertBar.style.display = 'none';
        statusIndicator.innerHTML = '<span style="color: var(--secondary)">⚙️ Running Safety Audit...</span>';
        resultsContainer.innerHTML = '<div class="animate-fade" style="text-align: center; padding: 2rem;">Performing Neural Ingestion...</div>';

        try {
            const options = {
                method: 'POST',
                body: isFile ? body : JSON.stringify(body)
            };
            if (!isFile) {
                options.headers = { 'Content-Type': 'application/json' };
            }

            const response = await fetch(url, options);
            if (!response.ok) throw new Error('Falha no processamento');

            const data = await response.json();
            currentSessionData = data;

            // Save to Registry (Persistence)
            localRecords.unshift({
                timestamp: new Date().toLocaleString(),
                risk: data.risk_level,
                summary: (data.compliance_summary || "").substring(0, 100) + '...'
            });
            localStorage.setItem('medgemma_records', JSON.stringify(localRecords.slice(0, 5)));

            // Show Alert Bar if Critical
            if (data.risk_level === 'Critical' || data.risk_level === 'High') {
                alertBar.style.display = 'block';
                alertBar.innerText = `⚠️ CRITICAL COMPLIANCE RISK: ${data.risk_level.toUpperCase()}`;
            }

            renderResults(data);

        } catch (error) {
            statusIndicator.innerHTML = `<span style="color: var(--error)">❌ System Error: ${error.message}</span>`;
            resultsContainer.innerHTML = '<p style="text-align:center; color: var(--error);">Backend unreachable on :8001</p>';
        } finally {
            analyzeBtn.disabled = false;
            uploadBtn.disabled = false;
            exportBtn.disabled = false;
        }
    }

    function renderRegistry() {
        const list = document.getElementById('registry-list');
        if (localRecords.length === 0) {
            list.innerHTML = '<div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); text-align: center; padding: 4rem;">NO LOCAL RECORDS IN SECURE STORAGE.</div>';
            return;
        }

        list.innerHTML = localRecords.map(rec => `
            <div class="data-card animate-fade" style="display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.3);">
                <div>
                    <strong style="color: var(--secondary); font-family: var(--font-mono); font-size: 0.8rem;">[${rec.timestamp}]</strong>
                    <div style="color: var(--text-muted); font-size: 0.75rem; margin-top: 0.25rem;">${rec.summary}</div>
                </div>
                <span class="badge" style="background: ${getRiskColor(rec.risk)}; color: ${rec.risk === 'Critical' ? 'white' : 'var(--primary)'};">${rec.risk}</span>
            </div>
        `).join('');
    }

    function renderResults(data) {
        // Update Status
        statusIndicator.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(16, 185, 129, 0.1); padding: 0.75rem; border: 1px solid var(--accent);">
                <span style="font-weight: 800; color: var(--accent); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">✅ Analysis Cycle Complete</span>
                <span class="badge" style="background: ${getRiskColor(data.risk_level)}; color: white;">Audit: ${data.risk_level}</span>
            </div>
        `;

        // Render Entity Cards
        const entitiesHtml = data.entities.map(entity => `
            <div class="data-card animate-fade" style="border-left: 3px solid ${getStatusColor(entity.status)}; background: rgba(15, 23, 42, 0.4);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.25rem;">
                    <span style="font-weight: 800; color: var(--text-main); font-size: 0.75rem; text-transform: uppercase;">${entity.name}</span>
                    <span style="font-size: 0.65rem; color: var(--text-muted); font-family: var(--font-mono);">${entity.category}</span>
                </div>
                <div style="font-size: 1rem; color: var(--secondary); font-family: var(--font-mono); font-weight: 600;">${entity.value || 'NULL'}</div>
            </div>
        `).join('');

        const summaryHtml = `
            <div class="animate-fade" style="margin-top: 2rem; padding: 1.25rem; background: rgba(2, 6, 23, 0.8); border: 1px solid var(--ui-border); border-left: 4px solid var(--secondary);">
                <h4 style="font-size: 0.7rem; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; font-family: var(--font-mono);">Compliance Narrative // [PT-BR]</h4>
                <p style="font-size: 0.9rem; line-height: 1.6; color: var(--text-main);">${data.compliance_summary}</p>
            </div>
        `;

        resultsContainer.innerHTML = entitiesHtml + summaryHtml;
    }

    function getRiskColor(level) {
        switch (level) {
            case 'Critical': return '#f43f5e'; // Emergency Red
            case 'High': return '#f97316';     // Orange
            case 'Medium': return '#f59e0b';   // Amber
            case 'Low': return '#10b981';      // Mint
            default: return '#94a3b8';         // Slate
        }
    }

    function getStatusColor(status) {
        switch (status) {
            case 'success': return '#10b981';
            case 'alert': return '#f59e0b';
            case 'error': return '#f43f5e';
            default: return 'rgba(148, 163, 184, 0.2)';
        }
    }
});
