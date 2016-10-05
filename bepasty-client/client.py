#!/usr/bin/env python3
import click


@click.group()
def main():
    pass


@main.command()
@click.argument('path', nargs=1, required=False, type=click.File('rb'))
@click.option('--password', '-p', help='Your access token', required=True)
@click.option('--url', '-u', help='The server\'s base URL', required=True)
@click.option('--name', '-n', help='The paste\'s name')
@click.option('--type', '-t', help='The paste\' content type')
@click.option('--insecure', '-i', help='Disable certificate checks', is_flag=True)
def upload(path, password, url, name, _type, insecure):
    pass


@main.command()
@click.option('--password', '-p', help='Your access token', required=True)
@click.option('--url', '-u', help='The server\'s base URL', required=True)
@click.option('--insecure', '-i', help='Disable certificate checks', is_flag=True)
def list(password, url, insecure):
    click.echo('Name'.ljust(20) + '│ ', nl=False)
    click.echo('Type'.ljust(19) + '│', nl=False)
    click.echo('Size'.rjust(10) + ' │ ', nl=False)
    click.echo('Date'.ljust(20) + '│ ', nl=False)
    click.echo('URL')
    click.echo('─' * 100)


if __name__ == '__main__':
    main()
