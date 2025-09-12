# 📡 Pathloss Prediction System

A professional web application for predicting signal pathloss in wireless communication systems using established empirical models.

## 🚀 Features

- **Three Pathloss Models**: ECC-33, SUI, and Okumura-Hata
- **Real-time Calculations**: Instant pathloss predictions
- **Modern UI**: Clean, responsive design with glassmorphism effects
- **Input Validation**: Comprehensive parameter validation
- **Multiple Environments**: Urban, Suburban, Rural, and Dense Urban

## 🧮 Supported Models

### ECC-33 Model
- **Range**: 30 MHz - 3 GHz
- **Best for**: Cellular networks
- **Formula**: `PL = Afs + Abm - G(htx) - G(hrx) - Garea`

### SUI Model
- **Range**: 1.9 - 11 GHz
- **Best for**: Wireless communications
- **Formula**: `PL = A + 10*γ*log10(d/d0) + Xf + Xh`

### Okumura-Hata Model
- **Range**: 150 MHz - 1.5 GHz (extended to 2 GHz)
- **Best for**: Mobile communications
- **Formula**: Standard Hata equation with environment corrections

## 🛠️ Installation

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd pathloss-prediction

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Vercel Deployment
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the Python app
3. Deploy with zero configuration

## 📊 Usage

1. **Enter Parameters**:
   - Frequency (MHz)
   - Distance (km)
   - Transmitter height (m)
   - Receiver height (m)
   - Environment type
   - Prediction model

2. **Get Results**:
   - Pathloss value in dB
   - Free space path loss comparison
   - Additional loss over free space

## 🎯 Input Ranges

| Parameter | Range | Unit |
|-----------|-------|------|
| Frequency | 30 - 11000 | MHz |
| Distance | 0.1 - 100 | km |
| TX Height | 1 - 200 | m |
| RX Height | 0.5 - 50 | m |

## 🌍 Environment Types

- **Dense Urban**: High-rise buildings, heavy traffic
- **Urban**: City centers, moderate buildings
- **Suburban**: Residential areas, some buildings
- **Rural**: Open areas, minimal obstructions

## 🔬 Mathematical Accuracy

All models have been cross-verified against:
- ETSI TR 101 112 (ECC-33)
- IEEE 802.16 standards (SUI)
- ITU-R P.1546 (Okumura-Hata)
- Authoritative telecommunications literature

## 🚀 Deployment

This application is optimized for Vercel deployment with:
- `vercel.json` configuration
- Python runtime support
- Automatic scaling
- Global CDN

## 📱 Responsive Design

- Mobile-first approach
- Glassmorphism UI effects
- Smooth animations
- Cross-browser compatibility

## 🛡️ Error Handling

- Input validation
- Range checking
- Model-specific constraints
- User-friendly error messages

## 📈 Performance

- Fast calculations
- Optimized algorithms
- Minimal dependencies
- Efficient rendering

---

**Built with ❤️ for telecommunications professionals**
