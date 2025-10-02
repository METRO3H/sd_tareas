import pandas


def limit_dataset(dataset, max_rows=20000, seed=123):
    if len(dataset) <= max_rows:
        return dataset
    
    n_classes = dataset["class_index"].nunique()
    per_class = max_rows // n_classes
    
    subset = (
        dataset.groupby("class_index", group_keys=False)
        .sample(n=min(per_class, len(dataset)), random_state=seed)
    )
    
    return subset.reset_index(drop=True)



def filter_dataset(dataset):
    dataset.columns = ["class_index", "question_title", "question_body", "yahoo_answer"]
    dataset.drop(columns=["question_body"], inplace=True)
    dataset.dropna(subset=["question_title", "yahoo_answer"], inplace=True)
    dataset.reset_index(drop=True, inplace=True)
    
    dataset = limit_dataset(dataset, max_rows=20000, seed=123)
    
    return dataset

def get_yahoo_dataset():
    try:
        dataset_raw = pandas.read_csv("./dataset/qa_yahoo.csv", header=None, sep=",", quotechar='"')
        
        return dataset_raw
    except Exception as e:
        print(f"[Error] Dataset not loaded:\n", e)
        return None