#!/usr/bin/env python3.6
import base64
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
    raw_data = stream.read(chunk_size)
    total_size = 0
    transaction_id = ''

    if path and not name:
        name = path.name

    if not _type:
        _type = magic.Magic(mime=True).from_buffer(raw_data) or 'text/plain'
        click.echo(f'Uploading with filetype {_type}.')

    while raw_data:
        raw_data_size = len(raw_data)
        previous_total = total_size
        total_size += raw_data_size + int(raw_data_size >= chunk_size)

        data = base64.b64encode(raw_data)
        r = f'bytes {previous_total}-{total_size - 1}/{total_size}'
        headers = {
            'Content-Type': _type,
            'Content-Length': str(len(data)),
            'Content-Range': r,
        }
        if name:
            headers['Content-Filename'] = name
        if transaction_id:
            headers['Transaction-Id'] = transaction_id

        response = handle_request(
            method='post',
            url=urljoin(url, '/apis/rest/items'),
            headers=headers,
            data=data,
            auth=('user', password),
            verify=not insecure,
        )
        if not response:
            break

        if response.status_code == 201:
            location = response.headers['Content-Location']
            click.echo(urljoin(url, location.split('/')[-1]))
            break

        transaction_id = response.headers['Transaction-Id']
        raw_data = stream.read(chunk_size)


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
        name = meta.get('filename')
        if not name:
            click.echo(f'File {key} is broken (empty metadata)', nl=False, err=True)
            click.echo(' - Please delete this file server-side!', err=True)
            continue

        name = name[:18] + '…' if len(name) > 19 else name
        created = datetime.fromtimestamp(meta['timestamp-upload']).isoformat()

        click.echo(name.ljust(20) + '│ ', nl=False)
        click.echo(meta['type'][:19].ljust(19) + '│ ', nl=False)
        click.echo(str(meta['size'])[:9].rjust(9) + ' │ ', nl=False)
        click.echo(created.ljust(20) + '│ ', nl=False)
        click.echo(urljoin(url, key))


if __name__ == '__main__':
    main()
