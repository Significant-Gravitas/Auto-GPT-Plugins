import requests


def get_num_astronauts():
    """Get the number of astronauts in space.

    Args:
        None

    Returns:
        int: The number of astronauts in space.
    """
    response = requests.get("http://api.open-notify.org/astros.json")#Get the data
    data = response.json()#Convert it to JSON
    return data["number"]#Extract the number and return it
