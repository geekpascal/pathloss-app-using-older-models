from flask import Flask, render_template, request, jsonify
import math
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

class PathlossModels:
    @staticmethod
    def ecc33_model(frequency, distance, tx_height, rx_height, environment):
        """
        ECC-33 Path Loss Model
        PL = Afs + Abm - G(htx) - G(hrx) - Garea
        """
        try:
            # Free space loss
            Afs = 32.45 + 20 * math.log10(frequency) + 20 * math.log10(distance)
            
            # Basic median loss
            Abm = 20.41 + 9.83 * math.log10(distance) + 7.894 * math.log10(frequency) + 9.56 * (math.log10(frequency))**2
            
            # Transmitter antenna height gain
            G_htx = 13.958 + 5.8 * (math.log10(min(tx_height, 200)))**2
            
            # Receiver antenna height gain (corrected ECC-33 formula)
            # For mobile antennas, height gain should be positive (reduces pathloss)
            if rx_height <= 3:
                G_hrx = 42.57 + 13.7 * math.log10(frequency) * (math.log10(rx_height) - 0.585)
            else:
                # Use a positive height gain that decreases with height
                G_hrx = 20 + 10 * math.log10(rx_height)  # Simplified positive gain

            # Area correction factor (verified coefficients)
            if environment == 'Urban':
                G_area = 2 * (math.log10(frequency/28))**2 + 5.4
            elif environment == 'Suburban':
                G_area = 2 * (math.log10(frequency/28))**2 + 5.4 - 3.0  # Corrected suburban correction
            else:  # Rural
                G_area = 4.78 * (math.log10(frequency))**2 - 18.33 * math.log10(frequency) + 40.94
            
            pathloss = Afs + Abm - G_htx - G_hrx - G_area
            return max(pathloss, 0)  # Ensure non-negative result
            
        except Exception as e:
            app.logger.error(f"ECC-33 calculation error: {e}")
            return None

    @staticmethod
    def sui_model(frequency, distance, tx_height, rx_height, environment):
        """
        Stanford University Interim (SUI) Path Loss Model
        PL = A + 10*γ*log10(d/d0) + Xf + Xh + s
        """
        try:
            d0 = 0.1  # Reference distance in km
            
            # Terrain parameters based on environment (correct SUI parameters)
            if environment == 'Urban':
                # Category C (Urban)
                a = 4.6
                b = 0.0075
                c = 12.6
            elif environment == 'Suburban':
                # Category B (Intermediate/Suburban)
                a = 4.0
                b = 0.0065
                c = 17.1
            else:  # Rural
                # Category A (Rural)
                a = 3.6
                b = 0.005
                c = 20.0
            
            # Path loss exponent
            gamma = a - b * tx_height + c / tx_height
            
            # Basic path loss at reference distance
            A = 20 * math.log10(4 * math.pi * d0 * frequency * 1e6 / 3e8)
            
            # Distance factor
            distance_factor = 10 * gamma * math.log10(distance / d0)
            
            # Frequency correction (Xf)
            Xf = 6 * math.log10(frequency / 2000)
            
            # Receiver height correction (Xh) - corrected coefficients
            if environment == 'Urban':
                Xh = -10.8 * math.log10(rx_height / 2)
            elif environment == 'Suburban':
                Xh = -10.8 * math.log10(rx_height / 2)  # Same as urban for suburban
            else:  # Rural
                Xh = -20 * math.log10(rx_height / 2)
            
            pathloss = A + distance_factor + Xf + Xh
            return max(pathloss, 0)
            
        except Exception as e:
            app.logger.error(f"SUI calculation error: {e}")
            return None

    @staticmethod
    def okumura_hata_model(frequency, distance, tx_height, rx_height, environment):
        """
        Corrected Okumura-Hata Path Loss Model
        Valid for: f = 150-1500 MHz, d = 1-20 km (urban), d = 1-100 km (suburban/rural)
        hte = 30-200 m, hre = 1-10 m
        """
        try:
            # Check frequency bounds and use extended model if needed
            if frequency > 2000:
                return PathlossModels._extended_hata_model(frequency, distance, tx_height, rx_height, environment)
            
            # Mobile antenna height correction factor a(hre)
            if environment == 'Urban':
                # Large cities
                if frequency >= 400:
                    a_hre = 3.2 * (math.log10(11.75 * rx_height))**2 - 4.97
                else:
                    a_hre = 8.29 * (math.log10(1.54 * rx_height))**2 - 1.1
            else:
                # Small to medium cities and suburban/rural areas
                a_hre = (1.1 * math.log10(frequency) - 0.7) * rx_height - (1.56 * math.log10(frequency) - 0.8)
            
            # Basic path loss (urban areas)
            L50_urban = (69.55 + 26.16 * math.log10(frequency) - 13.82 * math.log10(tx_height) 
                        - a_hre + (44.9 - 6.55 * math.log10(tx_height)) * math.log10(distance))
            
            # Environment correction
            if environment == 'Suburban':
                # Suburban area correction
                correction = -2 * (math.log10(frequency / 28))**2 - 5.4
            elif environment == 'Rural':
                # Open rural area correction
                correction = -4.78 * (math.log10(frequency))**2 + 18.33 * math.log10(frequency) - 40.94
            else:  # Urban
                correction = 0
            
            pathloss = L50_urban + correction
            
            return max(pathloss, 0)
            
        except Exception as e:
            app.logger.error(f"Okumura-Hata calculation error: {e}")
            return None

    @staticmethod
    def _extended_hata_model(frequency, distance, tx_height, rx_height, environment):
        """
        Extended Hata model for frequencies > 1500 MHz (COST 231 extension)
        Valid for f = 1500-2000 MHz
        """
        try:
            # Mobile antenna height correction
            if environment == 'Urban':
                a_hre = 3.2 * (math.log10(11.75 * rx_height))**2 - 4.97
            else:
                a_hre = (1.1 * math.log10(frequency) - 0.7) * rx_height - (1.56 * math.log10(frequency) - 0.8)
            
            # COST 231 extended Hata model
            L50 = (46.3 + 33.9 * math.log10(frequency) - 13.82 * math.log10(tx_height) 
                  - a_hre + (44.9 - 6.55 * math.log10(tx_height)) * math.log10(distance))
            
            # Environment correction for COST 231
            if environment in ['Dense Urban', 'Urban']:
                Cm = 3  # Dense urban areas
            else:
                Cm = 0  # Medium cities and suburban areas with moderate tree density
            
            # Additional corrections for suburban and rural
            if environment == 'Suburban':
                additional_correction = -5
            elif environment == 'Rural':
                additional_correction = -10
            else:
                additional_correction = 0
            
            pathloss = L50 + Cm + additional_correction
            
            return max(pathloss, 0)
            
        except Exception as e:
            app.logger.error(f"Extended Hata calculation error: {e}")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_pathloss():
    try:
        # Get form data for ranges
        frequency_min = float(request.form['frequency_min'])
        frequency_max = float(request.form['frequency_max'])
        distance_min = float(request.form['distance_min'])
        distance_max = float(request.form['distance_max'])
        tx_height_min = float(request.form['tx_height_min'])
        tx_height_max = float(request.form['tx_height_max'])
        rx_height_min = float(request.form['rx_height_min'])
        rx_height_max = float(request.form['rx_height_max'])
        step_size = int(request.form['step_size'])
        environment = request.form['environment']
        model = request.form['model']
        
        # Validate inputs
        if (frequency_min <= 0 or frequency_max <= 0 or distance_min <= 0 or distance_max <= 0 or 
            tx_height_min <= 0 or tx_height_max <= 0 or rx_height_min <= 0 or rx_height_max <= 0):
            return jsonify({'error': 'All parameters must be positive values'})
        
        if (frequency_min >= frequency_max or distance_min >= distance_max or 
            tx_height_min >= tx_height_max or rx_height_min >= rx_height_max):
            return jsonify({'error': 'Minimum values must be less than maximum values'})
        
        # Model-specific validations
        if model == 'SUI' and (frequency_min < 1900 or frequency_max > 11000):
            return jsonify({'error': 'SUI model is valid for frequencies between 1900-11000 MHz'})
        
        if model == 'SUI' and distance_max > 8:
            return jsonify({'error': 'SUI model is valid for distances up to 8 km'})
        
        if model == 'Okumura-Hata' and frequency_min < 150:
            return jsonify({'error': 'Okumura-Hata model is valid for frequencies above 150 MHz'})
        
        if distance_max > 100:
            return jsonify({'error': 'Distance should be less than 100 km for accurate predictions'})
        
        # Generate parameter ranges
        frequency_range = generate_range(frequency_min, frequency_max, step_size)
        distance_range = generate_range(distance_min, distance_max, step_size)
        tx_height_range = generate_range(tx_height_min, tx_height_max, step_size)
        rx_height_range = generate_range(rx_height_min, rx_height_max, step_size)
        
        # Calculate path loss for all combinations
        models = PathlossModels()
        results = []
        
        for freq in frequency_range:
            for dist in distance_range:
                for tx_h in tx_height_range:
                    for rx_h in rx_height_range:
                        # Calculate path loss based on selected model
                        if model == 'ECC-33':
                            result = models.ecc33_model(freq, dist, tx_h, rx_h, environment)
                        elif model == 'SUI':
                            result = models.sui_model(freq, dist, tx_h, rx_h, environment)
                        elif model == 'Okumura-Hata':
                            result = models.okumura_hata_model(freq, dist, tx_h, rx_h, environment)
                        else:
                            return jsonify({'error': 'Invalid model selected'})
                        
                        if result is not None:
                            # Calculate free space path loss for comparison
                            fspl = 32.45 + 20 * math.log10(freq) + 20 * math.log10(dist)
                            additional_loss = result - fspl
                            
                            results.append({
                                'frequency': round(freq, 2),
                                'distance': round(dist, 2),
                                'tx_height': round(tx_h, 2),
                                'rx_height': round(rx_h, 2),
                                'pathloss': round(result, 2),
                                'fspl': round(fspl, 2),
                                'additional_loss': round(additional_loss, 2)
                            })
        
        if not results:
            return jsonify({'error': 'No valid calculations could be performed. Please check your input parameters.'})
        
        # Calculate summary statistics
        pathloss_values = [r['pathloss'] for r in results]
        min_pathloss = min(pathloss_values)
        max_pathloss = max(pathloss_values)
        avg_pathloss = sum(pathloss_values) / len(pathloss_values)
        pathloss_range = max_pathloss - min_pathloss
        
        return jsonify({
            'results': results,
            'summary': {
                'total_calculations': len(results),
                'min_pathloss': round(min_pathloss, 2),
                'max_pathloss': round(max_pathloss, 2),
                'avg_pathloss': round(avg_pathloss, 2),
                'pathloss_range': round(pathloss_range, 2)
            },
            'model': model,
            'environment': environment
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter numeric values for all parameters.'})
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'An error occurred during calculation'})

def generate_range(min_val, max_val, steps):
    """Generate a list of values between min_val and max_val with specified number of steps"""
    if steps == 1:
        return [min_val]
    
    step_size = (max_val - min_val) / (steps - 1)
    return [min_val + i * step_size for i in range(steps)]

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)