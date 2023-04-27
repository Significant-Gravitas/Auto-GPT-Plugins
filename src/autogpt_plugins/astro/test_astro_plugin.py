from .astronauts import (
    get_num_astronauts
)

def test_astro():
    assert type(get_num_astronauts())==int