from supabase import create_client
from flask import current_app

def get_db():
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_SERVICE_KEY"]
    )
