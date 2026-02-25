import time
import hmac
import hashlib
import requests
import urllib.parse
import os
from dotenv import load_dotenv
from .logging_config import setup_logger

load_dotenv()
logger = setup_logger()

class BinanceFuturesClient:
    """
    Client for interacting with Binance Futures API
    Handles authentication, signature generation, and HTTP requests
    """
    
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Missing API credentials in .env file")
    
    def _sign(self, params: dict) -> str:
        """
        Generate HMAC SHA256 signature for API request
        
        Args:
            params: Request parameters
            
        Returns:
            Hexadecimal signature string
        """
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.secret_key.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def send_signed_request(self, endpoint: str, params: dict) -> dict:
        """
        Send signed POST request to Binance API
        
        Args:
            endpoint: API endpoint path
            params: Request parameters
            
        Returns:
            JSON response from API
            
        Raises:
            requests.exceptions.RequestException: On network or API errors
        """
        url = self.base_url + endpoint
        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self._sign(params)
        
        headers = {"X-MBX-APIKEY": self.api_key}
        
        try:
            logger.info(f"API Request - Endpoint: {endpoint}, Params: {params}")
            response = requests.post(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            logger.info(f"API Response - Status: {response.status_code}, Data: {result}")
            return result
        except requests.exceptions.Timeout:
            logger.error("API Request timeout")
            raise Exception("Network timeout - please check your connection")
        except requests.exceptions.ConnectionError:
            logger.error("API Connection failed")
            raise Exception("Network connection failed - please check your internet")
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.headers.get('content-type') == 'application/json' else {}
            error_msg = error_data.get('msg', e.response.text)
            error_code = error_data.get('code', 'Unknown')
            logger.error(f"API HTTP Error: {e.response.status_code} - Code: {error_code}, Message: {error_msg}")
            raise Exception(f"Binance API Error (Code {error_code}): {error_msg}")
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
    
    def send_algo_order_request(self, endpoint: str, params: dict) -> dict:
        """
        Send signed POST request to Binance Algo Order API (for STOP orders)
        
        Args:
            endpoint: API endpoint path
            params: Request parameters
            
        Returns:
            JSON response from API
        """
        # Use the same logic as regular orders but different endpoint
        return self.send_signed_request(endpoint, params)
