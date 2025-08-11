import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BASE_URL_FACEBOOK = 'https://graph.facebook.com/v23.0/'
BASE_URL_TIKTOK = 'https://business-api.tiktok.com/'
ID_ADS_ACCOUNT_FLARIO_COSMETICS = os.environ.get('ID_ADS_ACCOUNT_FLARIO_COSMETICS')
ACCESS_TOKEN_FACEBOOK = os.environ.get('MARKER_ACCESS_FACEBOOK_NOT_EXPIRED')
ACCESS_TOKEN_TIKTOK = os.environ.get('ACCESS_TOKEN_TIKTOK')
ADVERTISER_ID_TIKTOK = os.environ.get('ADVERTISER_ID_TIKTOK')