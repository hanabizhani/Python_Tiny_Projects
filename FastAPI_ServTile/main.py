"""
Developer: Hana Bizhani
Date: 2025-02-22
Change Log:
- Initial creation of the file.
"""
from contextlib import asynccontextmanager

from fastapi import APIRouter, HTTPException, Response, FastAPI
import pymbtiles
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from maptile.api import router as tile_router


# Lifespan event handler
# def check_file_exists(file_path: Path, file_description: str) -> None:
#     """
#     Check if a file exists at the specified path.
#
#     Parameters:
#     - file_path: Path to the file.
#     - file_description: Description of the file for error messages.
#
#     Raises:
#     - FileNotFoundError: If the file does not exist.
#     """
#     if not file_path.exists():
#         raise FileNotFoundError(f"{file_description} not found at {file_path}")
#     print(f"{file_description} found at {file_path}")
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan context manager to handle startup and shutdown events.
#     """
#     # Define file paths and their descriptions
#     files_to_check = [
#         (Path("data/netsanj.mbtiles"), "Netsanj MBTiles file"),
#         (Path("data/ecno_tile.mbtiles"), "Ecno MBTiles file"),
#     ]
#     # Startup logic: Check if required files exist
#     for file_path, file_description in files_to_check:
#         check_file_exists(file_path, file_description)
#
#     yield  # The application runs here
#     # Shutdown logic (optional)
#     print("Shutting down...")

app = FastAPI()
app.include_router(tile_router, prefix="/tile")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Common headers for tile responses
TILE_RESPONSE_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Connection': 'keep-alive',
    'Content-Encoding': 'gzip',
    'Content-Type': 'application/x-protobuf',
}

def xyz_to_tms(zoom: int, xtile: int, ytile_xyz: int) -> tuple[int, int]:
    """
    Convert XYZ tile coordinates to TMS tile coordinates.

    Parameters:
    - zoom: Zoom level of the tile.
    - xtile: X-coordinate (column) of the tile in XYZ format.
    - ytile_xyz: Y-coordinate (row) of the tile in XYZ format.

    Returns:
    - A tuple containing the TMS coordinates (xtile, ytile_tms).
    """
    n = 1 << zoom  # Equivalent to 2^zoom
    ytile_tms = (n - 1) - ytile_xyz
    return xtile, ytile_tms

def read_tile_from_mbtiles(mbtiles_path: str, zoom: int, column: int, row: int) -> bytes:
    """
    Read a tile from an MBTiles file.

    Parameters:
    - mbtiles_path: Path to the MBTiles file.
    - zoom: Zoom level of the tile.
    - column: Column (x-coordinate) of the tile.
    - row: Row (y-coordinate) of the tile.

    Returns:
    - Binary tile data in PBF format.

    Raises:
    - HTTPException: If the tile data is not found.
    """
    with pymbtiles.MBtiles(mbtiles_path) as src:
        print("test", zoom, column, row)
        tile_data = src.read_tile(zoom, column, row)
        if tile_data is None:
            raise HTTPException(status_code=404, detail="Tile data not found")
        return tile_data

@app.get('/serv/<int:zoom>/<int:column>/<int:row>.pbf', response_class=Response)
async def serve_tile(zoom: int, column: int, row: int) -> Response:
    """
    Serve a vector tile in Protocol Buffers (PBF) format from the 'data/roads.mbtiles' file.

    Parameters:
    - zoom: Zoom level of the tile.
    - column: Column (x-coordinate) of the tile.
    - row: Row (y-coordinate) of the tile.

    Returns:
    - Binary tile data in PBF format.
    - HTTP 404 if the tile is not found.
    """
    # column, row = xyz_to_tms(zoom, column, row)
    print(column)
    print(row)
    tile_data = read_tile_from_mbtiles("data/roads.mbtiles", zoom, column, row)
    # tile_data = read_tile_from_mbtiles("mbtiles/tiles.mbtiles", zoom, column, row)
    return Response(content=tile_data, media_type='application/x-protobuf', headers=TILE_RESPONSE_HEADERS)