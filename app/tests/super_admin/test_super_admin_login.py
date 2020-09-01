def test_contributor_login(super_admin_requests):
    json = dict(
                    email = "contributor@pixelmath.org",
                    password = "123456"
            )
    resp = super_admin_requests.post('/super-admin-api/login', json=json)
    assert resp.status_code == 400

def test_admin_login(super_admin_requests):
    json = dict(
                    email = "admin@pixelmath.org",
                    password = "123456"
            )
    resp = super_admin_requests.post('/super-admin-api/login', json=json)
    assert resp.status_code == 400

def test_graphics_login(super_admin_requests):
    json = dict(
                    email = "graphics@pixelmath.org",
                    password = "123456"
            )
    resp = super_admin_requests.post('/super-admin-api/login', json=json)
    assert resp.status_code == 400

def test_super_admin_login(super_admin_requests):
    json = dict(
                    email = "super_admin@pixelmath.org",
                    password = "123456"
            )
    resp = super_admin_requests.post('/super-admin-api/login', json=json)
    assert resp.status_code == 200

def test_super_admin_login_wrong_email(super_admin_requests):
    json = dict(
                        email = "super_admin@gmail.com",
                        password = "123456"
        )
    resp = super_admin_requests.post("/super-admin-api/login", json=json)
    assert resp.status_code == 400

def test_super_admin_login_wrong_password(super_admin_requests):
    json = dict(
                        email = "super_admin@pixelmath.com",
                        password = "12345678"
        )
    resp = super_admin_requests.post("/super-admin-api/login", json=json)
    assert resp.status_code == 400

def test_super_admin_login_no_email(super_admin_requests):
    json = dict(
                        password = "123456"
        )
    resp = super_admin_requests.post("/super-admin-api/login", json=json)
    assert resp.status_code == 400

def test_super_admin_login_no_password(super_admin_requests):
    json = dict(
                        email = "super_admin@gmail.com"
        )
    resp = super_admin_requests.post("/super-admin-api/login", json=json)
    assert resp.status_code == 400