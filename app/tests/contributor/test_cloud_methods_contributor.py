from app.db_controllers.contributor_controller import *

def test_get_user_document_valid():
    contributor_data = get_user_document_data("contributor")
    if contributor_data:
        assert True
    else:
        assert False

def test_get_user_document_invalid():
    contributor_data = get_user_document_data("contributor_invalid")
    if contributor_data:
        assert False
    else:
        assert True