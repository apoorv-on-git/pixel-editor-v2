def test_contributor_login(graphics_requests):
    json = dict(
                    email = "contributor@pixelmath.org",
                    password = "123456"
            )
    resp = graphics_requests.post('/graphics-api/login', json=json)
    assert resp.status_code == 400

def test_admin_login(graphics_requests):
    json = dict(
                    email = "admin@pixelmath.org",
                    password = "123456"
            )
    resp = graphics_requests.post('/graphics-api/login', json=json)
    assert resp.status_code == 400

def test_graphics_login(graphics_requests):
    json = dict(
                    email = "graphics@pixelmath.org",
                    password = "123456"
            )
    resp = graphics_requests.post('/graphics-api/login', json=json)
    assert resp.status_code == 200

def test_super_admin_login(graphics_requests):
    json = dict(
                    email = "super_admin@pixelmath.org",
                    password = "123456"
            )
    resp = graphics_requests.post('/graphics-api/login', json=json)
    assert resp.status_code == 400

def test_graphics_login_wrong_email(graphics_requests):
    json = dict(
                        email = "graphics@gmail.com",
                        password = "123456"
        )
    resp = graphics_requests.post("/graphics-api/login", json=json)
    assert resp.status_code == 400

def test_graphics_login_wrong_password(graphics_requests):
    json = dict(
                        email = "graphics@pixelmath.com",
                        password = "12345678"
        )
    resp = graphics_requests.post("/graphics-api/login", json=json)
    assert resp.status_code == 400

def test_graphics_login_no_email(graphics_requests):
    json = dict(
                        password = "123456"
        )
    resp = graphics_requests.post("/graphics-api/login", json=json)
    assert resp.status_code == 400

def test_graphics_login_no_password(graphics_requests):
    json = dict(
                        email = "graphics@gmail.com"
        )
    resp = graphics_requests.post("/graphics-api/login", json=json)
    assert resp.status_code == 400