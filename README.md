# Drag Race Tournament Manager - Web Version

A comprehensive web-based drag race tournament management system built with Flask. Features complete tournament management including driver registration, race recording, championship functionality, and detailed statistics tracking.

## 🏁 Features

### Driver Management
- ✅ Add and manage drivers across multiple divisions
- ✅ Edit driver information (name, division)
- ✅ Delete drivers from tournaments
- ✅ Track win/loss records and win ratios
- ✅ Driver status tracking (Active, Eliminated, Inactive)
- ✅ Division-based driver filtering

### Race Management
- ✅ Record regular races between two drivers
- ✅ Record championship races (3-driver eliminations)
- ✅ Automatic win/loss tracking
- ✅ Race history with timestamps
- ✅ Division-specific race organization

### Tournament Features
- ✅ Live tournament rankings by division
- ✅ Win ratio calculations and percentages
- ✅ Tournament statistics dashboard
- ✅ Driver elimination tracking (3 losses = eliminated)
- ✅ Championship race functionality
- ✅ Division management system

### Data Management
- ✅ Export results to Excel (.xlsx format)
- ✅ Export results to CSV
- ✅ Import drivers from Excel files
- ✅ Save/load tournament data (JSON)
- ✅ Sample data loading for testing

### User Interface
- ✅ Responsive web design (works on all devices)
- ✅ Tab-based navigation system
- ✅ Modal windows for data entry
- ✅ Real-time updates
- ✅ Mobile-friendly interface
- ✅ Custom favicon support

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Modern web browser

### Quick Start

1. **Clone or download** this repository
2. **Navigate to the project folder** in Terminal/Command Prompt
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Open your browser** and go to: `http://127.0.0.1:5000`

### For Network Access
To allow other devices to access the tournament (participants, spectators):
1. Find your computer's IP address
2. Share the URL: `http://YOUR_IP_ADDRESS:5000`
3. Participants can view live results from any device

## 📱 Usage Guide

### Main Navigation Tabs
1. **Dashboard** - Tournament overview and statistics
2. **Divisions** - Manage tournament divisions
3. **Drivers** - Add, edit, and manage drivers
4. **Races** - Record race results
5. **Rankings** - View current standings

### Getting Started
1. **Add Divisions:** Create tournament divisions (e.g., "Pro", "Amateur")
2. **Add Drivers:** Register drivers to specific divisions
3. **Record Races:** Input race results as they happen
4. **View Rankings:** Monitor live tournament standings
5. **Export Results:** Generate Excel/CSV reports

### Championship Races
- Record 3-driver elimination races
- Automatically handles complex win/loss scenarios
- Tracks championship progression

### Driver Status System
- **Active:** Currently competing (< 3 losses)
- **Eliminated:** Out of tournament (3+ losses)
- **Inactive:** Not currently participating

## 🏆 Key Advantages

### Over Desktop Applications
- ✅ **Universal Compatibility:** Works on Mac, PC, phones, tablets
- ✅ **No Installation Required:** Participants just need a browser
- ✅ **Real-time Updates:** Live results for all viewers
- ✅ **Cross-Platform:** No macOS security issues
- ✅ **Easy Sharing:** Simple web address to share
- ✅ **Centralized Management:** One person runs, everyone views

### Technical Benefits
- ✅ **Responsive Design:** Adapts to any screen size
- ✅ **Data Persistence:** Auto-saves tournament state
- ✅ **Export Options:** Multiple file formats supported
- ✅ **Robust Architecture:** Flask backend with JavaScript frontend

## 📊 Data Management

### Supported File Formats
- **Excel (.xlsx):** Full import/export with formatting
- **CSV:** Standard comma-separated values
- **JSON:** Tournament save/load functionality

### Excel Import Requirements
- Column A: Driver names
- Column B: Division names
- First row can be headers (automatically detected)

## 🔧 Technical Details

### Technology Stack
- **Backend:** Python Flask framework
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Data Processing:** Pandas, OpenPyXL
- **Storage:** JSON for tournament state, Excel/CSV for exports

### File Structure
```
drag_race_web_app/
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License  
├── Procfile            # Railway deployment
├── README.md           # Documentation
├── app.py             # Flask app (modified)
├── index.html         # Main template (moved from templates/)
├── registered_racers.xlsx # Sample data
├── requirements.txt   # Python deps (added gunicorn)
├── runtime.txt        # Python version
└── static/
   └── ms_logo.png    # Your favicon
```

### API Endpoints
- `GET /api/drivers` - Retrieve all drivers
- `POST /api/drivers` - Add new driver
- `PUT /api/drivers/<name>` - Update driver
- `DELETE /api/drivers/<name>` - Delete driver
- `POST /api/race` - Record race result
- `GET /api/rankings` - Get tournament rankings
- `GET /api/stats` - Tournament statistics
- `GET /api/export` - Export CSV
- `GET /api/export-excel` - Export Excel

## 🧪 Testing

Load sample data by clicking "Load Sample Data" on the dashboard to populate the tournament with test drivers and see all features in action.

## 🤝 Support

This is a complete tournament management solution suitable for:
- Local drag racing events
- Tournament organizers
- Racing clubs and associations
- Any competitive elimination-style tournaments

## 📝 Version History

Current version includes:
- Complete CRUD operations for drivers and divisions
- Championship race support
- Excel import/export functionality
- Responsive web design
- Real-time tournament tracking
- Comprehensive statistics and reporting