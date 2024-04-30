from pathlib import Path
import pyewts
import csv
from concurrent.futures import ProcessPoolExecutor
import os

converter = pyewts.pyewts()

def convert_to_wylie(text):
    return converter.toWylie(text)

def process_chunk(chunk, executor):
    # Map convert_to_wylie over all lines in the chunk
    results = list(executor.map(convert_to_wylie, (line[0] for line in chunk if line)))
    return results

def write_csv(csv_data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in csv_data:
            writer.writerow([row])

def read_and_process_csv(csv_path, executor):
    chunk_size = 10000  # Adjust this based on your memory and performance needs
    results = []

    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        chunk = []
        for i, line in enumerate(reader):
            chunk.append(line)
            if (i + 1) % chunk_size == 0:
                results.extend(process_chunk(chunk, executor))
                chunk = []
        if chunk:  # Process any remaining lines
            results.extend(process_chunk(chunk, executor))
    return results

def main():
    csv_path = Path("./data/train_dataset.csv")
    output_path = Path("./data/wylie_dataset.csv")
    cores = os.cpu_count()  # Get the number of CPU cores

    # Create a single ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=cores) as executor:
        # Process the CSV file and convert it to Wylie
        converted_data = read_and_process_csv(csv_path, executor)

    # Write the converted data to a new CSV file
    write_csv(converted_data, output_path)

if __name__ == "__main__":
    main()
