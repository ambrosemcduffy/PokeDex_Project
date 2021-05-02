"""Simple python wrapper around the public pokeapi rest api.

For the full documentation for the rest api please visit:
https://pokeapi.co/docs/v2
"""
import requests


def get_pokemon():
    """Gets data on the original 151 pokemon.

    Notes:
        The results are NOT sorted by their id
    Returns:
        list of dict
    """
    response = requests.get("http://pokeapi.co/api/v2/pokemon?limit=151", verify=False)
    json = response.json()
    return [data for data in json.get("results", [])]


def get_flavor_text(name):
    """Gets the flavor text for a pokemon.

    Args:
        name (str): name of the pokemon

    Returns:
        unicode
    """
    response = requests.get("http://pokeapi.co/api/v2/pokemon-species/{}".format(name), verify=False)
    json = response.json()
    return json.get("flavor_text_entries")[0]["flavor_text"]


def get_sprite_url(name):
    """Gets the url for the front sprite of the pokemon.

    Args:
        name (str): name of the pokemon

    Returns:
        unicode
    """
    response = requests.get("http://pokeapi.co/api/v2/pokemon/{}".format(name), verify=False)
    json = response.json()
    return json["sprites"]["front_default"]


