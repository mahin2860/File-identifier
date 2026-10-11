
import os
import shutil
import zipfile
import csv
from engine import CategorizationEngine, SUBJECT_DATA

def organize_files(input_path, output_path):
    engine = CategorizationEngine()
    
    # 1. Initialize Output Folder Structure
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    for level, subjects in SUBJECT_DATA.items():
        for sub_name in subjects:
            os.makedirs(os.path.join(output_path, level, sub_name), exist_ok=True)
    
    os.makedirs(os.path.join(output_path, "_Uncategorized"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "_Review_Required"), exist_ok=True)

    # 2. Process Input
    all_files_report = []
    
    # Handle both ZIP and Folder inputs
    if zipfile.is_zipfile(input_path):
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                if member.is_dir(): continue
                filename = os.path.basename(member.filename)
                res = engine.detect(filename, member.filename)
                
                # Determine Destination
                if res["level"] and res["subject"]:
                    dest_folder = os.path.join(output_path, res["level"], res["subject"])
                elif res["status"] == "review_required":
                    dest_folder = os.path.join(output_path, "_Review_Required")
                else:
                    dest_folder = os.path.join(output_path, "_Uncategorized")
                
                # Extract file
                with zip_ref.open(member) as source, open(os.path.join(dest_folder, filename), 'wb') as target:
                    shutil.copyfileobj(source, target)
                
                all_files_report.append([filename, member.filename, res["level"], res["subject"], res["status"]])
    else:
        for root, dirs, files in os.walk(input_path):
            for filename in files:
                rel_path = os.path.relpath(os.path.join(root, filename), input_path)
                res = engine.detect(filename, rel_path)
                
                if res["level"] and res["subject"]:
                    dest_folder = os.path.join(output_path, res["level"], res["subject"])
                elif res["status"] == "review_required":
                    dest_folder = os.path.join(output_path, "_Review_Required")
                else:
                    dest_folder = os.path.join(output_path, "_Uncategorized")
                
                shutil.copy2(os.path.join(root, filename), os.path.join(dest_folder, filename))
                all_files_report.append([filename, rel_path, res["level"], res["subject"], res["status"]])

    # 3. Generate CSV Report
    with open(os.path.join(output_path, "report.csv"), "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Original Path", "Level", "Subject", "Status"])
        writer.writerows(all_files_report)

    print(f"Successfully organized files into: {output_path}")
    print(f"Total files processed: {len(all_files_report)}")

if __name__ == "__main__":
    # You can change these paths as needed
    INPUT = "input" 
    OUTPUT = "output"
    
    if not os.path.exists(INPUT) or not os.listdir(INPUT):
        print("Please put your files or ZIP in the 'input' folder first.")
    else:
        # If input folder contains a ZIP, use that, otherwise process folder
        input_target = INPUT
        for f in os.listdir(INPUT):
            if f.endswith(".zip"):
                input_target = os.path.join(INPUT, f)
                break
        
        organize_files(input_target, OUTPUT)
