def add_superhero(superheroes: list, name: str, power: str) -> None:
    """Adds a new superhero to the list."""
    # Issue: No error handling for duplicate names or empty input
    superheroes.append({'name': name, 'power': power})

def get_superhero_by_name(superheroes: list, name: str):
    """Returns a superhero dict by name."""
    # Issue: No type hints for return, no error handling if not found
    for hero in superheroes:
        if hero['name'] == name:
            return hero
    # Issue: Should raise an exception or return a clear value if not found
    return None

def update_superhero_power(superheroes: list, name: str, new_power: str):
    """Updates the power of a superhero."""
    # Issue: No error handling if superhero not found
    for hero in superheroes:
        if hero['name'] == name:
            hero['power'] = new_power
            return
    # Issue: No feedback if update fails

def delete_superhero(superheroes: list, name: str) -> bool:
    """Deletes a superhero by name."""
    # Issue: Modifies list during iteration, may cause bugs
    for hero in superheroes:
        if hero['name'] == name:
            superheroes.remove(hero)
            return True
    return False

def list_superheroes(superheroes: list) -> list:
    """Returns a list of superhero names."""
    # Issue: No type hints for superheroes parameter, missing docstring details
    return [hero['name'] for hero in superheroes]
