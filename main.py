import health_logic
import sys
import matplotlib.pyplot as plt 

def get_multi_input(category_name):
    """
    Helper to get multiple inputs for allergies/conditions.
    Requirement: Logical Workflow
    """
    items = []
    print(f"   (Type 'done' to finish adding {category_name})")
    while True:
        item = input(f"   - Enter {category_name}: ").strip()
        if item.lower() == 'done':
            break
        if item:
            items.append(item)
    return items

def show_graph():
    """
    Visualizes Patient Weights.
    Requirement: Simulation/Visualization
    """
    if not health_logic.patients_db:
        print("\n[!] No data to visualize.")
        return
        
    names = []
    weights = []
    
    for profile in health_logic.patients_db.values():
        names.append(profile["name"])
        weights.append(profile["weight"])
        
    plt.figure(figsize=(10, 6))
    plt.bar(names, weights, color='#4CAF50') # Green bars
    plt.xlabel("Patient Name")
    plt.ylabel("Weight (kg)")
    plt.title("Patient Weight Distribution")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main_menu():
    health_logic.load_data_from_csv()

    while True:
        print("\n" + "="*30)
        print("   VITALTRACK HEALTH SYSTEM")
        print("="*30)
        print("1. Add New Patient")
        print("2. View All Records")
        print("3. Search by Condition")
        print("4. Delete Patient")
        print("5. Visualize Data (Graph)")
        print("6. Exit")
        
        choice = input("\nEnter Choice (1-6): ")
        #OPTION 1     
        try:
            if choice == '1':
                print("\n--- NEW PATIENT ENTRY ---")
                p_id = int(input("ID (Number): "))
                
                if health_logic.check_id_exists(p_id):
                    print("[!] Error: ID already exists.")
                else:
                    name = input("Name: ")
                    age = int(input("Age: "))
                    w = float(input("Weight (kg): "))
                    h = float(input("Height (cm): "))
                    b_type = input("Blood Type: ")
                    
                    print("\n[Medical History]")
                    conditions = get_multi_input("Condition")
                    
                    print("\n[Allergies]")
                    allergies = get_multi_input("Allergy")
                    
                    health_logic.create_patient(p_id, name, age, w, h, b_type, conditions, allergies)
                    print(f"\n[Success] Patient {name} saved!")

            #OPTION 2
            elif choice == '2':
                print("\n--- ALL RECORDS ---")
                if not health_logic.patients_db:
                    print("Database is empty.")
                else:
                    for pid, p in health_logic.patients_db.items():
                        print(f"[{pid}] {p['name']} | Age: {p['age']} | Blood Type1: {p['blood_type']}")
                        
                        cond_str = ", ".join(p['conditions'])
                        allg_str = ", ".join(p['allergies'])
                        
                        print(f"      Conditions: {cond_str}")
                        print(f"      Allergies:  {allg_str}")
                        critical_keywords = ["diabetes", "cardiac", "heart", "asthma"]
                        is_critical = False
                        for c in p['conditions']:
                            for k in critical_keywords:
                                if k in c.lower():
                                    is_critical = True
                        
                        if is_critical:
                            print(f"      \033[91m[!] ALERT: High Risk Patient ({cond_str})\033[0m")
                        
                        print("-" * 20)

            #OPTION 3
            elif choice == '3':
                query = input("\nEnter Condition to search (e.g., Diabetes): ").lower()
                found = False
                print(f"\n--- Search Results for '{query}' ---")
                for p in health_logic.patients_db.values():
                    match = False
                    for c in p['conditions']:
                        if query in c.lower():
                            match = True
                    
                    if match:
                        print(f"FOUND: {p['name']} (ID: {p['id']})")
                        found = True
                
                if not found:
                    print("No patients found with that condition.")

            #OPTION 4
            elif choice == '4':
                p_id = int(input("Enter ID to Delete: "))
                if health_logic.delete_patient(p_id):
                    print(f"[Success] Patient {p_id} deleted.")
                else:
                    print("[!] ID not found.")

            #OPTION 5
            elif choice == '5':
                print("Generating Graph...")
                show_graph()

            #OPTION 6
            elif choice == '6':
                print("Saving data... Exiting.")
                break
            
            else:
                print("Invalid option.")

        except ValueError:
            print("\n[!] Input Error: Please enter numbers where required (ID, Age, Weight).")
        except Exception as e:
            print(f"\n[!] Critical Error: {e}")

if __name__ == "__main__":
    main_menu()