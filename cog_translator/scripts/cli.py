"""Worker."""

import os
import json
import sys
import logging

from cog_translator import process


logger = logging.getLogger("cog_translator")
logger.setLevel(logging.INFO)


def main():
    """Load message and start process."""
    try:
        message = json.loads(os.environ["Message"])
        logger.info(f"Processing message {os.environ['Message']}")
        url = message["url"]
        bucket = message["bucket"]
        key = message["key"]

        options = {}
        if message.get("profile"):
            options["profile"] = message["profile"]
        if message.get("bidx"):
            options["bidx"] = message["bidx"]

        process(url, bucket, key, **options)

    except Exception as err:
        logger.error(err.message)
        sys.exit(3)

    else:
        logger.info(message)
        sys.exit(0)


if __name__ == "__main__":
    main()
