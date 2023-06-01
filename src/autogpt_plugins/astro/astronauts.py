import requests


def get_num_astronauts():
    """Get the number of astronauts in space.

    Args:
        None

    Returns:
        int: The number of astronauts in space.
    """
    #Get the data
    response = requests.get("http://api.open-notify.org/astros.json")
    #Convert it to JSON
    data = response.json()
    #Extract the number and return it
    return data["number"]
