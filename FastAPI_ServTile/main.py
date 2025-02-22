"""
Developer: Hana Bizhani
Date: 2025-02-22
Change Log:
- Initial creation of the file.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pathlib import Path
from maptile.api import router as tile_router


# Lifespan event handler
def check_file_exists(file_path: Path, file_description: str) -> None:
    """
    Check if a file exists at the specified path.

    Parameters:
    - file_path: Path to the file.
    - file_description: Description of the file for error messages.

    Raises:
    - FileNotFoundError: If the file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"{file_description} not found at {file_path}")
    print(f"{file_description} found at {file_path}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    """
    # Define file paths and their descriptions
    files_to_check = [
        (Path("data/netsanj.mbtiles"), "Netsanj MBTiles file"),
        (Path("data/ecno_tile.mbtiles"), "Ecno MBTiles file"),
    ]
    # Startup logic: Check if required files exist
    for file_path, file_description in files_to_check:
        check_file_exists(file_path, file_description)

    yield  # The application runs here
    # Shutdown logic (optional)
    print("Shutting down...")

app = FastAPI()
app.include_router(tile_router, prefix="/tile")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
