import csv
import os

DB_FILE = "patients.csv"
CSV_COLUMNS = ["id", "name", "age", "weight", "height", "blood_type", "conditions", "allergies"]

patients_db = {} 

used_ids = set()

def check_id_exists(patient_id):
    """Checks if an ID is already in the set."""
    return patient_id in used_ids

def create_patient(p_id, name, age, weight, height, blood_type, conditions_list, allergies_list):
    """
    Creates a new patient record and saves it to CSV.
    Accepts lists for conditions/allergies and joins them with ';' for storage.
    """
    patients_db[p_id] = {
        "id": p_id,
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "blood_type": blood_type,
        "conditions": conditions_list, 
        "allergies": allergies_list    
    }
    
    used_ids.add(p_id)
    
    save_all_data()

def delete_patient(p_id):
    if p_id in patients_db:
        del patients_db[p_id]
        used_ids.remove(p_id)
        save_all_data()
        return True
    return False

def save_all_data():
    
    try:
        with open(DB_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            
            for profile in patients_db.values():
              
                row_to_save = profile.copy()
                row_to_save["conditions"] = ";".join(profile["conditions"])
                row_to_save["allergies"] = ";".join(profile["allergies"])
                
                writer.writerow(row_to_save)
                
        print("[System] Database saved successfully.")
    except Exception as e:
        print(f"[Error] Could not save to CSV: {e}")

def load_data_from_csv():
    global patients_db, used_ids
    
    if not os.path.exists(DB_FILE):
        print("[System] No existing database found. Starting fresh.")
        return

    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                p_id = int(row["id"])
                row["id"] = p_id
                row["age"] = int(row["age"])
                row["weight"] = float(row["weight"])
                row["height"] = float(row["height"])
                row["conditions"] = row["conditions"].split(";") if row["conditions"] else []
                row["allergies"] = row["allergies"].split(";") if row["allergies"] else []
                patients_db[p_id] = row
                used_ids.add(p_id)
                
        print(f"[System] Successfully loaded {len(patients_db)} patient records.")
        
    except Exception as e:
        print(f"[Error] Corrupt CSV data or read error: {e}")

def get_patient_details(p_id):
    return patients_db.get(p_id)