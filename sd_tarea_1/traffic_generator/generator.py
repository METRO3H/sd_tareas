from distributions import generate_gaussian_distribution
import pandas
import time
import json
import requests

MAX_ITERATIONS = 100000

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
    print("REQUEST SERVER", "\n")
    
    # convert to json
    request_data = json.dumps(request_data, indent=6, ensure_ascii=True)
 
    try:
        # Have to define the URL
        URL = "http://localhost:8000/api/v1/qa_score"
        response = requests.post(URL, data=request_data)
        
        if response.status_code != 200:
            raise Exception(f"There is an error. Status code: {response.status_code}")
        
        print("[Status] Request sent successfully")
        
        return response.json()
       
    
    except Exception as e:
        print(f"[Error] Request not sent:\n", e)
        return None
    
def generate_traffic():
    dataset = get_yahoo_dataset()
    
    if dataset is None:
        exit(1)
    
    gauss_distribution = generate_gaussian_distribution(MAX_ITERATIONS)
    
    if gauss_distribution is None:
        exit(1)
    
    
    for i in range(MAX_ITERATIONS):
        print(f"\n[{i+1}/{MAX_ITERATIONS}]", end=" ")
        
        selected_rows = dataset[dataset["class_index"] == gauss_distribution[i]]
        
        selected_row = selected_rows.sample(n=1)

        request_data = {
            "question_title": selected_row["question_title"].item(),
            "yahoo_answer": selected_row["yahoo_answer"].item()
        }
        
        response = request_server(request_data)
        
        if response is None:
            continue
        
        response_json = json.dumps(response.json(), indent=6, ensure_ascii=True)
        
        print(response_json)
        
        time.sleep(3)
        
        
    
if __name__ == "__main__":
    generate_traffic()