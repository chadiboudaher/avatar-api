# Avatar API

## 1. Design data

This project will contain one model.
`Character`: The fields needed for this model are:

- id: integer
- name: string
- bio: string | Optional
- nation: string ("earth", "fire", "water", "air")
- is_bender: boolean
- show: string (ATLA, TLOK)
- first_appearance: string | Optional

## 2. Create schemas using pydantic library

Three basic schemas are created as a basis for the avatar api.

- `CharacterBase` - Base model
- `CharacterCreate` - Inherit from base, used for POST request bodies (no id).
- `CharacterOut` - Inherit from base, adds `id`. it is used for **responses**.

## 3. Create fake dataset

Fake dataset is created as a first step into created a simple api before moving on into real database using `sqlalchemy`.

All information is collected for `Avatar Wiki` website.

### Notes

1. `first_appearance`: This field should contain a proper string pattern.

### 3.1 Test fake database

create a `test_characters.py` file to test the validity of the fake database.

## 4. The importance of `model_response`

model_response is very important because it doesn't just describe the shape, it **filter** what you return to match that shape.

## 5. CRUD Operations

`GET`, `POST`, `PUT`, `DELETE` are the most simple operations in any API.
