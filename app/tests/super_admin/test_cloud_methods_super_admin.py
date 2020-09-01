from app.db_controllers.super_admin_controller import *

def test_get_user_document_valid():
    super_admin_data = get_user_document_data("super_admin")
    if super_admin_data:
        assert True
    else:
        assert False

def test_get_user_document_invalid():
    super_admin_data = get_user_document_data("super_admin_invalid")
    if super_admin_data:
        assert False
    else:
        assert True