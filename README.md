# Smart Building Code Compliance Checker

🏗️ **A Streamlit-powered web application for structural design compliance checking**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Engineering](https://img.shields.io/badge/Engineering-00599C?style=for-the-badge&logo=engineering&logoColor=white)

## 🎯 Overview

A comprehensive structural engineering tool that checks building designs against **Indian Standard codes** (IS 456:2000, IS 875). Built with Streamlit for easy deployment and user-friendly interface.

## 🚀 Live Demo

**Try it online:** [Streamlit Cloud Deployment](https://smart-building-compliance-checker.streamlit.app)

## ✨ Features

### 🏗️ **Structural Analysis**
- ✅ **Beam Design**: Flexural strength, shear capacity, deflection checks
- ✅ **Column Design**: Axial load capacity, slenderness ratio validation
- ✅ **Slab Design**: Thickness requirements, reinforcement spacing
- ✅ **Footing Design**: Bearing capacity, punching shear analysis

### 📋 **Code Compliance**
- 🇮🇳 **IS 456:2000** - Plain and Reinforced Concrete
- 🏢 **IS 875** - Design Loads (Dead, Live, Wind, Seismic)
- ⚡ **Real-time Validation** - Instant compliance feedback
- 📊 **Detailed Reports** - Step-by-step calculations

### 🔧 **Built With**
- **Frontend**: Streamlit (Interactive web interface)
- **Backend**: Python (Structural calculations)
- **Reports**: ReportLab (PDF generation)
- **Deployment**: Streamlit Cloud ready

## 🚀 Quick Start

### Option 1: Run Locally
```bash
# Clone the repository
git clone https://github.com/Nahid305/smart-building-compliance-checker.git
cd smart-building-compliance-checker

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Option 2: Streamlit Cloud
1. Fork this repository
2. Connect to Streamlit Cloud
3. Deploy with one click!

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Development
```bash
# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Smart Building Code Compliance Checker/
├── app.py                   # Main Streamlit application
├── backend/                 # Core calculation modules
│   ├── api/
│   │   └── check_code.py   # Main compliance checking API
│   ├── data/               # Building code specifications
│   └── utils/              # Calculation utilities
│       ├── beam_checker.py
│       ├── column_checker.py
│       ├── slab_checker.py
│       ├── footing_checker.py
│       ├── load_calculator.py
│       └── pdf_generator.py
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with NumPy, Pandas
- **Calculations**: Engineering formulas per IS codes
- **Reports**: ReportLab for PDF generation
- **Visualization**: Matplotlib, Plotly

## 🎯 Usage

1. **Launch Application**: Run `streamlit run app.py`
2. **Select Member Type**: Choose beam, column, slab, or footing
3. **Enter Dimensions**: Input member dimensions and properties
4. **Auto Load Calculation**: System calculates loads per IS 875
5. **Check Compliance**: Get instant pass/fail results
6. **Download Report**: Generate PDF compliance report

## 📊 Features Overview

### ✅ **Design Checks Available**
- **Flexural Strength** (IS 456:2000 Cl. 38)
- **Shear Strength** (IS 456:2000 Cl. 40)
- **Deflection Limits** (IS 456:2000 Cl. 23)
- **Minimum Reinforcement** (IS 456:2000 Cl. 26)
- **Maximum Spacing** (IS 456:2000 Cl. 26)
- **Load Combinations** (IS 875 Parts 1-5)

### 📈 **Supported Load Types**
- Dead Load (IS 875 Part 1)
- Live Load (IS 875 Part 2)  
- Wind Load (IS 875 Part 3)
- Seismic Load (IS 875 Part 5)

## 🚀 Deployment

### Streamlit Cloud Deployment
1. Push code to GitHub repository
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with automatic requirements.txt detection
4. Share your live application URL

### Local Network Deployment
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 🧪 Testing

The application includes comprehensive structural calculation tests:
- Beam design validation
- Column capacity verification  
- Load calculation accuracy
- Code compliance checking

## 📋 Requirements

### Python Dependencies
```
streamlit>=1.28.1
pandas>=2.1.0
numpy>=1.25.0
matplotlib>=3.7.0
plotly>=5.15.0
reportlab>=4.0.0
Pillow>=10.0.0
scipy>=1.11.0
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: support@smartbuilding.com
- 🐛 Issues: [GitHub Issues](https://github.com/Nahid305/smart-building-compliance-checker/issues)
- 📚 Documentation: [Wiki](https://github.com/Nahid305/smart-building-compliance-checker/wiki)

## 🏆 Acknowledgments

- Indian Standard codes IS 456:2000 and IS 875
- Streamlit community for the amazing framework
- Structural engineering best practices and guidelines

---

**Built with ❤️ for the structural engineering community**