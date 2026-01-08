# 🚀 Quick Start Guide

## Run the Application

### 1. Navigate to Backend Directory
```bash
cd data-analysis-app/backend
```

### 2. Start the Server
```bash
uvicorn app.main:app --reload
```

### 3. Open in Browser
```
http://localhost:8000
```

---

## Expected Server Output

```
============================================================
Data Analysis Web Application - Backend Server
Phase 1: File Upload & Dataset Profiling
============================================================
Uploads directory: C:\Users\91728\Desktop\SELT AUTO Analysis\data-analysis-app\backend\uploads
Frontend directory: C:\Users\91728\Desktop\SELT AUTO Analysis\data-analysis-app\frontend
Server is ready to accept requests!
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## How to Use

1. **Upload File**: Drag & drop or click to select CSV/Excel file
2. **Click "Upload & Analyze"**: Wait for processing
3. **View Results**: See dataset overview, column info, and preview

---

## Supported File Types

✅ CSV (.csv)  
✅ Excel (.xlsx, .xls)  
❌ Other formats not supported

---

## API Endpoints

- `GET /api/health` - Check server status
- `POST /api/upload` - Upload and profile dataset
- `GET /api/profile/{filename}` - Get existing profile
- `DELETE /api/delete/{filename}` - Delete uploaded file

---

## Interactive API Docs

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## Stop the Server

Press `Ctrl+C` in the terminal
