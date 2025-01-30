import os
import csv
import random
import heapq
from datetime import datetime, timedelta
import shutil


# list of current stock exchange of interest
se_dirs = ["LSE", "NASDAQ", "NYSE"]
output_dir_path = os.path.join(os.getcwd(), "output")

# here I wanted to get all the csv files in the input dir (alternative for the input number mentioned in the "Data&Inputs" of the pdf)
def process_dir(crt_dir):
    dir_path = os.path.join(os.getcwd(), crt_dir)
    if os.path.isdir(dir_path):
        csv_files = []
        for file in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file)) and file.endswith('.csv'):
                csv_files.append(file)
        return csv_files
    else:
        print("Directory not found: {0}".format(dir_path))
        return []


def get_random_set_points(crt_dir, input_file):
    file_path = os.path.join(os.getcwd(), crt_dir, input_file)
    print("Processing stock from {0}".format(file_path))
    with open(file_path, newline='', encoding='utf-8') as f:
        stock_info = list(csv.reader(f))

    #make sure that I have at least 10 data points from the random point
    random_entry_day = random.randint(0, len(stock_info)-10)

    return stock_info[random_entry_day:random_entry_day + 10]


def predict_stock(crt_dir, input_filename, data_points):
    # for the first predicted value, being only 10 values, we could just sort a tiny list
    # but for real case purposes, we could use a MAX-Heap - second highest value will be second in heap

    n_name = data_points[0][0]

    next_three_days = []
    last_data_point_day = datetime.strptime(data_points[-1][1], "%d-%m-%Y")
    for i in range(1,4):
        next_three_days.append((last_data_point_day + timedelta(days=i)).strftime("%d-%m-%Y"))

    
    n1_val = sorted([p[2] for p in data_points])[-2]
    n2_val = round(float(n1_val) + abs(float(data_points[-1][2]) - float(n1_val)) / 2 , 2)
    n3_val = round(n2_val + (float(n1_val) - n2_val) / 4 , 2)

    next_three_vals = [n1_val, n2_val, n3_val]
    
    for i, date in enumerate(next_three_days):
        data_points.append([n_name, date, next_three_vals[i]])

    # start writing output
    output_filename = "output_" + input_filename
    os.makedirs(output_dir_path, exist_ok=True)
    full_output_path = os.path.join(output_dir_path, output_filename)
    with open(full_output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        
        # Write multiple rows to the file
        writer.writerows(data_points)


if __name__ == "__main__":
    dirs_to_process = []

    # a switch case would work here but will use what python is offering us xD
    print("Please choose the desired stock exchange. Input is case insensitive. \nYou also can choose ALL to go through all directories:")
    while True:
        print("1. LSE")
        print("2. NASDAQ")
        print("3. NYSE")
        print("4. ALL (to process all directories)")
        print("5. EXIT")
        
        choice = input("Enter the name of the directory or option: ").strip().upper()

        if choice == "EXIT":
            print("Thank you for using our primitive predictor xD")
            break

        # all case - process all dirs
        if choice == "ALL":
            dirs_to_process = se_dirs
            break

        # Check if the input is one of the available directories
        if choice in se_dirs:
            dirs_to_process.append(choice)
            break
        else:
            print("Invalid directory name. Please check your spelling or select a valid option.")
            continue

    if dirs_to_process:
        shutil.rmtree(output_dir_path)
        for crt_dir in dirs_to_process:
            input_files = process_dir(crt_dir)

            if input_files:
                for input_file in input_files:
                    random_set_points = get_random_set_points(crt_dir, input_file)
                    predict_stock(crt_dir, input_file, random_set_points)
            else:
                print("No input CSV files in {0} dir.".format(crt_dir))
