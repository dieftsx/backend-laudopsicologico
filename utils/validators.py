import re
from typing import Optional

class Validators:
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate if password meets security requirements:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def validate_crp(crp: str) -> Optional[str]:
        """
        Validate CRP format and return formatted CRP if valid
        Format expected: XX/XXXXX (where X is a number)
        """
        crp = crp.strip()
        pattern = r"^\d{2}/\d{5}$"
        if not re.match(pattern, crp):
            return None
        return crp