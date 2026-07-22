# Avatar API

# Phase 1 - fake List database

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

# Phase 2 - Swapping fake list for a real SQLite database

## 1. Create `database.py`

- Setup connection to the database using `create_engine` function.
- Add `check_same_thread` argument and set it to **False** to use the same SQLite database in different threads. This is necessary as one single request could use more than one thread (for example dependencies) [FastAPI Docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-an-engine).

## 2. Create SessionLocal

- `autoflush=False`: Prevents the database from saving changes automatically after every single operation. Instead, the session waits for you to explicitly call `db.commit()`. If something goes wrong, you can run `db.rollback()` to undo uncommitted actions.
- `autocommit=False`: Prevents the session from automatically pushing pending changes to the database before runnning a read query.
- `bind=engine`: Connects the `SessionLocal` class to the database configuration.

## 3. Create Endpoint

In this step, CRUD operations are implemented with connection to the database, and tested using `Swagger UI`.

Some Notes:

- `.filter()`: is used to check a condition, `.first()` is added to provide a **None** option that can be used to raise exception.
- When creating a new character, `.add()` is used to add to the database, and `.refresh()` is used to fetch the current state like (id, etc.).

# Phase 3 - Relationships & Query Power

## 1. Promote `Nation` to a real table

Instead of a fixed enum, `Nation` becomes its own table (`id`, `name`), and `Character` gets a `nation_id` foreign key pointing to it.

- `ForeignKey("nations.id")`: creates the actual DB-level link.
- `relationship()`: the ORM-level convenience — lets you write `character.nation.name` instead of manually looking up the id.
- `back_populates`: keeps both sides in sync — the string passed must match the _attribute name_ on the other class (`Character.nation` ↔ `back_populates="characters"`, `Nation.characters` ↔ `back_populates="nation"`).

### Notes

1. Changing the schema this drastically breaks the existing SQLite file (`create_all()` only creates _new_ tables, it never alters existing ones). Fix for a learning project: delete `avatar.db` and let it regenerate. In production this is solved properly with **Alembic** migrations (Phase 8).
2. `Show` stayed as a plain enum — only 2 fixed values, no real one-to-many relationship to model.

## 2. Nested responses

`CharacterOut` no longer inherits cleanly from `CharacterBase`, since `nation` differs in shape between create (`nation_id: int`) and read (`nation: NationOut`, a nested object). Pydantic matches schema field names to object attribute names one-to-one — so the field must be named `nation` (not `nation_id`) to correctly read the SQLAlchemy relationship.

## 3. Query power on `GET /characters`

- Filtering: `?nation=fire`, `?is_bender=true` — filter through a joined table using `.join(Nation).filter(Nation.name == nation)`.
- Search: `?name=zu` — partial, case-insensitive match using `.ilike(f"%{name}%")`.
- Pagination: `?skip=0&limit=10` — `.offset(skip).limit(limit)`, always applied **last**, after all filters.

# Phase 4 - Proper error handling

## 1. Field-level validation

`Field(min_length=1, max_length=100)` on Pydantic schemas closes gaps that a plain `str` type hint allows through (like an empty name).

## 2. Foreign key existence checks

Pydantic can't validate that a `nation_id` actually exists in the database — that requires a manual query before creating/updating a `Character`, same pattern as the existing uniqueness check.

## 3. Create custom exception handler

A global handler catches anything that slips through all your specific `HTTPException`s and turns it into a clean, generic response.

# Phase 5 - Auth & Users

## 1. `User` model

Stores `username` and `hashed_password` only — never a raw password field.

## 2. Password hashing

`passlib` (`bcrypt` scheme) for `hash_password()` / `verify_password()`. Hashing is one-way — passwords are never stored or retrieved in plain text.

### Notes

1. Known compatibility bug: newer `bcrypt` versions raise instead of truncating on passlib's internal self-test. Fix: pin `bcrypt==4.0.1`.

## 3. JWT tokens

Used `pyjwt` (not `python-jose` — the FastAPI docs moved away from it since it's unmaintained). `create_access_token()` signs a payload (`{"sub": username}`) with a `SECRET_KEY` and expiry.

## 4. Login endpoint

Uses `OAuth2PasswordRequestForm` (form data, not JSON). Same generic error/status code (`401`) whether the username doesn't exist or the password is wrong — prevents leaking which usernames are registered.

## 5. Protecting routes

`get_current_user` dependency: decodes the token (`jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])` — note the plural `algorithms`), looks up the user, raises `401` if anything's invalid. Added as `Depends(get_current_user)` to every `/characters` route.

# Phase 6 - Project structure

## 1. Routers

Split routes into `routers/characters.py`, `routers/nations.py`, `routers/auth.py`, each with its own `APIRouter(prefix=..., tags=[...])`. `main.py` shrinks down to app setup + `include_router()` calls.

### Notes

1. Router `prefix` + route path combine — a route defined as `""` under `prefix="/characters"` becomes `/characters`; a route defined as `"/"` becomes `/characters/` (different path, watch for 404s from mismatched trailing slashes).

## 2. Config via `.env`

`pydantic-settings` + `SettingsConfigDict(env_file=".env")` moves `SECRET_KEY` out of hardcoded source code. `.env` added to `.gitignore` — secrets never get committed.

# Phase 7 - Testing

## 1. Isolated test database

Real database is never touched by tests. `app.dependency_overrides[get_db] = override_get_db` swaps in a separate test DB session for the whole test run.

## 2. Fixtures for per-test isolation

```python
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

Runs fresh table creation before each test, drops everything after — no leftover state between tests, no manual file deletion needed.

## 3. Coverage

Tests cover: unauthenticated access (401), full register → login → protected-route flow, field validation failures (422), and 404s on nonexistent resources.
