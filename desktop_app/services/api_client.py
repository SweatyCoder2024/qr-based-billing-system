# desktop_app/services/api_client.py

import requests
from typing import List, Dict, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def _handle_error(self, error: requests.exceptions.RequestException) -> Optional[Dict]:
        print(f"An error occurred: {error}")
        if error.response is not None:
            try:
                return error.response.json()
            except requests.exceptions.JSONDecodeError:
                return {"detail": error.response.text}
        return None

    def get_items(self, limit: int = 2000, skip: int = 0) -> List[Dict]:
        try:
            url = f"{self.base_url}/api/items/?limit={limit}&skip={skip}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return []

    def get_item(self, item_id: int) -> Optional[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/items/{item_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None

    def create_item(self, item_data: Dict) -> Optional[Dict]:
        try:
            response = self.session.post(f"{self.base_url}/api/items/", json=item_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def update_item(self, item_id: int, item_data: Dict) -> Optional[Dict]:
        try:
            response = self.session.put(f"{self.base_url}/api/items/{item_id}", json=item_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def delete_item(self, item_id: int) -> bool:
        try:
            response = self.session.delete(f"{self.base_url}/api/items/{item_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return False
    
    def upload_items_file(self, file_path: str) -> Optional[Dict]:
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f)}
                response = self.session.post(f"{self.base_url}/api/items/upload-file/", files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
        except FileNotFoundError:
            print(f"File not found at path: {file_path}")
            return {"detail": "File not found on local machine."}

    def create_session(self) -> Dict:
        try:
            response = self.session.post(f"{self.base_url}/api/sessions/create")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred creating session: {e}")
            return {}

    def get_dashboard_stats(self) -> Optional[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/dashboard/stats")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None
    
    def get_item_qr(self, item_id: int) -> Optional[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/items/{item_id}/qr")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None

    # --- NEW FUNCTIONS ---
    def get_active_sessions(self) -> List[Dict]:
        """Fetches all active sessions (bills) from the backend."""
        try:
            response = self.session.get(f"{self.base_url}/api/sessions/active")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return []

    def get_session_qr(self, session_id: str) -> Optional[Dict]:
        """Fetches the QR code for a specific existing session."""
        try:
            response = self.session.get(f"{self.base_url}/api/sessions/{session_id}/qr")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None
            
    def get_order_for_session(self, session_id: str) -> Optional[Dict]:
        """Fetches the pending order for a specific session."""
        try:
            response = self.session.get(f"{self.base_url}/api/orders/session/{session_id}")
            if response.status_code == 404:
                return None 
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None