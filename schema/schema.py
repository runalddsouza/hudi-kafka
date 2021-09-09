input_columns = {"product_id": str, "trade_id": str, "sequence": str, "price": float, "time": str, "volume_30d": str,
                 "low_24h": float, "volume_24h": str, "high_24h": float, "best_ask": float, "best_bid": float,
                 "last_size": float, "side": str}

avro_dict = {
    "type": "record",
    "name": "Cryptocurrency",
    "fields": [
        {"name": "product_id", "type": "string"},
        {"name": "trade_id", "type": "string"},
        {"name": "sequence", "type": "string"},
        {"name": "price", "type": "float"},
        {"name": "time", "type": "string"},
        {"name": "volume_30d", "type": "string"},
        {"name": "low_24h", "type": "float"},
        {"name": "volume_24h", "type": "string"},
        {"name": "high_24h", "type": "float"},
        {"name": "best_ask", "type": "float"},
        {"name": "best_bid", "type": "float"},
        {"name": "last_size", "type": "float"},
        {"name": "side", "type": "string"},
    ]
}
