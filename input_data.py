# input_data.py

list_of_inputs = [
    {
        "filepath": r"deploy/test1/random.yml",
        "key": "spec.replicas",
        "scale_up_replicas_count": 10,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy/test1/random1.yml",
        "key": "spec.replicas.data",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy/test1/random2.yml",
        "key": "data.PAAS_FRONTNED_REPLICAS",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy2/random3.yml",
        "key": "spec.replicas",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy2/random3.yml",
        "key": "data.PAAS_FRONTNED_REPLICAS",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy3/random4.yml",
        "key": "data.PAAS_FRONTNED_REPLICAS",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    {
        "filepath": r"deploy3/random4.yml",
        "key": "spec.replicas",
        "scale_up_replicas_count": 3,
        "scale_down_replicas_count": 0
    },
    # Add more input dictionaries as needed
]
