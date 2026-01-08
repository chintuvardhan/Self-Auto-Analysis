# 📊 Data Analysis Web Application

A powerful, rule-based data analysis system built completely from scratch **without using any AI APIs or external AI services at runtime**.

## 🎯 Project Overview

This application allows users to upload CSV or Excel files and automatically performs:
- Dataset profiling and metadata extraction
- Statistical analysis
- Automatic visualization generation
- Rule-based insights (NO AI-generated text)

**Current Status:** Phase 1 Complete ✅

## 🚀 Phase 1: File Upload & Dataset Profiling

### Features Implemented

✅ **File Upload**
- Support for CSV (.csv) and Excel (.xlsx, .xls) files
- Drag-and-drop interface
- File validation and error handling

✅ **Dataset Profiling**
- Number of rows and columns
- Column names and data types
- Semantic type detection (numerical, categorical, text, datetime, boolean)
- Missing value analysis (null counts and percentages)
- Unique value counts
- First 10 rows preview

✅ **Modern UI**
- Dark theme with vibrant accents
- Smooth animations and transitions
- Responsive design for all devices
- Real-time feedback and loading states

## 📁 Project Structure

```
data-analysis-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # API endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── profiler.py      # Dataset profiling logic
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py    # File validation utilities
│   ├── uploads/                 # Temporary file storage
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html              # Main UI
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
└── README.md                   # This file
```

## 🛠 Technology Stack

### Backend
- **Framework:** FastAPI
- **Data Processing:** pandas, numpy
- **Excel Support:** openpyxl
- **Server:** uvicorn

### Frontend
- **HTML5** for structure
- **CSS3** for styling (modern, responsive design)
- **Vanilla JavaScript** for logic (no frameworks)

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to Project Directory

```bash
cd data-analysis-app
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run the Application

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## 🎮 Usage

1. **Upload a File**
   - Click "Choose File" or drag and drop a CSV/Excel file
   - Supported formats: `.csv`, `.xlsx`, `.xls`

2. **View Results**
   - Dataset overview (rows, columns, file size)
   - Column information (data types, null values, unique counts)
   - Data preview (first 10 rows)

3. **Analyze Different Files**
   - Simply upload another file to analyze it

## 📡 API Documentation

### Endpoints

#### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Data Analysis API is running",
  "phase": "1 - File Upload & Dataset Profiling"
}
```

#### `POST /api/upload`
Upload a CSV or Excel file

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "example.csv",
  "profile": {
    "basic_info": {
      "num_rows": 1000,
      "num_columns": 10,
      "file_size_bytes": 52428,
      "file_size_mb": 0.05
    },
    "columns": [...],
    "preview": {...}
  }
}
```

#### `GET /api/profile/{filename}`
Get profile of a previously uploaded file

**Response:**
```json
{
  "filename": "example.csv",
  "profile": {...}
}
```

#### `DELETE /api/delete/{filename}`
Delete an uploaded file

**Response:**
```json
{
  "message": "File deleted successfully",
  "filename": "example.csv"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI:** `http://localhost:8000/api/docs`
- **ReDoc:** `http://localhost:8000/api/redoc`

## 🧠 Core Principles

✅ **No AI APIs** - No OpenAI, Gemini, or any external AI services  
✅ **Rule-Based Logic** - All analysis uses deterministic algorithms  
✅ **Clean Code** - Well-documented, modular, maintainable  
✅ **Production Quality** - Proper error handling and validation  
✅ **Phase-wise Development** - One feature at a time  

## 🗺 Future Phases (Planned)

### Phase 2: Statistics Engine
- Descriptive statistics (mean, median, mode, std dev)
- Distribution analysis
- Correlation matrix
- Statistical tests

### Phase 3: Visualization Engine
- Automatic chart type selection
- Interactive plots (using plotly)
- Distribution plots
- Correlation heatmaps
- Time series visualizations

### Phase 4: Insight Rules Engine
- Rule-based pattern detection
- Anomaly detection
- Trend identification
- Automated textual insights

### Phase 5: UI Integration & Polish
- Enhanced dashboard
- Export functionality
- Comparison features
- Advanced filtering

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 is already in use, run the server on a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

Then update the `API_BASE_URL` in `frontend/script.js`:
```javascript
const API_BASE_URL = 'http://localhost:8001/api';
```

### CORS Issues
If you encounter CORS errors, ensure the backend is running and the `API_BASE_URL` in `script.js` matches your server URL.

### File Upload Fails
- Ensure the file is a valid CSV or Excel file
- Check file size (max 100 MB)
- Verify the `uploads` directory exists and has write permissions

## 📝 Code Quality

- **Type Hints:** Python code uses type hints for clarity
- **Docstrings:** All functions have comprehensive docstrings
- **Comments:** Complex logic is well-commented
- **Error Handling:** Robust error handling throughout
- **Validation:** Input validation at all entry points

## 🤝 Contributing

This is a learning project built phase-by-phase. Each phase is implemented completely before moving to the next.

## 📄 License

This project is open source and available for educational purposes.

## 🎓 Learning Outcomes

By building this project, you'll learn:
- FastAPI backend development
- Pandas data manipulation
- Modern frontend design
- API design and documentation
- Rule-based analysis techniques
- Clean code principles

---

**Built with ❤️ using Python, FastAPI, and Vanilla JavaScript**

**No AI APIs • Rule-Based Analysis • Open Source**
