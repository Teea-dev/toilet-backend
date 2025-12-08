import sys
import os
import json
from flask import current_app
from app import app, db, Toilet  # Import the app and db from your main app file

def create_tables():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

def populate_database():
    """Populate the database with predefined toilet locations."""
    UI_TOILET_LOCATIONS = [
        {
            "name": "Engineering Building Toilet",
            "latitude": 7.44108,
            "longitude": 3.90420,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": False,
            "cleaniness_rating": 4.2,
            "description": "Modern facility with multiple stalls for both male and female students.",
            "opening_time": "08:00",
            "closing_time": "17:00",
            
        },
        {
            "name": "Access Bank Toilet",
            "latitude": 7.441625,
            "longitude": 3.903240,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.5,
            "description": "Spacious and well-maintained restroom near study areas.",
            "opening_time": "08:00",
            "closing_time": "16:00",
            "open_saturday": True,
            "open_sunday": True
        },
        {
            "name": "Arts Faculty Toilet",
            "latitude": 7.44060,
            "longitude": 3.90380,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 3.7,
            "description": "Basic facility with limited accessibility.",
            "opening_time": "07:30",
            "closing_time": "18:00",
            
        },
        {
            "name": "Student Eco-Friendly Center",
            "latitude": 7.438301,
            "longitude": 3.893746,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "Clean toilets with comfortable area to sit, read and charge.",
            "opening_time": "10:00",
            "closing_time": "16:00",
            
        },
         {
            "name": "U&I Toilet",
            "latitude": 7.438233,
            "longitude": 3.894730,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "Ask at the reception if you can use the toilet and you would be directed to it (Dont be shy they dont bite). Clean toilets with water running all the time .",
            "opening_time": "09:00",
            "closing_time": "21:00",
             "open_saturday": True,
            "open_sunday": True
        }
        ,
         {
            "name": "Jaja Toilet",
            "latitude":   7.442383941605227,
            "longitude": 3.900867913071352,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "The toilets at Jaja are good but it can be restricted at times. When you get into the building walk straight and you will see the toilets on your left. The toilets are clean and have running water.",
            "opening_time": "08:00",
            "closing_time": "22:00",
             "open_saturday": True,
            "open_sunday": True
        }
        ,
         {
            "name": "UI Hotels",
            "latitude":   7.448564093653943, 
            "longitude": 3.9008091255170227,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "The toilets at UI Hotels are  clean and always have running water. Ask the security at the gate if you can't find the toilet and they will direct you to it.",
            "opening_time": "00:00",  
            "closing_time": "23:00",
             "open_saturday": True,
            "open_sunday": True
        }
        ,
         {
            "name": "UI Central Mosque",
            "latitude":   7.447082461901469,
            "longitude":  3.899328746759421,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 3.7,
            "description": "The toilets at UI Central Mosque are alright, they aren't WC toilets. It is necessary to carry your own tissue paper as it is not provided. The toilets are usually clean and have running water most of the time. Females have to cover their heads to enter the mosque premises.",
            "opening_time": "07:00",
            "closing_time": "21:00",
            "open_saturday": True,
            "open_sunday": True
            
        }
        ,
         {
            "name": "The Faculty Of Social Sciences",
            "latitude":    7.447067741491339,
            "longitude":  3.893511100064327,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 3.7,
            "description": "The toilets in this building are always clean and have water running 80% of the time . The toilets that are always opened are  located on the first floor of the building. The downside is the toilets are for lecturers hence you need to be careful",
            "opening_time": "08:00",
            "closing_time": "16:00",
        }
        ,
         {
            "name": "Chemistry Building",
            "latitude":    7.444518,
            "longitude":   3.894077,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "The toilets in this building are always clean and have water running 80% of the time.",
             "opening_time": "07:00",
            "closing_time": "17:00",
           
        },
         {
            "name": "New Forestry Building Opposite Tree Club Parking Lot",
            "latitude":    7.44883,
            "longitude":   3.89752,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 4.7,
            "description": "The toilets in this building are always clean and have water running 80% of the time. The 003 is for males and the 002 is for females.",
             "opening_time": "09:00",
            "closing_time": "16:00",
           
        },
         {
            "name": "Tree Club Building Toilet",
            "latitude":    7.44901,
            "longitude":   3.89721,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 2,
            "description": "The toilets in this building are always open, they appear clean but have some sort of odour. Can be managed if in a hurry or emergency",
             "opening_time": "00:00",
            "closing_time": "23:59",
             "open_saturday": True,
            "open_sunday": True
           
        },
         {
            "name": "Faculty Of Agriculture Building Toilet ",
            "latitude":    7.44958,
            "longitude":   3.89607,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 2.5,
            "description": "The toilets in this faculty are situated between the LLT and SLT are always open, they appear clean but have some sort of odour. Can be managed if in a hurry or emergency",
             "opening_time": "09:00",
            "closing_time": "16:00",
             "open_saturday": True,
            "open_sunday": True
           
        },
         {
            "name": "Faculty Of Social Sciences Toilet ",
            "latitude":    7.44647,
            "longitude":   3.89318,
            "is_male": True,
            "is_female": True,
            "is_accessible": True,
            "is_open": True,
            "cleaniness_rating": 2.5,
            "description": "The toilets in this faculty  appear clean but have some sort of odour. Can be managed if in a hurry or emergency",
             "opening_time": "08:00",
            "closing_time": "16:00",
             
           
        },
        
    ]

    with app.app_context():
        # Clear existing data
        db.session.query(Toilet).delete()
        
        # Add new toilets
        for toilet_data in UI_TOILET_LOCATIONS:
            default_days = {
                "open_monday": True,
                "open_tuesday": True,
                "open_wednesday": True,
                "open_thursday": True,
                "open_friday": True,
                "open_saturday": False,
                "open_sunday": False
            }
            # Add default days to the toilet data
            for day in default_days:
                if day not in toilet_data:
                    toilet_data[day] = default_days[day]
            new_toilet = Toilet(**toilet_data, rating=0.0, num_ratings=0)
            db.session.add(new_toilet)
        
        # Commit changes
        db.session.commit()
        print(f"Successfully added {len(UI_TOILET_LOCATIONS)} toilet locations to the database.")

def export_toilets_to_json():
    """Export current database toilets to a JSON file."""
    with app.app_context():
        toilets = Toilet.query.all()
        toilet_list = []
        
        for toilet in toilets:
            toilet_dict = {
                "name": toilet.name,
                "latitude": toilet.latitude,
                "longitude": toilet.longitude,
                "is_male": toilet.is_male,
                "is_female": toilet.is_female,
                "is_accessible": toilet.is_accessible,
                "is_open": toilet.is_open,
                "cleaniness_rating": toilet.cleaniness_rating,
                "description": toilet.description,
                "opening_time": toilet.opening_time,
                "closing_time": toilet.closing_time,
                "open_monday": toilet.open_monday,
                "open_tuesday": toilet.open_tuesday,
                "open_wednesday": toilet.open_wednesday,
                "open_thursday": toilet.open_thursday,
                "open_friday": toilet.open_friday,
                "open_saturday": toilet.open_saturday,
                "open_sunday": toilet.open_sunday
            }
            toilet_list.append(toilet_dict)
        
        with open('ui_toilets.json', 'w') as f:
            json.dump(toilet_list, f, indent=4)
        
        print("Toilet locations exported to ui_toilets.json")

def import_toilets_from_json(file_path):
    """Import toilet locations from a JSON file."""
    with app.app_context():
        with open(file_path, 'r') as f:
            toilet_data = json.load(f)
        
        # Clear existing data
        db.session.query(Toilet).delete()
        
        # Add toilets from JSON
        for toilet_info in toilet_data:
            new_toilet = Toilet(**toilet_info, rating=0.0, num_ratings=0)
            db.session.add(new_toilet)
        
        db.session.commit()
        print(f"Successfully imported {len(toilet_data)} toilet locations from {file_path}")

def main():
    """Main menu for database operations."""
    print("Toilet Database Population Script")
    print("1. Populate Database with Predefined Locations")
    print("2. Export Current Toilets to JSON")
    print("3. Import Toilets from JSON")
    print("4. Update Database schema (add opening hours field)")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        # First recreate tables to ensure schema is up to date
        create_tables()
        populate_database()
    elif choice == '2':
        export_toilets_to_json()
    elif choice == '3':
        file_path = input("Enter the path to the JSON file: ")
        import_toilets_from_json(file_path)
    elif choice == '4':
        with app.app_context():
            db.drop_all()  # Drop existing tables
            db.create_all()  # Recreate with updated schema
            print("Database schema updated successfully.")    
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    if not os.environ.get('DYNO'):  # Check if not running on Heroku
        main()
    else:
        print("Running in Heroku environment - skipping main menu.")    
        create_tables()
        populate_database()
