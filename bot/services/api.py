"""API service to communicate with Django backend"""

import aiohttp
from typing import Optional, Dict, Any


class APIService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to backend"""
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                if method == 'GET':
                    async with session.get(url, params=data) as response:
                        res_json = await response.json()
                        if response.status >= 400:
                            return {"error": res_json}
                        return res_json
                elif method == 'POST':
                    async with session.post(url, json=data) as response:
                        res_json = await response.json()
                        if response.status >= 400:
                            return {"error": res_json}
                        return res_json
                elif method == 'PATCH':
                    async with session.patch(url, json=data) as response:
                        res_json = await response.json()
                        if response.status >= 400:
                            return {"error": res_json}
                        return res_json
            except Exception as e:
                print(f"API Error: {e}")
                return {"error": str(e)}
    
    async def telegram_login(self, telegram_user_id: int, username: str, first_name: str, last_name: str = "") -> Dict:
        """Login or register user via Telegram"""
        data = {
            "telegram_user_id": telegram_user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
        return await self._request('POST', '/users/telegram-login/', data)
    
    async def get_user(self, telegram_user_id: int) -> Dict:
        """Get user info"""
        return await self._request('GET', '/users/me/', {'telegram_user_id': telegram_user_id})
    
    async def update_language(self, telegram_user_id: int, language: str) -> Dict:
        """Update user language preference"""
        data = {
            "telegram_user_id": telegram_user_id,
            "language": language,
        }
        return await self._request('PATCH', '/users/language/', data)
    
    async def verify_phone(self, telegram_user_id: int, phone: str) -> Dict:
        """Verify and save user phone number"""
        data = {
            "telegram_user_id": telegram_user_id,
            "phone_number": phone,  # Match backend PhoneVerifySerializer
        }
        return await self._request('POST', '/users/phone-verify/', data)
    
    async def get_active_orders(self, telegram_user_id: int) -> Dict:
        """Get user's active orders"""
        return await self._request('GET', '/orders/active/', {'telegram_user_id': telegram_user_id})
    
    async def get_all_orders(self, telegram_user_id: int) -> Dict:
        """Get all user orders"""
        return await self._request('GET', '/orders/', {'telegram_user_id': telegram_user_id})
    
    async def send_message(self, telegram_user_id: int, message: str) -> Dict:
        """Send chat message from user"""
        data = {
            "telegram_user_id": telegram_user_id,
            "message": message,
        }
        return await self._request('POST', '/chat/send/', data)
