# Schema for grabbing columns and putting into Cassandra
    
SCORING_SCHEMA = {
    "table_name": "model_scores",
    "options": {
        "primary_key": ["model_id", "customer_id"],
    },
    "columns": {
        "customer_id": "text",
        "model_id": "bigint",
        "score": "float"
    }
}
    

    
    
