#!/usr/bin/env python3
"""
Drag Race Tournament Manager - Web Version
A web-based tournament management system using Flask
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import json
import os
from datetime import datetime
from io import BytesIO, StringIO
import tempfile
import csv
import pandas as pd

app = Flask(__name__)

# Copy the models from the desktop app
class DriverStatus:
    ACTIVE = "ACTIVE"
    ELIMINATED = "ELIMINATED"
    INACTIVE = "INACTIVE"

class Driver:
    def __init__(self, name, division, wins=0, losses=0, races=None, status=DriverStatus.ACTIVE):
        self.name = name
        self.division = division
        self.wins = wins
        self.losses = losses
        self.races = races or []
        self.status = status
    
    @property
    def total_races(self):
        return self.wins + self.losses
    
    @property
    def win_ratio(self):
        return (self.wins / self.total_races) if self.total_races > 0 else 0.0
    
    @property
    def is_eliminated(self):
        return self.losses >= 3
    
    def update_status(self):
        if self.is_eliminated:
            self.status = DriverStatus.ELIMINATED
        else:
            self.status = DriverStatus.ACTIVE
    
    def add_race_result(self, race_number, won):
        self.races.append(race_number)
        if won:
            self.wins += 1
        else:
            self.losses += 1
        self.update_status()
    
    def to_dict(self):
        return {
            'name': self.name,
            'division': self.division,
            'wins': self.wins,
            'losses': self.losses,
            'races': self.races,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        driver = cls(
            name=data['name'],
            division=data['division'],
            wins=data.get('wins', 0),
            losses=data.get('losses', 0),
            races=data.get('races', []),
            status=data.get('status', DriverStatus.ACTIVE)
        )
        return driver

class Race:
    def __init__(self, race_number, driver1, driver2, winner, division, timestamp=None, driver3=None, race_type="regular"):
        self.race_number = race_number
        self.driver1 = driver1
        self.driver2 = driver2
        self.winner = winner
        self.division = division
        self.timestamp = timestamp or datetime.now().isoformat()
        self.driver3 = driver3
        self.race_type = race_type
    
    @property
    def loser(self):
        if self.race_type == "championship" and self.driver3:
            drivers = [self.driver1, self.driver2, self.driver3]
            losers = [d for d in drivers if d != self.winner]
            return ", ".join(losers)
        return self.driver2 if self.winner == self.driver1 else self.driver1
    
    def to_dict(self):
        return {
            'race_number': self.race_number,
            'driver1': self.driver1,
            'driver2': self.driver2,
            'winner': self.winner,
            'division': self.division,
            'timestamp': self.timestamp,
            'driver3': self.driver3,
            'race_type': self.race_type
        }

class TournamentManager:
    def __init__(self):
        self.drivers = {}
        self.races = []
        self.race_counter = 0
        self.divisions = [
            "2X4_4CYL", "4X4_4CYL", "4X4_6CYL_PETROL", 
            "4X4_6CYL_DIESEL", "4X4_V8_PETROL", "4X4_V8_DIESEL", 
            "DAMES", "OPEN"
        ]
    
    def add_driver(self, name, division):
        name = name.strip()
        if not name or name in self.drivers:
            return False, f"Driver '{name}' already exists or is empty"
        
        if division not in self.divisions:
            return False, f"Invalid division: {division}"
        
        self.drivers[name] = Driver(name, division)
        return True, f"Successfully added {name} to {division}"
    
    def record_race(self, driver1_name, driver2_name, winner_name, driver3_name=None, race_type="regular"):
        if driver1_name not in self.drivers or driver2_name not in self.drivers:
            return False, "Driver not found"
        
        racing_drivers = [driver1_name, driver2_name]
        if driver3_name:
            racing_drivers.append(driver3_name)
        
        if winner_name not in racing_drivers:
            return False, "Winner must be one of the racing drivers"
        
        driver1 = self.drivers[driver1_name]
        driver2 = self.drivers[driver2_name]
        
        if driver1.division != driver2.division:
            return False, f"Drivers must be in the same division"
        
        if driver1.is_eliminated or driver2.is_eliminated:
            return False, "Eliminated drivers cannot race"
        
        self.race_counter += 1
        race = Race(
            race_number=self.race_counter,
            driver1=driver1_name,
            driver2=driver2_name,
            winner=winner_name,
            division=driver1.division,
            driver3=driver3_name,
            race_type=race_type
        )
        self.races.append(race)
        
        winner = self.drivers[winner_name]
        winner.add_race_result(self.race_counter, won=True)
        
        for driver_name in racing_drivers:
            if driver_name != winner_name:
                loser = self.drivers[driver_name]
                loser.add_race_result(self.race_counter, won=False)
        
        return True, f"Race {self.race_counter}: {winner_name} wins!"
    
    def get_rankings(self, division=None):
        drivers_to_rank = []
        
        for driver in self.drivers.values():
            if division is None or driver.division == division:
                drivers_to_rank.append(driver)
        
        drivers_to_rank.sort(key=lambda d: (
            d.status == DriverStatus.ELIMINATED,
            -d.wins,
            -d.win_ratio,
            d.losses
        ))
        
        rankings = []
        for position, driver in enumerate(drivers_to_rank, 1):
            rankings.append({
                'position': position,
                'name': driver.name,
                'division': driver.division,
                'wins': driver.wins,
                'losses': driver.losses,
                'total_races': driver.total_races,
                'win_ratio': driver.win_ratio,
                'status': driver.status
            })
        
        return rankings
    
    def get_active_drivers(self, division):
        return [
            name for name, driver in self.drivers.items()
            if driver.division == division and driver.status == DriverStatus.ACTIVE
        ]
    
    def get_tournament_stats(self):
        total_drivers = len(self.drivers)
        active_drivers = len([d for d in self.drivers.values() if d.status == DriverStatus.ACTIVE])
        eliminated_drivers = len([d for d in self.drivers.values() if d.status == DriverStatus.ELIMINATED])
        
        return {
            'total_drivers': total_drivers,
            'active_drivers': active_drivers,
            'eliminated_drivers': eliminated_drivers,
            'total_races': len(self.races),
            'divisions': len(set(driver.division for driver in self.drivers.values()))
        }
    
    def to_dict(self):
        return {
            'drivers': {name: driver.to_dict() for name, driver in self.drivers.items()},
            'races': [race.to_dict() for race in self.races],
            'race_counter': self.race_counter
        }
    
    def from_dict(self, data):
        self.drivers = {name: Driver.from_dict(driver_data) for name, driver_data in data['drivers'].items()}
        self.races = [Race(**race_data) for race_data in data['races']]
        self.race_counter = data.get('race_counter', len(self.races))

# Global tournament instance
tournament = TournamentManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(f'static/{filename}')

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    return jsonify([driver.to_dict() for driver in tournament.drivers.values()])

@app.route('/api/drivers', methods=['POST'])
def add_driver():
    data = request.json
    success, message = tournament.add_driver(data['name'], data['division'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/divisions')
def get_divisions():
    return jsonify(tournament.divisions)

@app.route('/api/race', methods=['POST'])
def record_race():
    data = request.json
    success, message = tournament.record_race(
        data['driver1'],
        data['driver2'], 
        data['winner'],
        data.get('driver3'),
        data.get('race_type', 'regular')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/rankings')
def get_rankings():
    division = request.args.get('division')
    rankings = tournament.get_rankings(division)
    return jsonify(rankings)

@app.route('/api/active-drivers/<division>')
def get_active_drivers(division):
    drivers = tournament.get_active_drivers(division)
    return jsonify(drivers)

@app.route('/api/stats')
def get_stats():
    stats = tournament.get_tournament_stats()
    return jsonify(stats)

@app.route('/api/export')
def export_csv():
    # Create CSV export (simpler alternative to Excel)
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Name', 'Division', 'Wins', 'Losses', 'Win Ratio', 'Status'])
    
    # Write data
    for driver in tournament.drivers.values():
        status = "ACTIVE" if driver.status == DriverStatus.ACTIVE else "ELIMINATED"
        writer.writerow([
            driver.name,
            driver.division,
            driver.wins,
            driver.losses,
            f"{driver.win_ratio:.1%}",
            status
        ])
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"Drag Race Results {today}.csv"
    
    # Create response
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
    return response

@app.route('/api/export-excel')
def export_excel():
    # Create Excel export (like original drag race app)
    try:
        # Create data organized by divisions
        divisions_data = {}
        
        for driver in tournament.drivers.values():
            division = driver.division
            if division not in divisions_data:
                divisions_data[division] = []
            
            status = "ACTIVE" if driver.status == DriverStatus.ACTIVE else "ELIMINATED"
            divisions_data[division].append({
                'Name': driver.name,
                'Wins': driver.wins,
                'Losses': driver.losses,
                'Total Races': driver.total_races,
                'Win Ratio': f"{driver.win_ratio:.1%}",
                'Status': status
            })
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Create a sheet for each division
            for division, drivers in divisions_data.items():
                if drivers:  # Only create sheet if there are drivers
                    df = pd.DataFrame(drivers)
                    # Sort by wins (descending), then by win ratio
                    df = df.sort_values(['Wins', 'Win Ratio'], ascending=[False, False])
                    df.to_excel(writer, sheet_name=division, index=False)
        
        output.seek(0)
        
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"Drag Race Results {today}.xlsx"
        
        # Create response
        response = Response(
            output.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating Excel file: {str(e)}'})

@app.route('/api/save', methods=['POST'])
def save_tournament():
    data = tournament.to_dict()
    return jsonify(data)

@app.route('/api/drivers/<driver_name>', methods=['PUT'])
def update_driver(driver_name):
    try:
        data = request.json
        new_name = data.get('name', '').strip()
        new_division = data.get('division', '').strip()
        
        if not new_name or not new_division:
            return jsonify({'success': False, 'message': 'Name and division are required'})
        
        if new_division not in tournament.divisions:
            return jsonify({'success': False, 'message': f'Invalid division: {new_division}'})
        
        # Check if driver exists
        if driver_name not in tournament.drivers:
            return jsonify({'success': False, 'message': f'Driver {driver_name} not found'})
        
        # Check if new name already exists (only if name is changing)
        if new_name != driver_name and new_name in tournament.drivers:
            return jsonify({'success': False, 'message': f'Driver {new_name} already exists'})
        
        # Get the driver object
        driver = tournament.drivers[driver_name]
        
        # Update name if it changed
        if new_name != driver_name:
            del tournament.drivers[driver_name]
            driver.name = new_name
            tournament.drivers[new_name] = driver
        
        # Update division
        driver.division = new_division
        
        return jsonify({'success': True, 'message': f'Driver updated successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/drivers/<driver_name>', methods=['DELETE'])
def delete_driver(driver_name):
    try:
        # Check if driver exists
        if driver_name not in tournament.drivers:
            return jsonify({'success': False, 'message': f'Driver {driver_name} not found'})
        
        # Remove driver (races remain in history - just like original)
        del tournament.drivers[driver_name]
        
        return jsonify({'success': True, 'message': f'Driver {driver_name} deleted successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/load', methods=['POST'])
def load_tournament():
    try:
        data = request.json
        tournament.from_dict(data)
        return jsonify({'success': True, 'message': 'Tournament loaded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/load-excel', methods=['POST'])
def load_excel():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Read Excel file
        try:
            # Read ALL sheets from the Excel file
            all_sheets = pd.read_excel(file, sheet_name=None)  # None reads all sheets
            
            drivers_data = {}
            total_drivers = 0
            
            # Process each sheet
            for sheet_name, df in all_sheets.items():
                print(f"Processing sheet: {sheet_name}")
                
                # Check if this sheet has driver data
                if 'Name' not in df.columns:
                    # Try to find if sheet name corresponds to a division
                    division_from_sheet = sheet_name.strip().upper()
                    if division_from_sheet in tournament.divisions:
                        # Assume first column is names if no 'Name' column
                        if len(df.columns) > 0:
                            name_col = df.columns[0]
                            for index, row in df.iterrows():
                                try:
                                    name = str(row[name_col]).strip()
                                    
                                    # Skip empty rows
                                    if not name or name.lower() == 'nan':
                                        continue
                                    
                                    # Create driver data with division from sheet name
                                    drivers_data[name] = {
                                        'name': name,
                                        'division': division_from_sheet,
                                        'wins': 0,
                                        'losses': 0,
                                        'races': [],
                                        'status': 'ACTIVE'
                                    }
                                    total_drivers += 1
                                    
                                except Exception as row_error:
                                    continue
                    continue
                
                # Sheet has 'Name' column - process normally
                for index, row in df.iterrows():
                    try:
                        name = str(row['Name']).strip()
                        
                        # Skip empty rows
                        if not name or name.lower() == 'nan':
                            continue
                        
                        # Determine division
                        division = None
                        
                        # Try to get division from 'Division' column
                        if 'Division' in df.columns:
                            division = str(row['Division']).strip().upper()
                        else:
                            # Use sheet name as division
                            division = sheet_name.strip().upper()
                        
                        # Validate division
                        if division not in tournament.divisions:
                            return jsonify({
                                'success': False, 
                                'message': f'Invalid division "{division}" for driver "{name}" in sheet "{sheet_name}". Valid divisions: {", ".join(tournament.divisions)}'
                            })
                        
                        # Create driver data with no race history
                        drivers_data[name] = {
                            'name': name,
                            'division': division,
                            'wins': 0,
                            'losses': 0,
                            'races': [],
                            'status': 'ACTIVE'
                        }
                        total_drivers += 1
                    
                    except Exception as row_error:
                        return jsonify({
                            'success': False, 
                            'message': f'Error processing row {index + 1} in sheet "{sheet_name}" (driver "{row.get("Name", "Unknown")}"): {str(row_error)}'
                        })
            
            # Create tournament data structure (no races, just drivers)
            tournament_data = {
                'drivers': drivers_data,
                'races': [],
                'race_counter': 0
            }
            
            # Load the data into the tournament
            tournament.from_dict(tournament_data)
            
            return jsonify({
                'success': True, 
                'message': f'Successfully loaded {len(drivers_data)} drivers from Excel file'
            })
            
        except Exception as excel_error:
            return jsonify({
                'success': False, 
                'message': f'Error reading Excel file: {str(excel_error)}. Please ensure it\'s a valid Excel file with columns: Name, Division, Wins, Losses, Status (optional)'
            })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)