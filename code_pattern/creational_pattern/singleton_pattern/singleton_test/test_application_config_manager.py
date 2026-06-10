"""
This test file checks the behavior of the application configuration manager.

The main idea is easy to understand:
- The configuration manager should act like a single shared object.
- Asking for it twice should give the same object.
- The object should have the required settings loaded.

This makes sure the code behaves like a single source of truth for app settings,
so different parts of the app can rely on the same values.
"""

import unittest
from code_pattern.creational_pattern.singleton_pattern.singleton_code.application_configuration_manager import (ApplicationConfigManager)


class TestApplicationConfigManager(unittest.TestCase):
    """Tests for the shared configuration manager."""

    def test_singleton_instance(self):
        """Confirm the configuration manager is only created once."""
        first_config = ApplicationConfigManager()
        second_config = ApplicationConfigManager()

        # Both requests should return the same shared object.
        self.assertIs(first_config, second_config)

    def test_config_loaded(self):
        """Confirm the configuration values are available."""
        config = ApplicationConfigManager()

        # The shared configuration object should provide each setting.
        self.assertIsNotNone(config.get_environment())
        self.assertIsNotNone(config.get_database_url())
        self.assertIsNotNone(config.get_kafka_broker())


if __name__ == "__main__":
    unittest.main()