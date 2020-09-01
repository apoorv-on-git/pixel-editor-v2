from app.db_controllers.admin_controller import *

def test_get_user_document_valid():
    admin_data = get_user_document_data("admin")
    if admin_data:
        assert True
    else:
        assert False

def test_get_user_document_invalid():
    admin_data = get_user_document_data("admin_invalid")
    if admin_data:
        assert False
    else:
        assert True