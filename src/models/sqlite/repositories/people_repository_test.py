from unittest import mock
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pets import PetsTable
from src.models.sqlite.entities.people import PeopleTable
from .people_repository import PeopleRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PeopleTable), mock.call.query(PetsTable)], # query
                    [
                        PeopleTable(id=1, first_name="Fulano", last_name="Silva", age=18, pet_id=3),
                        PeopleTable(id=2, first_name="Sicrano", last_name="Vieira", age=8, pet_id=4),
                        PetsTable(id=3, name='dog', type='dog'), PetsTable(id=4, name='cat', type='cat')
                    ] # resultado
                )
            ]
        )

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_value, exc_tb): pass

def test_insert_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    repo.insert_person(first_name="John", last_name="Doe", age=70, pet_id=80)

    mock_connection.session.rollback.assert_not_called()
    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_get_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    response = repo.get_person(1)
    print(response)
