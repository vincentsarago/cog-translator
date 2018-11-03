"""Main."""

import os
from urllib.parse import urlparse

import wget

from boto3.session import Session as boto3_session

import rasterio
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")

__version__ = "1.0.0"


def _s3_download(path, key):
    session = boto3_session(region_name=REGION_NAME)
    s3 = session.client("s3")

    url_info = urlparse(path.strip())
    s3_bucket = url_info.netloc
    s3_key = url_info.path.strip("/")

    s3.download_file(s3_bucket, s3_key, key)
    return True


def _upload(path, bucket, key):
    session = boto3_session(region_name=REGION_NAME)
    s3 = session.client("s3")

    with open(path, 'rb') as data:
        s3.upload_fileobj(data, bucket, key)

    return True


def _get_overview_level(src_path, minsize):
    with rasterio.open(src_path) as src:
        width = src.width
        height = src.height
    nlevel = 0
    overview = 1
    while (min(width // overview, height // overview) > minsize):
        overview *= 2
        nlevel += 1
    return nlevel


def _translate(src_path, dst_path, profile="ycbcr", bidx=None):
    """Convert image to COG."""
    output_profile = cog_profiles.get(profile)
    output_profile.update(dict(BIGTIFF="IF_SAFER"))

    block_size = min(output_profile["blockxsize"], output_profile["blockysize"])

    config = dict(
        NUM_THREADS=4,
        GDAL_TIFF_INTERNAL_MASK=True,
        GDAL_TIFF_OVR_BLOCKSIZE=block_size,
    )

    ovr_level = _get_overview_level(src_path, block_size)
    cog_translate(
        src_path,
        dst_path,
        output_profile,
        bidx,
        None,
        None,
        ovr_level,
        "bilinear",
        config,
    )

    return dst_path


def process(url, s3_bucket, s3_key, profile="ycbcr", bidx=None):
    """Download, convert and upload."""
    url_info = urlparse(url.strip())
    src_path = "/tmp/" + os.path.basename(url_info.path)

    if url_info.scheme.startswith("http"):
        wget.download(url, src_path)
    elif url_info.scheme == "s3":
        _s3_download(url, src_path)
    else:
        raise Exception(f"Unsuported scheme {url_info.scheme}")

    bname = os.path.basename(src_path)
    ext = bname.split(".")[-1]
    dst_path = "/tmp/" + bname.replace(f".{ext}", f"_cog.tif")
    _translate(src_path, dst_path, profile=profile, bidx=bidx)
    _upload(dst_path, s3_bucket, s3_key)

    return True
