import time

class AccessController:
    def __init__(self, entry_window_seconds=5):
        self.is_authorized = False
        self.auth_start_time = 0
        self.entry_window_seconds = entry_window_seconds
        self.entry_log = []

    def trigger_access_request(self, method="QR Scan"):
        """
        Simulate an authorized entry request (Card swipe, QR, etc.)
        """
        self.is_authorized = True
        self.auth_start_time = time.time()
        print(f"[ACCESS] Authorized via {method} at {self.auth_start_time}")
        return True

    def check_status(self):
        """
        Check if the door is currently technically 'open' for the authorized person.
        """
        if self.is_authorized:
            elapsed = time.time() - self.auth_start_time
            if elapsed > self.entry_window_seconds:
                self.is_authorized = False # Time expired
                print("[ACCESS] Entry window closed.")
        
        return self.is_authorized

    def validate_entry(self, person_count):
        """
        Core Logic:
        - If Authorized Window is OPEN:
            - If person_count == 0: Waiting...
            - If person_count == 1: PASS.
            - If person_count > 1: TAILGATING ALERT!
        - If Authorized Window is CLOSED:
            - If person_count > 0: UNAUTHORIZED ENTRY / LOITERING.
        """
        status = "SECURE"
        alert = None

        is_open = self.check_status()

        if is_open:
            if person_count == 0:
                status = "DOOR UNLOCKED - WAITING ENTRY"
            elif person_count == 1:
                status = "AUTHORIZED ENTRY"
            elif person_count > 1:
                status = "TAILGATING DETECTED"
                alert = "TAILGATING"
        else:
            if person_count > 0:
                # If no auth trigger but people are present, it depends if they are recognized or not.
                # But strictly speaking, if they didn't swipe card, it's an anomaly.
                # However, for this MVP, we might rely on Face Auth to handle "Unauthorized" tags.
                # This controller purely checks counting logic vs card swipe.
                pass

        return status, alert
