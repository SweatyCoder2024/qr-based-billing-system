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

    def get_items(self, limit: int = 1000, skip: int = 0) -> List[Dict]:
        """Fetches all items from the backend API."""
        try:
            url = f"{self.base_url}/api/items/?limit={limit}&skip={skip}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return []

    def get_item(self, item_id: int) -> Optional[Dict]:
        """Fetches a single item by its ID."""
        try:
            response = self.session.get(f"{self.base_url}/api/items/{item_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return None

    def create_item(self, item_data: Dict) -> Optional[Dict]:
        """Sends a request to create a new item."""
        try:
            response = self.session.post(f"{self.base_url}/api/items/", json=item_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def update_item(self, item_id: int, item_data: Dict) -> Optional[Dict]:
        """Sends a request to update an item."""
        try:
            response = self.session.put(f"{self.base_url}/api/items/{item_id}", json=item_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def delete_item(self, item_id: int) -> bool:
        """Sends a request to delete an item."""
        try:
            response = self.session.delete(f"{self.base_url}/api/items/{item_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self._handle_error(e)
            return False

    def create_session(self) -> Dict:
        # ... (this function is unchanged)
        try:
            response = self.session.post(f"{self.base_url}/api/sessions/create")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred creating session: {e}")
            return {}