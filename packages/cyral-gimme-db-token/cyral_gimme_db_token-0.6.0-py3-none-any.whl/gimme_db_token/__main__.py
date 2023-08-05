import logging
import sys

import click

from ._aws import (configure_s3_proxy_settings, s3_proxy_is_configured,
                   update_aws_creds)
from ._client import (browser_authenticate, decrypt_msg,
                      poll_opaque_token_service)
from ._crypto import generate_keys
from ._pgpass import update_pgpass

logger = logging.getLogger("gimme_db_token")
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - - %(funcName)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)


@click.command(name="gimme_db_token")
@click.argument("db", type=click.Choice(["pg", "s3"], case_sensitive=False), nargs=-1)
@click.option(
    "--address",
    required=False,
    envvar="CYRAL_ADDRESS",
    show_envvar=True,
    help="Address (FQDN) of Cyral controlplane. Example: acme.cyral.com.",
)
@click.option(
    "--tenant",
    required=False,
    envvar="CYRAL_TENANT",
    show_envvar=True,
    help="Tenant Name. If given, the controlplane address will be assumed to be <tenant>.cyral.com",
)
@click.option(
    "--sidecar",
    required=False,
    envvar="CYRAL_SIDECAR",
    show_envvar=True,
    help="(Required only for S3) Sidecar address. Required to autoconfigure S3 proxy settings.",
)
@click.option(
    "--autoconfigure/--no-autoconfigure",
    required=False,
    default=None,
    help="(Required only for S3) Enable/Disable S3 proxy settings autoconfiguration and prompts. If omitted, user input will be required if S3 proxy is misconfigured.",
)
@click.option(
    "--profile",
    help="(Required only for S3) Name of AWS profile to store S3 access credentials in. NOTE: any existing credentials in this profile will be overwritten. If no AWS profile with the provided name exists, it will be created.",
)
@click.option(
    "--stdout",
    help="Print the access token to stdout. The token will not be stored in the specified credential files.",
    is_flag=True,
)
@click.option("--silent", help="Run the program quietly.", is_flag=True)
@click.option(
    "--idp",
    required=False,
    envvar="CYRAL_IDP",
    show_envvar=True,
    help="If not logged in, you will be redirected to the IdP with this ID.",
)
@click.option(
    "--timeout",
    default=5 * 60,
    envvar="CYRAL_DB_TOKEN_TIMEOUT",
    type=click.INT,
    show_envvar=True,
    help="Number of seconds to wait for Cyral server to respond before timeout",
)
@click.option("-v", "--verbose", is_flag=True)
@click.version_option(version="0.6.0")
def update_token(
    db,
    address,
    tenant,
    sidecar,
    autoconfigure,
    profile,
    stdout,
    silent,
    idp,
    timeout,
    verbose,
):
    """Fetch a fresh database access token from Cyral and store it locally.
    Currently, gimme_db_token supports Postgresql and S3 (with more coming!).
    If a database type is not specified, Postgresql database type is used.

    Example usage:

        This command will fetch a database access token for Postgresql and store it in your system.

        > gimme_db_token pg --address mycompany.cyral.com

        This is equivalent to:

        > gimme_db_token pg --tenant mycompany

        You can also specify multiple database types:

        > gimme_db_token pg s3 --address mycompany.cyral.com --profile myprofile

        To store database access token in an environment variable with one command, run the following:

        > export CYRAL_TOKEN=$(gimme_db_token --address mycompany.cyral.com --stdout --silent)

        To autoconfigure S3 proxy settings:

        > gimme_db_token s3 --autoconfigure --address mycompany.cyral.com --profile myprofile --sidecar sidecar.address

        To silence S3 proxy misconfiguration prompts:

        > gimme_db_token s3 --no-autoconfigure --address mycompany.cyral.com --profile myprofile

    """
    # for backwards compatibility, if DB type is not set, use Postgresql
    db = db or ("pg",)
    check_common_args(tenant, address)
    address = address or f"{tenant}.cyral.com"
    if "s3" in db:
        check_s3_args(profile)
        check_and_configure_s3_proxy_settings(
            autoconfigure, profile, sidecar, address, silent
        )
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("/* IN DEBUG MODE */")
    try:
        private_key, public_key = generate_keys()
        browser_authenticate(address, public_key, silent, idp=idp)
        msg = poll_opaque_token_service(address, public_key, timeout)
        decrypt_msg(msg, private_key)
        # note: despite the field name, this access token is not encrypted anymore.
        # it was decrypted by the above line
        access_token = msg["EncryptedAccessToken"]
        if stdout:
            print(access_token)
        else:
            if "pg" in db:
                update_pgpass(access_token, msg.get("SidecarEndpoints"), silent)
            if "s3" in db:
                update_aws_creds(access_token, msg.get("UserEmail"), profile, silent)

    except Exception as e:
        print(
            "There was an error fetching your token. If this persists, please run the tool with the -v flag and contact support@cyral.com with the output. We’d be happy to help!"
        )
        if verbose:
            raise e


def check_common_args(tenant, address):
    if not (bool(tenant) ^ bool(address)):
        print(
            "Please provide either a Cyral controlplane address via --address or a tenant name via --tenant."
        )
        sys.exit(1)


def check_s3_args(profile):
    if not profile:
        print("Please provide an AWS profile name to use via --profile")
        sys.exit(1)


def check_s3_proxy_config_args(sidecar):
    if not sidecar:
        print(
            "Please provide a Cyral sidecar address to configure S3 proxy settings via --sidecar."
        )
        sys.exit(1)


def check_and_configure_s3_proxy_settings(
    autoconfigure, profile, sidecar, address, silent
):
    if autoconfigure is not False and not s3_proxy_is_configured(profile):
        # Notice that autoconfigure can be None or True at this point
        if autoconfigure is None:
            user_input = input(
                "S3 proxy settings are not correctly configured to work with Cyral. "
                "Proceed with the configuration first? [y/n] "
            )
        if autoconfigure or str(user_input) == "y":
            check_s3_proxy_config_args(sidecar)
            configure_s3_proxy_settings(profile, sidecar, address)
            if not silent:
                print("Successfully configured S3 proxy settings.")


def run():
    update_token(prog_name="gimme_db_token")


if __name__ == "__main__":
    run()
