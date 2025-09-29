
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import math
from datetime import datetime,time


app = Flask(__name__)
if os.environ.get('DATABASE_URL'):
    # Heroku PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development - SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ui_toilets.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Toilet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    num_ratings = db.Column(db.Integer, nullable=False)
    is_male = db.Column(db.Boolean, nullable = False)
    is_female = db.Column(db.Boolean, nullable = False)
    is_accessible = db.Column(db.Boolean, nullable = False)
    is_open = db.Column(db.Boolean, nullable = False)
    cleaniness_rating = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text)
    opening_time = db.Column(db.String(5), nullable=True)
    closing_time = db.Column(db.String(5), nullable=True)
    #Days of the week the toilet is open
    open_monday=db.Column(db.Boolean, default=True)
    open_tuesday=db.Column(db.Boolean, default=True)
    open_wednesday=db.Column(db.Boolean, default=True)
    open_thursday=db.Column(db.Boolean, default=True)
    open_friday=db.Column(db.Boolean, default=True)
    open_saturday=db.Column(db.Boolean, default=True)
    open_sunday=db.Column(db.Boolean, default=True)
    
    def is_currently_open(self):
        if not self.opening_time or not self.closing_time:
            return self.is_open
        
        now = datetime.now()
        current_time = now.time()
        
        day_of_the_week= now.strftime("%A").lower()
        day_open = getattr(self, f'open_{day_of_the_week}', True)
        
        if not day_open:
            return False
        
        
        try:
            open_hour, open_minute = map(int, self.opening_time.split(':'))
            close_hour, close_minute = map(int, self.closing_time.split(':'))
            
            opening_time = time(hour=open_hour, minute=open_minute)
            closing_time = time(hour=close_hour, minute=close_minute)
            
            
            if closing_time < opening_time:
                # If closing time is less than opening time, it means the toilet closes after midnight
                return current_time >= opening_time or current_time <= closing_time
            else:
                return opening_time <= current_time <= closing_time
                
        except (ValueError,AttributeError):
            return self.is_open
                
    
    
def haversine(lat1, lon1, lat2, lon2):
    
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/api/add_toilet', methods=['POST'])

def add_toilet():
    data = request.json        
    
    required_fields = ['name', 'location', 'is_male', 'is_female', 'is_accessible']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    new_toilet = Toilet(
        name=data['name'],
        latitude=data['location']['latitude'],
        longitude=data['location']['longitude'],
        is_male=data['is_male'],
        is_female=data['is_female'],
        is_accessible=data['is_accessible'],
        is_open=data.get('is_open', True),
        cleaniness_rating=data.get('cleaniness_rating', 0.0),
        description=data.get('description', ''),
        rating=0.0,
        num_ratings=0,
        
        opening_time=data.get('opening_time'),
        closing_time=data.get('closing_time'),
        open_monday=data.get('open_monday', True),
        open_tuesday=data.get('open_tuesday', True),
        open_wednesday=data.get('open_wednesday', True),
        open_thursday=data.get('open_thursday', True),
        open_friday=data.get('open_friday', True),
        open_saturday=data.get('open_saturday', True),
        open_sunday=data.get('open_sunday', True)
    )

    db.session.add(new_toilet)
    db.session.commit()

    return jsonify({'message': 'Toilet added successfully', 'toilet_id': new_toilet.id}), 201
            
@app.route('/api/toilets', methods=['GET'])
def get_toilets():
    lat = request.args.get('latitude', type=float) 
    lon = request.args.get('longitude', type=float)
    
    # Filter options
    is_male = request.args.get('is_male', type=bool)
    is_female = request.args.get('is_female', type=bool)
    is_accessible = request.args.get('is_accessible', type=bool)
    is_open = request.args.get('is_open', type=bool)
    
    # Base query
    query = Toilet.query     
    
    # Apply filters
    if is_male is not None:
        query = query.filter_by(is_male=is_male)
    if is_female is not None:    
        query = query.filter_by(is_female=is_female)
    if is_accessible is not None:
        query = query.filter_by(is_accessible=is_accessible)
    if is_open is not None:
        # query = query.filter_by(is_open=is_open)
        pass
    # Fetch all toilets  
    toilets = query.all()
    
    toilet_list = []
    for toilet in toilets:
        curren_open_status = toilet.is_currently_open()
        if is_open is not None and curren_open_status != is_open:
            continue
        toilet_data = {
            'id': toilet.id,
            'name': toilet.name,
            'latitude': toilet.latitude,
            'longitude': toilet.longitude,
            'rating': toilet.rating,
            'num_ratings': toilet.num_ratings,
            'is_male': toilet.is_male,
            'is_female': toilet.is_female,
            'is_accessible': toilet.is_accessible,
            'is_open': toilet.is_open,
            'cleaniness_rating': toilet.cleaniness_rating,
            'description': toilet.description,
            'opening_time': toilet.opening_time,
            'closing_time': toilet.closing_time,
            'open_monday': toilet.open_monday,
            'open_tuesday': toilet.open_tuesday,
            'open_wednesday': toilet.open_wednesday,
            'open_thursday': toilet.open_thursday,
            'open_friday': toilet.open_friday,
            'open_saturday': toilet.open_saturday,
            'open_sunday': toilet.open_sunday
        }
                
        # Calculate distance if coordinates provided
        if lat and lon:
            distance = haversine(lat, lon, toilet.latitude, toilet.longitude)
            toilet_data['distance'] = distance
        
        toilet_list.append(toilet_data)
    
    # Sort by distance if coordinates provided
    if lat and lon:
        toilet_list.sort(key=lambda x: x.get('distance', float('inf')))
    
    return jsonify(toilet_list)

@app.route('/api/update-toilet/<int:toilet_id>', methods=['PUT'])
def update_toilet(toilet_id):
    data = request.json

    toilet = Toilet.query.get_or_404(toilet_id)
    if 'name' in data:
        toilet.name = data['name']
    if 'location' in data:
        toilet.location = data['location']  
    if 'latitude' in data:
        toilet.latitude = data['latitude']
    if 'longitude' in data:
        toilet.longitude = data['longitude']
    if 'is_male' in data:
        toilet.is_male= data['is_male']
    if 'is_female' in data:
        toilet.is_female = data['is_female']
    if 'is_accessible' in data:
        toilet.is_accessible = data['is_accessible']    
    if 'is_open' in data:
        toilet.is_open = data['is_open']
    if 'cleaniness_rating' in data:
        toilet.cleaniness_rating = data['cleaniness_rating']
    if 'description' in data:
        toilet.description = data['description']
    if 'open_monday' in data:
        toilet.open_monday = data['open_monday']
    if 'open_tuesday' in data:
        toilet.open_tuesday = data['open_tuesday']
    if 'open_wednesday' in data:
        toilet.open_wednesday = data['open_wednesday']
    if 'open_thursday' in data:
        toilet.open_thursday = data['open_thursday']
    if 'open_friday' in data:
        toilet.open_friday = data['open_friday']
    if 'open_saturday' in data:
        toilet.open_saturday = data['open_saturday']
    if 'open_sunday' in data:
        toilet.open_sunday = data['open_sunday']
                
    db.session.commit()
    return jsonify({'message': 'Toilet updated successfully', 'toilet_id': toilet.id})            
        
@app.route('/api/delete-toilet/<int:toilet_id>', methods=['DELETE'])

def delete_toilet(toilet_id):
    toilet = Toilet.query.get_or_404(toilet_id)
    
    db.session.delete(toilet)
    db.session.commit()
    
    return jsonify({'message': 'Toilet deleted successfully', 'toilet_id': toilet.id})

@app.route('/api/open-toillets', methods=['GET', 'POST'])
def get_open_toilets():
    try:
        # Check if coordinates are provided via POST request
        if request.method == 'POST' and request.is_json:
            data = request.json
            lat = data.get('lat')
            lng = data.get('lng')
        else:
            # If not POST or not JSON, check for URL parameters
            lat = request.args.get('latitude', type=float)
            lng = request.args.get('longitude', type=float)
        
        # Query only open toilets
        # query = Toilet.query.filter_by(is_open=True)
        toilets = Toilet.query.all()
        
        # Fetch all open toilets
        # toilets = query.all()
        
        toilet_list = []
        
        for toilet in toilets:
            if not toilet.is_currently_open():
                continue
            toilet_data = {
                'id': toilet.id,
                'name': toilet.name,
                'latitude': toilet.latitude,
                'longitude': toilet.longitude,
                'rating': toilet.rating,
                'num_ratings': toilet.num_ratings,
                'is_male': toilet.is_male,
                'is_female': toilet.is_female,
                'is_accessible': toilet.is_accessible,
                'is_open': True,
                'cleaniness_rating': toilet.cleaniness_rating,
                'description': toilet.description,
                'opening_time': toilet.opening_time,
                'closing_time': toilet.closing_time,
                
            }
            
            # Calculate distance if coordinates provided
            if lat is not None and lng is not None:
                try:
                    distance = haversine(float(lat), float(lng), toilet.latitude, toilet.longitude)
                    toilet_data['distance'] = distance
                except (TypeError, ValueError) as e:
                    print(f"Error calculating distance: {e}")
            
            toilet_list.append(toilet_data)
        
        # Sort by distance if coordinates provided
        if lat is not None and lng is not None:
            toilet_list.sort(key=lambda x: x.get('distance', float('inf')))
        
        return jsonify(toilet_list)
    
    except Exception as e:
        print(f"Error in get_open_toilets: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok", "message": "Toilet Finder API is running"}), 200    

#Create the database
with app.app_context():
    
    db.create_all()    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 