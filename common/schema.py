# Schema for grabbing columns and putting into Cassandra

FEATURE_SCHEMA = {
    "table_name": "demo_columns",
    "options": {
        "primary_key": ["dataset_id", "column"],
    },
    "columns": {
        "dataset_id": "bigint",
        "column": "text"
    }
}
    
SCORING_SCHEMA = {
    "table_name": "scores",
    "options": {
        "primary_key": ["dataset_id", "customer_id"],
    },
    "columns": {
        "customer_id": "text",
        "dataset_id": "bigint",
        "score": "float"
    }
}
    

    
    
