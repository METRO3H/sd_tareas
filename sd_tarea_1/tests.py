
import json

gauss_tests_config = {
    
        "gauss_lru_2mb": {
            "host": "redis_1_gauss_lru_2mb",
            "port": 6379,
        },
        
        "gauss_lru_5mb": {
            "host": "redis_2_gauss_lru_5mb",
            "port": 6380,
        },
        
        "gauss_lru_10mb": {
            "host": "redis_3_gauss_lru_10mb",
            "port": 6381,
        },
        
        "gauss_lfu_2mb": {
            "host": "redis_4_gauss_lfu_2mb",
            "port": 6382,
        },
        
        "gauss_lfu_5mb": {
            "host": "redis_5_gauss_lfu_5mb",
            "port": 6383,
        },
        
        "gauss_lfu_10mb": {
            "host": "redis_6_gauss_lfu_10mb",
            "port": 6384,
        }

}

# poisson_tests_config = {
#     "poisson_lru_2mb": {
#         "host": "redis_7",
#         "port": 6385,
#     },
    
#     "poisson_lru_5mb": {
#         "host": "redis_8",
#         "port": 6386,
#     },
# }



# get the keys of the dictionary
gauss_tests = list(gauss_tests_config.keys())

# tests_config = {**gauss_tests_config, **poisson_tests_config}
tests_config = {**gauss_tests_config}


if __name__ == "__main__":
    print("All tests configurations:", "\n")
    print(json.dumps(tests_config, indent=4))
