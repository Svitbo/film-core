from google.cloud import storage

from ..config import config

storage_client = storage.Client()

static_bucket_name = config.GCP_STATIC_BUCKET
static_bucket = storage_client.get_bucket(static_bucket_name)
