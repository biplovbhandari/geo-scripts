import argparse
import rasterio
from rasterio.merge import merge
from pathlib import Path


def merge_tiles(input_dir, output_file):
    """
    Merge all TIFF files in a directory into a single TIFF file.

    Parameters:
    - input_dir: Directory containing the TIFF files/tiles to merge.
    - output_file: Path to save the merged TIFF file.
    """
    # Path to the directory where your TIFF files are stored
    input_dir = Path(input_dir)
    output_file = Path(output_file)

    # Find all TIFF files in the directory
    tiff_files = list(input_dir.glob("*.tif"))

    # Open the TIFF files
    src_files_to_mosaic = []
    for fp in tiff_files:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)

    # Merge the TIFF files
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Copy the metadata
    out_meta = src.meta.copy()

    # Update the metadata
    out_meta.update({"driver": "GTiff",
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_trans,
                    "crs": src.crs,
                    "compress": "lzw",
                    })

    # Write the mosaic raster to disk
    with rasterio.open(output_file, "w", **out_meta, compress="lzw") as dest:
        dest.write(mosaic)

    # Close the source files
    for src in src_files_to_mosaic:
        src.close()

    print(f"Merged TIFF saved as {output_file}")
    return output_file

if __name__ == '__main__':

    # Create argument parser
    parser = argparse.ArgumentParser(description="Tile Raster Images.")
    # Input folder arguments
    parser.add_argument("-i", "--input_folder", "--i", required=True, help="Folder containing the raster tiles.", dest="input_folder")
    # Output folder arguments
    parser.add_argument("-o", "--output_file", "--o", required=True, help="File where the output will be saved.", dest="output_folder")

    # Parse arguments
    args = parser.parse_args()

    # Call the tile_raster function with arguments
    merge_tiles(args.input_folder, args.output_folder)
