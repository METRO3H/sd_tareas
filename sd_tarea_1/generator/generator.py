from distributions import generate_gaussian_distribution
import pandas
import time
import json
import requests

MAX_ITERATIONS = 100000
SEED = 123

def filter_dataset(dataset):
    dataset.columns = ["class_index", "question_title", "question_body", "yahoo_answer"]
    dataset.drop(columns = ["question_body"], inplace=True)
    
    # filter empty values for columns question_title and yahoo_answer
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
    print(gauss_row)
    
    URL = "http://middleware_server:8075"
    
    try:
        # Have to define the URL
        response = requests.post(URL, json=request_data)
        
        if response.status_code != 200:
            raise Exception(f"There is an error. Status code: {response.status_code}")
        
        print("    ↳ Proccessed successfully")
        
        return response.json()
       
    
    except Exception as e:
        print(f"    ↳ Error processing it :\n", e)
        return None

def get_data_from_gauss_distribution(dataset, gauss_distribution, index):
    selected_rows = dataset[dataset["class_index"] == gauss_distribution[index]]
    
    selected_row = selected_rows.sample(n=1, random_state=SEED)
    idx = selected_row.index[0]

    data = {
        "idx": int(idx),
        "question": selected_row["question_title"].item(),
        "yahoo_answer": selected_row["yahoo_answer"].item()
    }
    
    return data

def generate_traffic(dataset, gauss_distribution):
    
    for i in range(MAX_ITERATIONS):
        print(f"[{i+1}/{MAX_ITERATIONS}]", end=" ")
        
        gauss_data = get_data_from_gauss_distribution(dataset, gauss_distribution, i)
        
        request_data = {
            "gauss" : gauss_data,
        }
        
        
        response = request_server(request_data)
        
        if response is None:
            print(f"[Error] Request not processed")
            continue
        
        
        print(response)
        
        time.sleep(11)
        
        
    
if __name__ == "__main__":
    
    dataset = get_yahoo_dataset()

    if dataset is None:
        exit(1)

    gauss_distribution = generate_gaussian_distribution(MAX_ITERATIONS, SEED)
    
    if gauss_distribution is None:
        exit(1)
        
    print(" ")
    
    generate_traffic(dataset, gauss_distribution)
