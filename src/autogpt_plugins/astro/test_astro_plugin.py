from .astronauts import get_num_astronauts
from .astronauts import get_coords_iss

def test_astro():
    assert type(get_num_astronauts())==int

def test_iss():
    latitude, longitude = get_coords_iss()
    assert type(latitude)==float
    assert type(longitude)==float
