# 📡 Pathloss Prediction System

A professional web application for predicting signal pathloss in wireless communication systems using established empirical models. Now with **simulation capabilities** for analyzing parameter ranges and comprehensive results visualization.

## 🚀 Features

- **Three Pathloss Models**: ECC-33, SUI, and Okumura-Hata
- **Range-based Simulation**: Analyze pathloss across parameter ranges
- **Comprehensive Results Table**: View all simulation results in an organized table
- **Statistical Analysis**: Min, max, average, and range statistics
- **Modern UI**: Clean, responsive design with professional styling
- **Input Validation**: Comprehensive parameter validation
- **Multiple Environments**: Urban, Suburban, and Rural

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

## 📊 How It Works

### Simulation Process

1. **Define Parameter Ranges**:
   - **Frequency Range**: Enter minimum and maximum frequency values (MHz)
   - **Distance Range**: Enter minimum and maximum distance values (km)
   - **Transmitter Height Range**: Enter minimum and maximum TX height values (m)
   - **Receiver Height Range**: Enter minimum and maximum RX height values (m)

2. **Select Step Size**:
   - Choose how many calculation points you want per parameter (5, 10, 15, or 20 steps)
   - The system generates evenly distributed values between your min and max values
   - **Example**: If you set frequency range 900-1800 MHz with 10 steps, you get: 900, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800 MHz

3. **Choose Model & Environment**:
   - Select your preferred pathloss prediction model
   - Choose the environment type (Urban, Suburban, or Rural)

4. **Run Simulation**:
   - The system calculates pathloss for **ALL possible combinations** of your parameter ranges
   - **Total calculations** = (step_size)⁴
   - **Example**: 10 steps = 10,000 calculations (10×10×10×10)

### Results Display

The simulation results are displayed in a comprehensive table showing:
- **Parameter Values**: Each combination of frequency, distance, TX height, RX height
- **Predicted Pathloss**: The calculated pathloss in dB
- **Free Space Loss**: Theoretical free space pathloss for comparison
- **Additional Loss**: Extra loss due to environment and obstacles

### Statistical Summary

- **Min Pathloss**: Lowest pathloss value across all simulations
- **Max Pathloss**: Highest pathloss value across all simulations  
- **Average Pathloss**: Mean pathloss across all simulations
- **Range**: Difference between max and min pathloss values

## 🎯 Input Ranges

| Parameter | Range | Unit | Notes |
|-----------|-------|------|-------|
| Frequency | 150 - 11000 | MHz | Model-specific limits apply |
| Distance | 0.1 - 100 | km | SUI model limited to 8 km |
| TX Height | 10 - 200 | m | Transmitter antenna height |
| RX Height | 1 - 10 | m | Receiver antenna height |
| Step Size | 5, 10, 15, 20 | steps | Number of calculation points per parameter |

### Step Size Impact

| Step Size | Total Calculations | Use Case |
|-----------|-------------------|----------|
| 5 steps | 625 | Quick analysis |
| 10 steps | 10,000 | Standard simulation |
| 15 steps | 50,625 | Detailed analysis |
| 20 steps | 160,000 | Comprehensive study |

## 🌍 Environment Types

- **Urban**: City centers with moderate to high building density
- **Suburban**: Residential areas with some buildings and vegetation
- **Rural**: Open areas with minimal obstructions and buildings

## 📈 Example Simulation

### Scenario: Cellular Network Planning
- **Frequency Range**: 900 - 1800 MHz (10 steps)
- **Distance Range**: 1 - 10 km (10 steps)  
- **TX Height Range**: 30 - 100 m (10 steps)
- **RX Height Range**: 1.5 - 3 m (10 steps)
- **Model**: ECC-33
- **Environment**: Urban

**Result**: 10,000 calculations showing how pathloss varies across different parameter combinations, helping engineers optimize network coverage and capacity planning.

## 🔢 Understanding Step Size

The **step size** determines how many calculation points are generated between your minimum and maximum values for each parameter.

### How Step Size Works:
- **5 steps**: Generates 5 evenly spaced values between min and max
- **10 steps**: Generates 10 evenly spaced values between min and max
- **15 steps**: Generates 15 evenly spaced values between min and max
- **20 steps**: Generates 20 evenly spaced values between min and max

### Example with Frequency Range 900-1800 MHz:
- **5 steps**: 900, 925, 950, 975, 1800 MHz
- **10 steps**: 900, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800 MHz
- **15 steps**: 900, 951.4, 1002.9, 1054.3, 1105.7, 1157.1, 1208.6, 1260, 1311.4, 1362.9, 1414.3, 1465.7, 1517.1, 1568.6, 1800 MHz

### Choosing the Right Step Size:
- **5 steps**: Quick analysis, basic understanding
- **10 steps**: Standard simulation, good balance of detail and performance
- **15 steps**: Detailed analysis, more precise results
- **20 steps**: Comprehensive study, maximum detail (may take longer to process)

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

- **Fast Calculations**: Optimized algorithms for rapid simulation processing
- **Scalable Design**: Handles up to 160,000 calculations efficiently
- **Minimal Dependencies**: Lightweight Flask backend with pure Python math
- **Efficient Rendering**: Responsive table display with smooth scrolling
- **Memory Optimized**: Streamlined data structures for large result sets

---

**Built with ❤️ for telecommunications professionals**
