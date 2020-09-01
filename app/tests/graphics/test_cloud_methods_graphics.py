from app.db_controllers.graphics_controller import *

def test_get_user_document_valid():
    graphics_data = get_user_document_data("graphics")
    if graphics_data:
        assert True
    else:
        assert False

def test_get_user_document_invalid():
    graphics_data = get_user_document_data("graphics_invalid")
    if graphics_data:
        assert False
    else:
        assert True