import click
import requests


def handle_request(**kwargs):
    try:
        response = requests.request(**kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError:
        click.echo('Could not connect to server:\n', err=True)
    except requests.exceptions.Timeout:
        click.echo('Incurred request timeout.', err=True)
    except requests.exceptions.HTTPError:
        click.echo(f'The request failed with status {response.status_code}. Response:\n', err=True)
        click.echo(response.content, err=True)
