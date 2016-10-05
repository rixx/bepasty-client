#!/usr/bin/env python3
from datetime import datetime
import json
from urllib.parse import urljoin

import click
import magic

from helpers import handle_request


@click.group()
def main():
    pass


@main.command()
@click.argument('path', nargs=1, required=False, type=click.File('rb'))
@click.option('--password', '-p', help='Your access token', required=True)
@click.option('--url', '-u', help='The server\'s base URL', required=True)
@click.option('--name', '-n', help='The paste\'s name')
@click.option('--type', '-t', '_type', help='The paste\' content type')
@click.option('--insecure', '-i', help='No certificate checks', is_flag=True)
def upload(path, password, url, name, _type, insecure):
    chunk_size = 1024 * 1024
    stream = path or click.get_binary_stream('stdin')

    if path and not name:
        name = path.name

    first_chunk = stream.read(chunk_size)
    if not _type:
        _type = magic.Magic(mime=True).from_buffer(first_chunk) or 'text/plain'
        click.echo(f'Uploading with filetype {_type}.')


@main.command()
@click.option('--password', '-p', help='Your access token', required=True)
@click.option('--url', '-u', help='The server\'s base URL', required=True)
@click.option('--insecure', '-i', help='No certificate checks', is_flag=True)
def list(password, url, insecure):
    response = handle_request(
        method='get',
        url=urljoin(url, '/apis/rest/items'),
        auth=('user', password),
        verify=not insecure,
    )
    click.echo('Name'.ljust(20) + '│ ', nl=False)
    click.echo('Type'.ljust(19) + '│', nl=False)
    click.echo('Size'.rjust(10) + ' │ ', nl=False)
    click.echo('Date'.ljust(20) + '│ ', nl=False)
    click.echo('URL')
    click.echo('─' * 100)

    for key, paste in json.loads(response.content).items():
        meta = paste['file-meta']
        name = meta['filename']
        name = name[:18] + '…' if len(name) > 19 else name
        created = datetime.fromtimestamp(meta['timestamp-upload']).isoformat()

        click.echo(name.ljust(20) + '│ ', nl=False)
        click.echo(meta['type'][:19].ljust(19) + '│ ', nl=False)
        click.echo(str(meta['size'])[:9].rjust(9) + ' │ ', nl=False)
        click.echo(created.ljust(20) + '│ ', nl=False)
        click.echo(urljoin(url, key))


if __name__ == '__main__':
    main()
