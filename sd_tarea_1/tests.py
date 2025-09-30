
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

zipf_tests_config = {
    "zipf_lru_2mb": {
        "host": "redis_7_zipf_lru_2mb",
        "port": 6385,
    },

    "zipf_lru_5mb": {
        "host": "redis_8_zipf_lru_5mb",
        "port": 6386,
    },
    
    "zipf_lru_10mb": {
        "host": "redis_9_zipf_lru_10mb",
        "port": 6387,
    },
    
    "zipf_lfu_2mb": {
        "host": "redis_10_zipf_lfu_2mb",
        "port": 6388,
    },
    
    "zipf_lfu_5mb": {
        "host": "redis_11_zipf_lfu_5mb",
        "port": 6389,
    },
    
    "zipf_lfu_10mb": {
        "host": "redis_12_zipf_lfu_10mb",
        "port": 6390,
    }
}



# get the keys of the dictionary
gauss_tests = list(gauss_tests_config.keys())

zipf_tests = list(zipf_tests_config.keys())

# tests_config = {**gauss_tests_config, **poisson_tests_config}
tests_config = {**gauss_tests_config, **zipf_tests_config}


if __name__ == "__main__":
    print("All tests configurations:", "\n")
    print(json.dumps(tests_config, indent=4))
