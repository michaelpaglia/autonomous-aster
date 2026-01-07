"""
AsterDEX Futures API Client with Web3 ECDSA Authentication
"""
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
from typing import Dict, Any, Optional
import json


class AsterDEXClient:
    def __init__(self, base_url: str, api_wallet: str, private_key: str, user_address: Optional[str] = None):
        """
        Initialize AsterDEX client with Web3 authentication

        Args:
            base_url: API base URL (e.g., https://fapi.asterdex.com)
            api_wallet: Signer wallet address
            private_key: Private key for signing (with or without 0x prefix)
            user_address: Main account wallet address (defaults to api_wallet if not provided)
        """
        self.base_url = base_url.rstrip('/')
        self.api_wallet = api_wallet
        self.user_address = user_address or api_wallet

        # Ensure private key has 0x prefix
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key

        self.account = Account.from_key(private_key)
        self.w3 = Web3()

    def _get_nonce(self) -> int:
        """Get current timestamp in microseconds for nonce"""
        return int(time.time() * 1_000_000)

    def _sort_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sort parameters by ASCII key order"""
        return {k: params[k] for k in sorted(params.keys())}

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate ECDSA signature for request parameters

        Args:
            params: Request parameters (already sorted)

        Returns:
            Hex signature string
        """
        # Get nonce (current timestamp in microseconds)
        nonce = self._get_nonce()

        # Convert all params to strings
        str_params = {k: str(v) for k, v in params.items()}

        # Create parameter string for ABI encoding
        param_types = ['address', 'address', 'uint256']
        param_values = [self.user_address, self.api_wallet, nonce]

        # Add sorted parameters
        for key in sorted(str_params.keys()):
            param_types.append('string')
            param_types.append('string')
            param_values.append(key)
            param_values.append(str_params[key])

        # ABI encode
        encoded = self.w3.codec.encode(param_types, param_values)

        # Keccak hash
        message_hash = self.w3.keccak(encoded)

        # Sign with private key (using unsafe hash signing for raw hash)
        signed_message = self.account.unsafe_sign_hash(message_hash)

        # Return signature as hex string
        return signed_message.signature.hex()

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     requires_signature: bool = False) -> Dict[str, Any]:
        """
        Make HTTP request to AsterDEX API

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            params: Request parameters
            requires_signature: Whether this endpoint requires authentication

        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if requires_signature:
            # Sort parameters
            sorted_params = self._sort_params(params)

            # Add authentication parameters
            sorted_params['user'] = self.user_address
            sorted_params['signer'] = self.api_wallet
            sorted_params['nonce'] = self._get_nonce()

            # Generate signature
            signature = self._generate_signature({k: v for k, v in sorted_params.items()
                                                 if k not in ['user', 'signer', 'nonce']})
            sorted_params['signature'] = signature

            params = sorted_params

        # Make request
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, data=params, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, data=params, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, data=params, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Check for errors
        response.raise_for_status()

        return response.json()

    # ==================== Market Data Endpoints ====================

    def ping(self) -> Dict[str, Any]:
        """Test connectivity to the API"""
        return self._make_request('GET', '/fapi/v3/ping')

    def get_server_time(self) -> Dict[str, Any]:
        """Get server time"""
        return self._make_request('GET', '/fapi/v3/time')

    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get exchange information"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/exchangeInfo', params)

    def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """Get order book depth"""
        params = {'symbol': symbol, 'limit': limit}
        return self._make_request('GET', '/fapi/v3/depth', params)

    def get_recent_trades(self, symbol: str, limit: int = 500) -> Dict[str, Any]:
        """Get recent trades"""
        params = {'symbol': symbol, 'limit': limit}
        return self._make_request('GET', '/fapi/v3/trades', params)

    def get_mark_price(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get mark price"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/markPrice', params)

    def get_ticker_24h(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get 24hr ticker price change statistics"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/ticker/24hr', params)

    def get_ticker_price(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get latest price"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/ticker/price', params)

    # ==================== Trading Endpoints ====================

    def place_order(self, symbol: str, side: str, order_type: str, quantity: Optional[float] = None,
                   price: Optional[float] = None, **kwargs) -> Dict[str, Any]:
        """
        Place a new order

        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: BUY or SELL
            order_type: LIMIT, MARKET, STOP, TAKE_PROFIT, etc.
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            **kwargs: Additional parameters (timeInForce, stopPrice, etc.)
        """
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': order_type.upper(),
        }

        if quantity is not None:
            params['quantity'] = quantity
        if price is not None:
            params['price'] = price

        params.update(kwargs)

        return self._make_request('POST', '/fapi/v3/order', params, requires_signature=True)

    def cancel_order(self, symbol: str, order_id: Optional[int] = None,
                    orig_client_order_id: Optional[str] = None) -> Dict[str, Any]:
        """Cancel an active order"""
        params = {'symbol': symbol}
        if order_id:
            params['orderId'] = order_id
        if orig_client_order_id:
            params['origClientOrderId'] = orig_client_order_id

        return self._make_request('DELETE', '/fapi/v3/order', params, requires_signature=True)

    def cancel_all_orders(self, symbol: str) -> Dict[str, Any]:
        """Cancel all open orders on a symbol"""
        params = {'symbol': symbol}
        return self._make_request('DELETE', '/fapi/v3/allOpenOrders', params, requires_signature=True)

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get all open orders"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/openOrders', params, requires_signature=True)

    # ==================== Account Endpoints ====================

    def get_account_info(self) -> Dict[str, Any]:
        """Get current account information"""
        return self._make_request('GET', '/fapi/v3/account', {}, requires_signature=True)

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        return self._make_request('GET', '/fapi/v3/balance', {}, requires_signature=True)

    def get_position_risk(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get current position information"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/fapi/v3/positionRisk', params, requires_signature=True)

    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """Change initial leverage"""
        params = {'symbol': symbol, 'leverage': leverage}
        return self._make_request('POST', '/fapi/v3/leverage', params, requires_signature=True)
