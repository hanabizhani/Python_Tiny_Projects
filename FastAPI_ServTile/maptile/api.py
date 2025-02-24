"""
Developer: Hana Bizhani
Date: 2025-02-22
Change Log:
- Initial creation of the file.
- Refactored to reduce redundancy and improve readability.
"""

from fastapi import APIRouter, HTTPException, Response
import pymbtiles
# import json
# from mapbox_vector_tile import encode
# import sqlite3

router = APIRouter()

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
        print("test")
        tile_data = src.read_tile(zoom, column, row)
        if tile_data is None:
            raise HTTPException(status_code=404, detail="Tile data not found")
        return tile_data

# @router.post('/serv/<int:zoom>/<int:column>/<int:row>.pbf', response_class=Response)
# def serve_tile(zoom: int, column: int, row: int) -> Response:
#     """
#     Serve a vector tile in Protocol Buffers (PBF) format from the 'netsanj.mbtiles' file.

#     Parameters:
#     - zoom: Zoom level of the tile.
#     - column: Column (x-coordinate) of the tile.
#     - row: Row (y-coordinate) of the tile.

#     Returns:
#     - Binary tile data in PBF format.
#     - HTTP 404 if the tile is not found.
#     """
#     column, row = xyz_to_tms(zoom, column, row)
#     print(column)
#     print(row)
#     tile_data = read_tile_from_mbtiles("data/shp_joined.mbtiles", zoom, column, row)
#     # tile_data = read_tile_from_mbtiles("mbtiles/tiles.mbtiles", zoom, column, row)
#     return Response(content=tile_data, media_type='application/x-protobuf', headers=TILE_RESPONSE_HEADERS)

# @router.post("/")
# def root():
#     return {"message": "Hello World"}

# @router.post('/ecno/<int:zoom>/<int:column>/<int:row>.pbf', response_class=Response)
# def ecno_tile(zoom: int, column: int, row: int) -> Response:
    """
    Serve a vector tile in Protocol Buffers (PBF) format from the 'output (2).mbtiles' file.

    Parameters:
    - zoom: Zoom level of the tile.
    - column: Column (x-coordinate) of the tile.
    - row: Row (y-coordinate) of the tile.

    Returns:
    - Binary tile data in PBF format.
    - HTTP 404 if the tile is not found.
    """
    column, row = xyz_to_tms(zoom, column, row)
    tile_data = read_tile_from_mbtiles("data/ecno_tile.mbtiles", zoom, column, row)
    return Response(content=tile_data, media_type='application/x-protobuf', headers=TILE_RESPONSE_HEADERS)

# @router.post('/converGeoJsonToMbtile')
# def converGeoJsonToMbtile():
#     # Load GeoJSON
#     with open("roads/roads.geojson", "r") as f:
#         geojson = json.load(f)
#
#     # Convert to vector tiles
#     tiles = encode(geojson)
#
#     # Save to MBTiles
#     with MBTiles("mbtiles", "w") as mbtiles:
#         for tile in tiles:
#             mbtiles.write_tile(tile["z"], tile["x"], tile["y"], tile["data"])
#
#     return "SUCCESS"