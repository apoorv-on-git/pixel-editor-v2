def test_contributor_login(admin_requests):
    json = dict(
                    email = "contributor@pixelmath.org",
                    password = "123456"
            )
    resp = admin_requests.post('/admin-api/login', json=json)
    assert resp.status_code == 400

def test_admin_login(admin_requests):
    json = dict(
                    email = "admin@pixelmath.org",
                    password = "123456"
            )
    resp = admin_requests.post('/admin-api/login', json=json)
    assert resp.status_code == 200

def test_graphics_login(admin_requests):
    json = dict(
                    email = "graphics@pixelmath.org",
                    password = "123456"
            )
    resp = admin_requests.post('/admin-api/login', json=json)
    assert resp.status_code == 400

def test_super_admin_login(admin_requests):
    json = dict(
                    email = "super_admin@pixelmath.org",
                    password = "123456"
            )
    resp = admin_requests.post('/admin-api/login', json=json)
    assert resp.status_code == 400

def test_admin_login_wrong_email(admin_requests):
    json = dict(
                        email = "admin@gmail.com",
                        password = "123456"
        )
    resp = admin_requests.post("/admin-api/login", json=json)
    assert resp.status_code == 400

def test_admin_login_wrong_password(admin_requests):
    json = dict(
                        email = "admin@pixelmath.com",
                        password = "12345678"
        )
    resp = admin_requests.post("/admin-api/login", json=json)
    assert resp.status_code == 400

def test_admin_login_no_email(admin_requests):
    json = dict(
                        password = "123456"
        )
    resp = admin_requests.post("/admin-api/login", json=json)
    assert resp.status_code == 400

def test_admin_login_no_password(admin_requests):
    json = dict(
                        email = "admin@gmail.com"
        )
    resp = admin_requests.post("/admin-api/login", json=json)
    assert resp.status_code == 400