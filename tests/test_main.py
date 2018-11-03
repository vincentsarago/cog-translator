"""tests cog_translator handler."""

import os

from click.testing import CliRunner

import rasterio
from cog_translator import _translate, _get_overview_level

raster_path_rgb = os.path.join(os.path.dirname(__file__), "fixtures", "image_rgb.tif")


def test_translate_valid():
    """Should work as expected (create cogeo file)."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        _translate(raster_path_rgb, "cogeo.tif", "ycbcr")
        with rasterio.open("cogeo.tif") as src:
            assert src.height == 512
            assert src.width == 512
            assert src.meta["dtype"] == "uint8"
            assert (
                not src.is_tiled
            )  # Because blocksize is 512 and the file is 512, the output is not tiled
            assert src.compression.value == "JPEG"
            assert src.photometric.value == "YCbCr"
            assert src.interleaving.value == "PIXEL"
            # File is too small to have overviews
            assert not src.overviews(1)
            assert src.tags()["OVR_RESAMPLING_ALG"] == "BILINEAR"


def test_ovrlevel_valid():
    """Should work as expected (find overview level)."""
    assert _get_overview_level(raster_path_rgb, 128) == 2
