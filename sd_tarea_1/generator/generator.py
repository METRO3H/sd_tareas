from gauss_distribution import generate_gaussian_dataset_distribution
from checkpoint import load_checkpoint, save_checkpoint
from zipf_distribution import generate_zipf_dataset_distribution
import pandas
import requests
import numpy

MAX_ITERATIONS = 100000
SEED = 123

RNG = numpy.random.default_rng(SEED)

def filter_dataset(dataset):
    dataset.columns = ["class_index", "question_title", "question_body", "yahoo_answer"]
    dataset.drop(columns=["question_body"], inplace=True)
    dataset.dropna(subset=["question_title", "yahoo_answer"], inplace=True)
    return dataset

def get_yahoo_dataset():
    try:
        dataset_raw = pandas.read_csv("./dataset/qa_yahoo.csv", header=None, sep=",", quotechar='"')
        dataset = filter_dataset(dataset_raw)
        print("[Status] Dataset loaded successfully")
        return dataset
    except Exception as e:
        print(f"[Error] Dataset not loaded:\n", e)
        return None

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
        print(f"    ↳ Error processing it :\n", e)
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
        print(f"[{i+1}/{MAX_ITERATIONS}] Starting request")

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

if __name__ == "__main__":
    dataset = get_yahoo_dataset()

    if dataset is None:
        exit(1)

    # Generamos ambas distribuciones
    gauss_indices = generate_gaussian_dataset_distribution(dataset, MAX_ITERATIONS, SEED)
    zipf_indices  = generate_zipf_dataset_distribution(dataset, MAX_ITERATIONS, SEED, a=1.5)
    
    if gauss_indices is None or zipf_indices is None:
        exit(1)
        
    print(" ")
    
    start_index = load_checkpoint()
    
    print(f"[Resume] Starting from iteration {start_index + 1}")

    generate_traffic(dataset, gauss_indices, zipf_indices, start_index)
