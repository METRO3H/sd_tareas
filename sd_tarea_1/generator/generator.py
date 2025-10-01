from gauss_distribution import generate_gaussian_dataset_distribution
from checkpoint import load_checkpoint, save_checkpoint
from zipf_distribution import generate_zipf_dataset_distribution
from dataset import get_yahoo_dataset, filter_dataset
import requests
import numpy
import time

MAX_ITERATIONS = 100000
SEED = 123

RNG = numpy.random.default_rng(SEED)


def request_server(request_data):
    gauss_row = f'{request_data["gauss"]["idx"]} - "{request_data["gauss"]["question"]}"'
    zipf_row = f'{request_data["zipf"]["idx"]} - "{request_data["zipf"]["question"]}"'
    print(f"    ↳ Gauss: {gauss_row}")
    print(f"    ↳ Zipf : {zipf_row}")

    URL = "http://middleware_server:8075"
    
    try:
        response = requests.post(URL, json=request_data)
        
        if response.status_code != 200:
            raise Exception(f"There is an error. Status code: {response.status_code}")
        
        print("    ↳ Processed successfully")
        return response.json()
    
    except Exception as e:
        print(f"    ↳ Error processing it :")
        print(f"    ↳ {e}")
        return None

def get_data_from_distribution(dataset, distribution_indices, index):
    row_idx = distribution_indices[index]
    selected_row = dataset.iloc[row_idx]
    
    return {
        "idx": int(row_idx),
        "question": selected_row["question_title"],
        "yahoo_answer": selected_row["yahoo_answer"]
    }


def generate_traffic(dataset, gauss_indices, zipf_indices, start_index=0):
    for i in range(start_index, MAX_ITERATIONS):
        print(" ")
        progress = round(i / MAX_ITERATIONS * 100, 2)
        
        print(f"[{progress}%][{i+1}/{MAX_ITERATIONS}] Starting request")

        gauss_data = get_data_from_distribution(dataset, gauss_indices, i)
        zipf_data  = get_data_from_distribution(dataset, zipf_indices, i)
        
        request_data = {
            "gauss": gauss_data,
            "zipf": zipf_data,
        }
        
        response = request_server(request_data)
        
        save_checkpoint(i)
        
        if response is None:
            print(f"[Error] Request not processed")
            continue
        
        # print(response)

def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}h, {minutes}min, {secs}s"

if __name__ == "__main__":
    
    start_time = time.time()
    
    dataset_raw = get_yahoo_dataset()

    if dataset_raw is None:
        exit(1)
        
    dataset = filter_dataset(dataset_raw)
    
    if dataset is None:
        exit(1)
        
    print("[Status] Dataset loaded successfully | Rows: {:,}".format(len(dataset)))
    
    
    
    # Generamos ambas distribuciones
    gauss_indices = generate_gaussian_dataset_distribution(dataset, MAX_ITERATIONS, SEED)
    zipf_indices  = generate_zipf_dataset_distribution(dataset, MAX_ITERATIONS, SEED, a=1.05)
    
    if gauss_indices is None or zipf_indices is None:
        exit(1)
        
    print(" ")
    
    start_index = load_checkpoint()
    
    print(f"[Resume] Starting from iteration {start_index + 1}")

    generate_traffic(dataset, gauss_indices, zipf_indices, start_index)

    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    print(f"\n[Status] Process finished in {format_time(elapsed_time)}")