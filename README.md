# tech_challenge_lseg
LSEG Pre-Interview Coding Challenge; Backend

## Description

This script does a primitive prediction of the three next stock values of some given data points.

## Requirements

- Python 3.x
- Required libraries (all are in standard Python library):
  - `os`
  - `csv`
  - `random`
  - `datetime`
  - `shutil`

## Set Up

- No specific action required, the input dirs

## How to Run

```bash
python3 predict_stock_price.py
```

The app will prompt the user with a menu to select different options:
- ALL to take all the directories as input
- LSE/NASDAQ/NYSE if the user wants to look only over a specific dir
- EXIT to exit the script

The input is case insensitive and if invalid option is provided, will loop until a valid option or exit command.

## Input

The script will go through the list of predefined input dirs from the given archive.
It will take all the csv files in that selected dir and will try to predict the next 3 stock values.

## Output

The output file/files will all be placed in the output directory with output_ prefix followed by the filename for that specific iteration.
Before each new run, the output dir will be cleaned.

## Follow UP

- If any other input dirs are added, they should be added also in *se_dirs* in the main script.

## Step by Step into the Script

1. First there is the prompt for the user, in order to decide what input to use next
    - After this, a previous run output cleanup is performed
2. With the desired directory, the input files are obtained using *process_dir* function
    - This will take only the .csv files in the current directory
3. For each input file, the *get_random_set_points* function will:
    - first check for valid input data
    - take a random starting point in the input
    - return the list of the 10 data entries from the starting point
4. Will call the *predict_stock* funtion which will:
    - compute next three days
    - compute next three values
    - write the output in a dedicated file in an output directory
