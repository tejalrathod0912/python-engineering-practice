"""
Application Configuration Manager using Singleton Pattern

Run:
    python3 application_configuration_manager.py

What it demonstrates:
    - Singleton Pattern (only one config instance)
    - Centralized configuration access
    - Production-style environment usage
    - Clean separation of concerns
"""


from config.settings import Settings  # pyproject.toml must include src/ in packages

class ApplicationConfigManager:
    """
    Singleton class responsible for managing application configuration.

    Why Singleton?
    - Configuration should be loaded only once
    - Same config must be shared across entire application
    """

    _instance = None  # Holds single instance

    def __new__(cls):
        if cls._instance is None:
            # Create instance only once
            cls._instance = super().__new__(cls)

            # Load configuration once
            cls._instance._initialize()

        return cls._instance

    def _initialize(self):
        """
        Load configuration from Settings class.
        This runs only once in application lifecycle.
        """
        self.db_url = Settings.DB_URL
        self.kafka_broker = Settings.KAFKA_BROKER
        self.app_env = Settings.APP_ENV

    def get_database_url(self):
        """Return database connection string"""
        return self.db_url

    def get_kafka_broker(self):
        """Return Kafka broker address"""
        return self.kafka_broker

    def get_environment(self):
        """Return application environment (dev/staging/prod)"""
        return self.app_env


# ----------------------------
# Demo / Execution Layer
# ----------------------------

def singleton_demo():
    """
    Demonstrates Singleton behavior in real application usage.
    """

    config1 = ApplicationConfigManager()
    config2 = ApplicationConfigManager()

    print("=== CONFIG DEMO ===")

    print("DB URL:", config1.get_database_url())
    print("Kafka Broker:", config1.get_kafka_broker())
    print("Environment:", config1.get_environment())

    print("\n=== SINGLETON CHECK ===")
    print("config1 is config2:", config1 is config2)  # Must be True


if __name__ == "__main__":
    singleton_demo()
