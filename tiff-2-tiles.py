import argparse
import rasterio
from rasterio import windows
import numpy as np
from itertools import product
from pathlib import Path


def get_tiles(ds, width=512, height=512):
    """
    Generate windows for tiling an image.

    Parameters:
    - ds: Dataset opened with rasterio.
    - width, height: Tile size.
    """
    ncols, nrows = ds.meta["width"], ds.meta["height"]
    offsets = product(range(0, ncols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=ncols, height=nrows)
    for col_off, row_off in offsets:
        window = windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform


def tile_raster(input_folder, output_folder, tile_size=(512, 512)):
    """
    Tile raster files in a folder and save the tiles with metadata.

    Parameters:
    - input_folder: Folder containing the raster files to tile.
    - output_folder: Folder where the tiles will be saved.
    - tile_size: Tuple of (width, height) for the tile size.
    """
    input_folder_path = Path(input_folder)
    output_folder_path = Path(output_folder)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for filepath in input_folder_path.glob("*.tif"):
        print(f"Processing {filepath}")

        output_folder = output_folder_path / filepath.stem / f"{tile_size[0]}x{tile_size[1]}"
        output_folder.mkdir(parents=True, exist_ok=True)

        print(f"Saving tiles to folder: {output_folder}")

        with rasterio.open(filepath) as src:
            for window, transform in get_tiles(src, width=tile_size[0], height=tile_size[1]):
                # Use the window to read a tile from the source raster
                tile = src.read(window=window)

                # Skip empty tiles
                if np.all(tile == 0):
                    continue

                # Define metadata for the new tile
                meta = src.meta.copy()
                meta.update({
                    "driver": "GTiff",
                    "height": window.height,
                    "width": window.width,
                    "transform": transform
                })

                output_filename = f"{filepath.stem}_tile_{int(window.col_off)}_{int(window.row_off)}.tif"
                with rasterio.open(output_folder / output_filename, "w", **meta) as dest:
                    dest.write(tile)


if __name__ == '__main__':

    # Create argument parser
    parser = argparse.ArgumentParser(description="Tile Raster Images.")
    # Input folder arguments
    parser.add_argument("-i", "--input_folder", "--i", required=True, help="Folder containing the raster files to tile.", dest="input_folder")
    # Output folder arguments
    parser.add_argument("-o", "--output_folder", "--o", required=True, help="Folder where the tiles will be saved.", dest="output_folder")
    # Tile size argument
    parser.add_argument("-t", "--tile_size", "--t", type=int, default=512, help="Tile size as a single integer for both width and height.", dest="tile_size")

    # Parse arguments
    args = parser.parse_args()

    # Convert tile_size to a tuple before passing
    tile_size = (args.tile_size, args.tile_size)

    # Call the tile_raster function with arguments
    tile_raster(args.input_folder, args.output_folder, tile_size)
