def test_contributor_login(contributor_requests):
    json = dict(
                    email = "contributor@pixelmath.org",
                    password = "123456"
            )
    resp = contributor_requests.post('/contributor-api/login', json=json)
    assert resp.status_code == 200

def test_admin_login(contributor_requests):
    json = dict(
                    email = "admin@pixelmath.org",
                    password = "123456"
            )
    resp = contributor_requests.post('/contributor-api/login', json=json)
    assert resp.status_code == 400

def test_graphics_login(contributor_requests):
    json = dict(
                    email = "graphics@pixelmath.org",
                    password = "123456"
            )
    resp = contributor_requests.post('/contributor-api/login', json=json)
    assert resp.status_code == 400

def test_super_admin_login(contributor_requests):
    json = dict(
                    email = "super_admin@pixelmath.org",
                    password = "123456"
            )
    resp = contributor_requests.post('/contributor-api/login', json=json)
    assert resp.status_code == 400

def test_contributor_login_wrong_email(contributor_requests):
    json = dict(
                        email = "contributor@gmail.com",
                        password = "123456"
        )
    resp = contributor_requests.post("/contributor-api/login", json=json)
    assert resp.status_code == 400

def test_contributor_login_wrong_password(contributor_requests):
    json = dict(
                        email = "contributor@pixelmath.com",
                        password = "12345678"
        )
    resp = contributor_requests.post("/contributor-api/login", json=json)
    assert resp.status_code == 400

def test_contributor_login_no_email(contributor_requests):
    json = dict(
                        password = "123456"
        )
    resp = contributor_requests.post("/contributor-api/login", json=json)
    assert resp.status_code == 400

def test_contributor_login_no_password(contributor_requests):
    json = dict(
                        email = "contributor@gmail.com"
        )
    resp = contributor_requests.post("/contributor-api/login", json=json)
    assert resp.status_code == 400