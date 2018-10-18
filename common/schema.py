# Schema for grabbing columns and putting into Cassandra
    
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
    

    
    
