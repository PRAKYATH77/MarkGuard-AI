# 🛡️ MarkGuard AI - AI-Powered IC Authentication System

> **Intelligent Real-Time Counterfeit Detection for Integrated Circuits**

An enterprise-grade full-stack application that leverages **artificial intelligence and computer vision** to detect counterfeit integrated circuits (ICs) with high accuracy. This system combines **real EasyOCR**, image quality analysis, and datasheet validation to provide professional IC authentication.

**Perfect for:** Manufacturing quality assurance, supply chain verification, and electronics retailers.

---

## 🎯 Key Features

✨ **Real-Time IC Authentication**
- Upload IC chip images and get instant GENUINE/COUNTERFEIT verdict
- Confidence scoring based on multiple validation checks

🤖 **AI-Powered Analysis**
- Real EasyOCR integration for accurate text recognition
- Manufacturer logo detection and verification
- Blur detection to identify print quality issues
- Pattern matching against official datasheets

📊 **Dynamic Dashboard**
- Real-time statistics updating every 2 seconds
- Track total scans, genuine ICs, counterfeits found
- Calculate yield rate percentage
- Beautiful stat cards with color-coded badges

💡 **Intelligent Explanations**
- AI-generated insights explaining verdict reasoning
- Shows exactly why an IC passed or failed validation
- Detailed detection breakdown (manufacturer, logo, text, quality)

🎨 **Professional UI/UX**
- Modern responsive design with gradient aesthetics
- Smooth animations and transitions
- Professional card layouts with hover effects
- Mobile-friendly interface

---

## 🏗️ Architecture & Technology Stack

### **Backend - FastAPI (Production-Ready)**
```
- FastAPI: High-performance Python web framework (async)
- EasyOCR: Real-time optical character recognition
- OpenCV: Advanced image processing & blur detection
- Uvicorn: ASGI server with auto-reload
- Python-dotenv: Secure environment configuration
```

### **Frontend - React 18 (Modern & Optimized)**
```
- React 18: Component-based UI with hooks
- Axios: HTTP client for API communication
- Tailwind CSS: Utility-first CSS framework
- CSS3 Animations: Smooth transitions & effects
```

### **Database - Flexible Storage**
```
- Mock In-Memory: Perfect for demo/testing (no setup required)
- MongoDB Ready: Easy upgrade path for production deployments
```

---

## 🎓 How It Works

```
User Uploads IC Image + Part Number
          ↓
EasyOCR reads text from image
          ↓
OpenCV analyzes image quality (blur detection)
          ↓
Backend fetches expected specs from datasheet
          ↓
Intelligent validator checks: Logo match? Text match? Quality OK?
          ↓
Returns: GENUINE/COUNTERFEIT with confidence & explanation
          ↓
Stats updated in real-time on dashboard
```

---

## 📋 Supported IC Components (Expandable)

Currently supporting these part numbers (easily expandable):

| Part Number | Manufacturer | Component Type |
|-------------|--------------|-----------------|
| **NE555DR** | Texas Instruments | Precision Timer |
| **LM7805** | Fairchild | Voltage Regulator |
| **ATMEGA328P** | Microchip | 8-bit Microcontroller |

*→ Add more part numbers to `backend/app/core/scraper.py` to expand database*

---

## 🚀 Getting Started

### Prerequisites
```
✓ Python 3.8 or higher
✓ Node.js 14+ with npm
✓ 2GB RAM minimum
```

### Installation & Running

**1️⃣ Clone Repository**
```bash
git clone https://github.com/PRAKYATH77/MarkGuard-AI.git
cd MarkGuard-AI
```

**2️⃣ Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python main.py
```
✓ Backend runs on: `http://localhost:8000`

**3️⃣ Frontend Setup** (New Terminal)

**1. Clone the repository**
```bash
git clone https://github.com/PRAKYATH77/MarkGuard-AI.git
cd MarkGuard-AI
```

**2. Setup Backend**
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on: `http://localhost:8000`

**3. Setup Frontend** (in new terminal)
```bash
cd frontend
npm install
npm start
```
Frontend runs on: `http://localhost:3000`

## 💻 Usage

1. **Open** http://localhost:3000 in your browser
2. **Upload** an IC chip image (JPG/PNG)
3. **Enter** the part number (e.g., NE555DR)
4. **Click** "🔍 SCAN IC"
5. **View Results**:
   - ✅ GENUINE or ❌ COUNTERFEIT verdict
   - 📊 Confidence score
   - 📖 AI explanation
   - 🔍 Detection details (manufacturer, logo, text found, image quality)

## 📊 Dashboard Statistics

The dashboard displays real-time metrics:
- **Total Scanned**: Total number of ICs analyzed
- **Genuine ICs**: Count of verified authentic ICs
- **Counterfeit Found**: Count of detected counterfeits
- **Yield Rate**: Percentage of genuine vs total scans

## 🔧 API Endpoints

### POST `/api/v1/scan-ic`
Scan and verify an IC chip
```bash
curl -X POST http://localhost:8000/api/v1/scan-ic \
  -F "file=@chip_image.jpg" \
  -F "part_number=NE555DR"
```

**Response:**
```json
{
  "file_id": "uuid",
  "part_number": "NE555DR",
  "status": "PASS",
  "confidence": 98.5,
  "explanation": "All authenticity checks passed...",
  "detected_data": {
    "manufacturer": "Texas Instruments",
    "expected_logo": "Ti",
    "image_quality": "Clear",
    "detected_texts": ["NE555DR", "USA", "BATCH2024"]
  },
  "issues": []
}
```

### GET `/api/v1/stats`
Get current statistics
```bash
curl http://localhost:8000/api/v1/stats
```

**Response:**
```json
{
  "total_scanned": 5,
  "genuine": 4,
  "counterfeit": 1,
  "yield_rate": 80.0
}
```

## 🏗️ Project Structure

```
MarkGuard-AI/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── app/
│       ├── api/             # API endpoints
│       │   ├── scan.py       # IC scanning endpoint
│       │   ├── stats.py      # Statistics endpoint
│       │   └── history.py    # Scan history endpoint
│       ├── core/            # Business logic
│       │   ├── validator.py  # IC validation logic
│       │   ├── scraper.py    # Datasheet info retrieval
│       │   └── config.py     # Configuration
│       └── database/        # Database operations
│           └── connection.py # Mock database collection
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── index.js         # React entry point
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js   # Tailwind CSS config
└── README.md
```

## 🔍 How It Works

1. **Image Upload**: User uploads IC chip image
2. **OCR Analysis**: EasyOCR reads text from the image
3. **Quality Check**: OpenCV detects image blur
4. **Datasheet Lookup**: Retrieves expected specs for part number
5. **Validation**: Compares OCR results with datasheet
6. **Verdict**: Returns GENUINE if all checks pass, COUNTERFEIT otherwise
7. **Explanation**: AI generates detailed reasoning for the verdict

## 🎓 Key Validation Checks

- ✓ Part number matches expected specs
- ✓ Manufacturer logo clearly visible
- ✓ Image quality is clear (not blurry)
- ✓ Text OCR confidence is high

## 🚀 Production Deployment

To deploy to production:

1. **Backend**: Deploy FastAPI to cloud (Heroku, AWS, GCP, Azure)
2. **Frontend**: Build and deploy React to CDN (Vercel, Netlify)
3. **Database**: Connect to MongoDB Atlas for persistent data
4. **Environment**: Set proper `.env` variables for production URLs

## 📝 Environment Variables

Create `.env` file in `backend/`:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=markguard_db
PROJECT_NAME=MarkGuard AI
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more IC part numbers
- Enhance validation logic
- Improve UI/UX
- Add more features

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**PRAKYATH77** - Full-Stack AI Developer

GitHub: [PRAKYATH77](https://github.com/PRAKYATH77)

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ for IC Authentication**