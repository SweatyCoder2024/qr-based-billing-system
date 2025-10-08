# desktop_app/main.py

import sys
import asyncio
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QObject, pyqtSignal

from ui.billing_tab import BillingTab
from ui.items_tab import ItemsTab
from ui.dashboard_tab import DashboardTab
from services.api_client import APIClient
from services.websocket_client import WebSocketClient

class UIMessageBridge(QObject):
    message_received = pyqtSignal(dict)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Billing System")
        self.setGeometry(100, 100, 1200, 800)

        self.api_client = APIClient(base_url="http://localhost:8000")
        self.websocket_client = WebSocketClient()
        self.ws_thread = None
        self.ui_bridge = UIMessageBridge()

        self.tabs = QTabWidget()
        self.billing_tab = BillingTab(self.api_client) 
        self.items_tab = ItemsTab(self.api_client)
        self.dashboard_tab = DashboardTab(self.api_client)

        self.tabs.addTab(self.billing_tab, "Billing")
        self.tabs.addTab(self.items_tab, "Item Management")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.setCentralWidget(self.tabs)

        self.billing_tab.session_created.connect(self.start_websocket_connection)
        self.ui_bridge.message_received.connect(self.billing_tab.handle_websocket_message)

    def start_websocket_connection(self, session_id: str):
        """Stops any old listener and starts a new one."""
        print(f"Main window received session ID: {session_id}, preparing WebSocket listener.")
        self.websocket_client.stop()

        def run_websocket_loop():
            def thread_safe_handler(message):
                self.ui_bridge.message_received.emit(message)

            self.websocket_client.set_message_handler(thread_safe_handler)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.websocket_client.connect_and_listen(session_id))

        self.ws_thread = threading.Thread(target=run_websocket_loop, daemon=True)
        self.ws_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())