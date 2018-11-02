"""Lambda_pyskel.scripts.cli."""

import json

import click
from boto3.session import Session as boto3_session

from rio_cogeo.profiles import cog_profiles


class CustomType:
    """Click CustomType."""

    class BdxParamType(click.ParamType):
        """Band inddex type."""

        name = "bidx"

        def convert(self, value, param, ctx):
            """Validate and parse band index."""
            try:
                bands = [int(x) for x in value.split(",")]
                assert all(b > 0 for b in bands)
                return bands

            except (ValueError, AttributeError, AssertionError):
                raise click.ClickException(
                    "bidx must be a string of comma-separated integers (> 0), "
                    "representing the band indexes."
                )

    bidx = BdxParamType()


@click.command(short_help="Send message to a SNS topic")
@click.argument("url", type=str, nargs=1)
@click.option(
    "--profile",
    type=click.Choice(cog_profiles.keys()),
    default="ycbcr",
    help="CloudOptimized GeoTIFF profile (default: ycbcr)",
)
@click.option("--bidx", "-b", type=CustomType.bidx, help="Band index to copy")
@click.option(
    "--bucket",
    type=str,
    required=True,
    help="Output S3 bucket",
)
@click.option(
    "--key",
    type=str,
    required=True,
    help="Output S3 key",
)
@click.option(
    "--region",
    type=str,
    default="us-east-1",
    help="AWS region",
)
@click.option(
    "--topic",
    type=str,
    required=True,
    help="SNS Topic",
)
def main(url, profile, bidx, bucket, key, region, topic):
    """Send message."""
    session = boto3_session(region_name=region)
    sns = session.client("sns")

    message = dict(
        url=url,
        bucket=bucket,
        key=key,
        profile=profile,
    )

    if bidx:
        message["bidx"] = bidx

    response = sns.publish(TargetArn=topic, Message=json.dumps(message))
    return response["MessageId"]


if __name__ == "__main__":
    main()
