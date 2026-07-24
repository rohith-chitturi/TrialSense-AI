import os
import shutil
from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageProvider(ABC):
    @abstractmethod
    async def save(self, file: BinaryIO, path: str) -> str:
        """Save a file and return its storage URI/path."""
        pass

    @abstractmethod
    async def get(self, path: str) -> BinaryIO:
        """Retrieve a file by its path."""
        pass

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Delete a file by its path."""
        pass

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_dir: str = "uploads"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    async def save(self, file: BinaryIO, path: str) -> str:
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)
            
        return full_path

    async def get(self, path: str) -> BinaryIO:
        full_path = os.path.join(self.base_dir, path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File {full_path} not found.")
        return open(full_path, "rb")

    async def delete(self, path: str) -> bool:
        full_path = os.path.join(self.base_dir, path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

# In a real app, this would be injected via a dependency container
storage_provider: StorageProvider = LocalStorageProvider()
