import os

__all__ = [x for x in os.listdir() if x.endswith(".py") and x != "__init__.py"]