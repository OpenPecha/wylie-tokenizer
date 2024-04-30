from pathlib import Path
from datasets import load_dataset

def download_dataset():
    dataset = load_dataset('spsither/tibetan_monolingual_A_filtered_deduped')
    # Iterate over all splits (e.g., 'train', 'test') and save them
    for split in dataset.keys():
        dataset[split].to_csv(f'path/to/save/{split}_dataset.csv')
    
def main():
    download_dataset()

if __name__ == "__main__":
    main()