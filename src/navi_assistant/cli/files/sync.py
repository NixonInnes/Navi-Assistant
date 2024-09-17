# src/navi_assistant/cli/files/sync.py

import os

import click

from ... import ai
from ...navi import Navi
from ...style import art, messaging


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
def sync(use_global: bool = False):
    """Sync the store files with the assistant."""
    click.echo(art.styled_fairy + messaging.make_header("Files:Sync"))

    navi = Navi(use_global)

    client = ai.get_client()

    store_id = navi.config["store_id"]

    files = ai.get_store_files(navi.config["store_folders"], navi.config["store_file_extensions"])

    click.echo(messaging.make_info("Uploading files..."))
    for file in files:
        stat = os.stat(file)
        if file not in navi.cache["store_files"]:
            navi.cache["store_files"][file] = {"id": "", "uploaded": 0}
        
        if navi.cache["store_files"][file]["uploaded"] < stat.st_mtime:
            click.echo(messaging.make_info(f"  Uploading {file}"))
            store_file = ai.upload_file(client, store_id, file)
            navi.cache["store_files"][file] = {"id": store_file.id, "uploaded": stat.st_mtime}
        else:
            click.echo(messaging.make_info(f"  Skipping {file}"))
    click.echo(messaging.make_info("Upload complete."))

    # Remove any files that are in the store but not in files
    click.echo(messaging.make_info("Cleaning up old files..."))
    store_files_ids = [f.id for f in ai.list_store_files(client, store_id)]
    local_file_ids = [v["id"] for v in navi.cache["store_files"].values()]
    for file in store_files_ids:
        if file not in local_file_ids:
            click.echo(messaging.make_info(f"  Removing {file}"))
            ai.delete_file(client, store_id, file)
    click.echo(messaging.make_info("Cleanup complete."))
    
    navi.save_cache()
    click.echo(messaging.make_info("Sync complete."))