from os import path
import pytest


def run_tests():
    test_directory = path.join(path.dirname(__file__), "src", "test")
    pytest.main(["-v", "-s", "--disable-warnings", test_directory])


if __name__ == "__main__":
    run_tests()
