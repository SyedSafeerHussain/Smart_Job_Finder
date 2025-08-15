import csv
import os
def save_to_csv(data,filename):
    folder="data"
    os.makedirs(folder,exist_ok=True)
    filepath=os.path.join(folder,filename)
    if not data:
        print("NO data save in csv")
    keys=data[0].keys()
    with open(filepath,"w",newline="",encoding="utf-8")as f:
        writer=csv.DictWriter(f,fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} records to {filepath}")


def read_csv(filename):
    """Read CSV file and return data as list of dictionaries"""
    folder = "data"
    filepath = os.path.join(folder, filename)
    data = []
    
    # Create data directory if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"CSV file not found: {filepath}")
        return data
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
    
    return data