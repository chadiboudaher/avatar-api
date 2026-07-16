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

# 2. Create schemas using pydantic library

Three basic schemas are created as a basis for the avatar api.

- `CharacterBase` - Base model
- `CharacterCreate` - Inherit from base, used for POST request bodies (no id).
- `CharacterOut` - Inherit from base, adds `id`. it is used for **responses**.
