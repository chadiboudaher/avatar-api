from models import CharacterOut
from fake_db import fake_database

for char in fake_database:
    validated = CharacterOut(**char)
    print(validated)