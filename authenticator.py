"""Authenticator class."""


class Authenticator:
    """Checks credentials and limits failed attempts."""

    USER, PASSWORD, MAX_TRIES, LOCK_MINUTES = "user123", "Givemetheykey123", 3, 5

    def check(self, username, password):
        """True if the credentials match."""
        return username == self.USER and password == self.PASSWORD

    def login(self, ask=input):
        """Prompt for credentials; lock (message only) after 3 failures."""
        for _ in range(self.MAX_TRIES):
            if self.check(ask("Username: "), ask("Password: ")):
                return True
            print("Invalid credentials, try again.")
        print(f"Too many failed attempts. Locked for {self.LOCK_MINUTES} minutes.")
        return False