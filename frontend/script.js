/**
 * Data Analysis Dashboard - Frontend Logic
 * Modern Analytics Dashboard with Sidebar Navigation
 */

// ==================== Configuration ====================
const API_BASE_URL = 'http://localhost:8000/api';

// ==================== State ====================
let selectedFile = null;
let currentDataset = null;

// ==================== DOM Elements ====================
// Navigation
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page-content');

// Upload elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const uploadBtn = document.getElementById('uploadBtn');
const loading = document.getElementById('loading');

// Header elements
const datasetName = document.getElementById('datasetName');
const refreshBtn = document.getElementById('refreshBtn');
const uploadNewBtn = document.getElementById('uploadNewBtn');

// Error message
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// ==================== Navigation ====================
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const pageName = item.dataset.page;
        switchPage(pageName);
    });
});

function switchPage(pageName) {
    // Update active nav item
    navItems.forEach(item => item.classList.remove('active'));
    document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

    // Show corresponding page
    pages.forEach(page => page.classList.remove('active'));
    const targetPage = document.getElementById(`${pageName}Page`);
    if (targetPage) {
        targetPage.classList.add('active');
    }
}

// ==================== File Upload ====================

// File input change
if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });
}

// Drag and drop
if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        handleFileSelect(file);
    });

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
}

// Upload button
if (uploadBtn) {
    uploadBtn.addEventListener('click', uploadFile);
}

// Header buttons
if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
        if (currentDataset) {
            location.reload();
        }
    });
}

if (uploadNewBtn) {
    uploadNewBtn.addEventListener('click', () => {
        switchPage('upload');
        resetUpload();
    });
}

// ==================== File Handling ====================

function handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    const validExtensions = ['.csv', '.xlsx', '.xls'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
        showError('Invalid file type. Please upload a CSV or Excel file (.csv, .xlsx, .xls)');
        return;
    }

    selectedFile = file;

    // Display file info
    if (fileName) fileName.textContent = file.name;
    if (fileSize) fileSize.textContent = formatFileSize(file.size);
    if (fileInfo) fileInfo.style.display = 'flex';

    hideError();
}

async function uploadFile() {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Show loading
        if (loading) loading.style.display = 'block';
        if (uploadBtn) uploadBtn.disabled = true;
        hideError();

        // Upload file
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }

        const data = await response.json();

        // Hide loading
        if (loading) loading.style.display = 'none';

        // Process the uploaded file
        await processDataset(data.filename);

    } catch (error) {
        if (loading) loading.style.display = 'none';
        if (uploadBtn) uploadBtn.disabled = false;
        showError(error.message);
    }
}

async function processDataset(filename) {
    try {
        currentDataset = filename;

        // Update header
        if (datasetName) datasetName.textContent = filename;

        // Fetch profile data
        const profileResponse = await fetch(`${API_BASE_URL}/profile/${filename}`);
        if (!profileResponse.ok) throw new Error('Failed to fetch profile');
        const profileData = await profileResponse.json();

        // Fetch statistics
        const statsResponse = await fetch(`${API_BASE_URL}/statistics/${filename}`);
        const statsData = statsResponse.ok ? await statsResponse.json() : null;

        // Fetch visualizations
        const vizResponse = await fetch(`${API_BASE_URL}/visualizations/${filename}`);
        const vizData = vizResponse.ok ? await vizResponse.json() : null;

        // Populate dashboard
        populateDashboard(profileData, statsData, vizData);
        populateOverview(profileData);
        populateStatistics(statsData);
        populateVisualizations(vizData);

        // Fetch and display insights
        await fetchAndDisplayInsights(filename);

        // Switch to dashboard
        switchPage('dashboard');

    } catch (error) {
        showError(error.message);
    }
}

// ==================== Dashboard Population ====================

function populateDashboard(profile, stats, viz) {
    // Update KPI cards
    const kpiRows = document.getElementById('kpiRows');
    const kpiColumns = document.getElementById('kpiColumns');
    const kpiNumeric = document.getElementById('kpiNumeric');
    const kpiMissing = document.getElementById('kpiMissing');

    if (kpiRows) kpiRows.textContent = profile.total_rows?.toLocaleString() || '0';
    if (kpiColumns) kpiColumns.textContent = profile.total_columns || '0';

    // Count numeric columns
    const numericCount = profile.columns?.filter(col => col.semantic_type === 'numerical').length || 0;
    if (kpiNumeric) kpiNumeric.textContent = numericCount;

    // Calculate missing percentage
    const totalCells = profile.total_rows * profile.total_columns;
    const missingCells = profile.total_missing || 0;
    const missingPercent = totalCells > 0 ? ((missingCells / totalCells) * 100).toFixed(1) : 0;
    if (kpiMissing) kpiMissing.textContent = `${missingPercent}%`;

    // Populate dashboard charts (placeholders for now)
    // You can add Plotly charts here later
}

function populateOverview(profile) {
    // Basic info
    const basicInfo = document.getElementById('basicInfo');
    if (basicInfo) {
        basicInfo.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Total Rows</div>
                <div class="stat-value">${profile.total_rows?.toLocaleString() || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Columns</div>
                <div class="stat-value">${profile.total_columns || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Memory Usage</div>
                <div class="stat-value">${formatFileSize(profile.memory_usage_bytes || 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Missing Values</div>
                <div class="stat-value">${profile.total_missing || 0}</div>
            </div>
        `;
    }

    // Column table
    const columnTable = document.getElementById('columnTable');
    if (columnTable && profile.columns) {
        const tbody = columnTable.querySelector('tbody');
        tbody.innerHTML = profile.columns.map(col => `
            <tr>
                <td><strong>${col.name}</strong></td>
                <td>${col.dtype}</td>
                <td><span class="type-badge type-${col.semantic_type}">${col.semantic_type}</span></td>
                <td>${col.non_null_count}</td>
                <td>${col.null_count}</td>
                <td>${col.null_percentage}%</td>
                <td>${col.unique_count}</td>
            </tr>
        `).join('');
    }

    // Preview table
    const previewTable = document.getElementById('previewTable');
    if (previewTable && profile.preview) {
        const headers = Object.keys(profile.preview[0] || {});
        previewTable.innerHTML = `
            <thead>
                <tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>
            </thead>
            <tbody>
                ${profile.preview.map(row => `
                    <tr>${headers.map(h => `<td>${row[h] !== null ? row[h] : '<em>null</em>'}</td>`).join('')}</tr>
                `).join('')}
            </tbody>
        `;
    }
}

function populateStatistics(stats) {
    if (!stats) return;

    // Dataset summary
    const datasetSummary = document.getElementById('datasetSummary');
    if (datasetSummary && stats.dataset_summary) {
        const summary = stats.dataset_summary;
        datasetSummary.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Total Numeric Columns</div>
                <div class="stat-value">${summary.total_numeric_columns || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Values Analyzed</div>
                <div class="stat-value">${summary.total_values_analyzed?.toLocaleString() || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Mean</div>
                <div class="stat-value">${summary.average_mean?.toFixed(2) || 'N/A'}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Std Dev</div>
                <div class="stat-value">${summary.average_std?.toFixed(2) || 'N/A'}</div>
            </div>
        `;
    }

    // Statistics table
    const statisticsTable = document.getElementById('statisticsTable');
    const noNumericMessage = document.getElementById('noNumericMessage');

    if (stats.column_statistics && Object.keys(stats.column_statistics).length > 0) {
        if (noNumericMessage) noNumericMessage.style.display = 'none';
        if (statisticsTable) {
            const tbody = statisticsTable.querySelector('tbody');
            tbody.innerHTML = Object.entries(stats.column_statistics).map(([col, stat]) => `
                <tr>
                    <td><strong>${col}</strong></td>
                    <td>${stat.count}</td>
                    <td>${stat.mean?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.median?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.mode?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.min?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.max?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.std?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.variance?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.q1?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.q2?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.q3?.toFixed(2) || 'N/A'}</td>
                    <td>${stat.range?.toFixed(2) || 'N/A'}</td>
                </tr>
            `).join('');
        }
    } else {
        if (noNumericMessage) noNumericMessage.style.display = 'block';
    }
}

function populateVisualizations(viz) {
    const chartsGrid = document.getElementById('chartsGrid');
    const noChartsMessage = document.getElementById('noChartsMessage');

    if (!viz || !viz.charts || viz.charts.length === 0) {
        if (noChartsMessage) noChartsMessage.style.display = 'block';
        if (chartsGrid) chartsGrid.innerHTML = '';
        return;
    }

    if (noChartsMessage) noChartsMessage.style.display = 'none';

    if (chartsGrid) {
        chartsGrid.innerHTML = viz.charts.map(chart => `
            <div class="chart-card">
                <h3 class="chart-title">${chart.title}</h3>
                <div class="chart-container" id="chart-${chart.id}"></div>
            </div>
        `).join('');

        // Render each chart with Plotly
        viz.charts.forEach(chart => {
            renderChart(chart);
        });
    }
}

// ==================== Insights Population ====================

async function fetchAndDisplayInsights(filename) {
    const insightsGrid = document.getElementById('insightsGrid');
    const noInsightsMessage = document.getElementById('noInsightsMessage');
    const insightSummary = document.getElementById('insightSummary');

    try {
        const response = await fetch(`${API_BASE_URL}/insights/${filename}`);
        if (!response.ok) throw new Error('Failed to fetch insights');
        const data = await response.json();

        if (!data.insights || data.insights.length === 0) {
            if (noInsightsMessage) noInsightsMessage.style.display = 'block';
            if (insightsGrid) insightsGrid.innerHTML = '';
            if (insightSummary) insightSummary.innerHTML = '';
            return;
        }

        if (noInsightsMessage) noInsightsMessage.style.display = 'none';

        // Render Summary Cards
        if (insightSummary) {
            insightSummary.innerHTML = `
                <div class="stat-card" style="border-left: 4px solid #ef4444;">
                    <div class="stat-label">High Severity</div>
                    <div class="stat-value" style="color: #ef4444;">${data.summary.high}</div>
                </div>
                <div class="stat-card" style="border-left: 4px solid #f59e0b;">
                    <div class="stat-label">Medium Severity</div>
                    <div class="stat-value" style="color: #f59e0b;">${data.summary.medium}</div>
                </div>
                <div class="stat-card" style="border-left: 4px solid #3b82f6;">
                    <div class="stat-label">Low Severity</div>
                    <div class="stat-value" style="color: #3b82f6;">${data.summary.low}</div>
                </div>
            `;
        }

        // Render Insight Cards
        if (insightsGrid) {
            insightsGrid.innerHTML = data.insights.map((insight, index) => `
                <div class="insight-card severity-${insight.severity}" style="animation-delay: ${index * 0.1}s" onclick="this.classList.toggle('expanded')">
                    <div class="insight-header">
                        <span class="insight-title">${insight.title}</span>
                        <span class="severity-badge">${insight.severity}</span>
                    </div>
                    <p class="insight-description">${insight.description}</p>
                    <div class="insight-footer">
                        <span class="insight-type">
                            <i class="fas fa-tag"></i> ${insight.type.replace('_', ' ')}
                        </span>
                        <span>Click to see evidence</span>
                    </div>
                    <div class="insight-evidence">
                        <strong>Evidence:</strong><br>
                        Metric: ${insight.evidence.metric}<br>
                        Value: ${insight.evidence.value}<br>
                        Threshold: ${insight.evidence.threshold}<br>
                        Target Columns: ${insight.columns.join(', ')}
                    </div>
                </div>
            `).join('');
        }

    } catch (error) {
        console.error('Error fetching insights:', error);
        if (noInsightsMessage) {
            noInsightsMessage.textContent = '⚠️ Error loading insights';
            noInsightsMessage.style.display = 'block';
        }
    }
}

// ==================== Utility Functions ====================

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function showError(message) {
    if (errorMessage && errorText) {
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }
}

function hideError() {
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
}

function resetUpload() {
    selectedFile = null;
    if (fileInput) fileInput.value = '';
    if (fileInfo) fileInfo.style.display = 'none';
    if (fileName) fileName.textContent = '';
    if (fileSize) fileSize.textContent = '';
    hideError();
}

// ==================== Initialization ====================
console.log('Data Analysis Dashboard - Initialized');
console.log('API Base URL:', API_BASE_URL);

// Set greeting based on time
function updateGreeting() {
    const hour = new Date().getHours();
    const greetingEl = document.querySelector('.greeting');
    if (greetingEl) {
        if (hour < 12) greetingEl.textContent = 'Good morning';
        else if (hour < 18) greetingEl.textContent = 'Good afternoon';
        else greetingEl.textContent = 'Good evening';
    }
}

updateGreeting();
