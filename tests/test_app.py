from app import app


def test_show_recipes_route():
    client = app.test_client()

    # Simulate a GET request to the show_recipes route
    response = client.get('/show_recipes')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66' 

    response_with_session = client.get('/show_recipes')
    assert response_with_session.status_code == 200


def test_search_recipes_route():
    client = app.test_client()

    # Simulate a POST request to the search_recipes route with a search query
    response = client.post('/search_recipes', data={'query': 'burger'})

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_about_route():
    client = app.test_client()

    # Simulate a GET request to the about route
    response = client.get('/about')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_sign_up_route_get():
    client = app.test_client()

    # Simulate a GET request to the sign_up route
    response = client.get('/sign_up')

    # Check if the response status code is 200 (OK) for the GET request
    assert response.status_code == 200


def test_sign_in_route_get():
    client = app.test_client()

    # Simulate a GET request to the sign_in route
    response = client.get('/sign_in')

    # Check if the response status code is 200 (OK) for the GET request
    assert response.status_code == 200

def test_profile_route_get():
    client = app.test_client()

    # Simulate a GET request to the profile route
    response = client.get('/profile')

    # Check if the response status code is 302 (redirect)
    assert response.status_code == 302


def test_edit_profile_route_get():
    client = app.test_client()

    # Simulate a GET request to the edit_profile route
    response = client.get('/edit_profile')

    # Check if the response status code is 302 (redirect)
    assert response.status_code == 302


def test_delete_profile_route():
    client = app.test_client()

    # Simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    # Simulate a GET request to the delete_profile route
    response_get = client.get('/delete_profile')

    # Check if the response status code is 200 (OK) for the GET request
    assert response_get.status_code == 200

    # Simulate a POST request to the delete_profile route
    response_post = client.post('/delete_profile')

    # Check if the response status code is 302 (Found/Redirect) for a successful profile deletion
    assert response_post.status_code == 302


def test_add_recipe_route_get():
    client = app.test_client()

    # Simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    # Simulate a GET request to the add_recipe route
    response_get = client.get('/add_recipe')

    # Check if the response status code is 200 (OK) for the GET request
    assert response_get.status_code == 200


def test_view_recipe_route_authenticated_user():
    client = app.test_client()

    # Simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the view_recipe route with the specified recipe ID
    response = client.get(f'/recipe/{recipe_id}')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_view_recipe_route_non_user():
    client = app.test_client()
    # Simulate a GET request to the view_recipe route as a non-user

    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the view_recipe route with the specified recipe ID
    response = client.get(f'/recipe/{recipe_id}')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_delete_recipe_route_authorized_user():
    client = app.test_client()

    # Simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the delete_recipe route with the specified recipe ID
    response = client.get(f'/delete_recipe/{recipe_id}')

    # Check if the response status code is 302 (Found/Redirect) for successful recipe deletion
    assert response.status_code == 302

def test_delete_recipe_route_unauthenticated_user():
    client = app.test_client()

    # Simulate a GET request to the delete_recipe route as an unauthenticated user
    
    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the delete_recipe route with the specified recipe ID
    response = client.get(f'/delete_recipe/{recipe_id}')

    # Check if the response status code is 302 (Found/Redirect) for unauthenticated user
    assert response.status_code == 302


def test_edit_recipe_route_authorized_user():
    client = app.test_client()

    # Simulate setting a user session 
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the edit_recipe route with the specified recipe ID
    response_get = client.get(f'/edit_recipe/{recipe_id}')

    # Check if the response status code is 302 (Found/Redirect) for viewing the edit form
    assert response_get.status_code == 302

    # Simulate a POST request to the edit_recipe route with form data for updating the recipe
    response_post = client.post(f'/edit_recipe/{recipe_id}', data={
        'recipe_name': 'Updated Recipe Name',
        'category': 'Updated Category',
        'recipe_description': 'Updated Description',
        'prep_time': '30 minutes',
        'cook_time': '45 minutes',
        'servings': '4',
        'method_step[0]': 'Step 1',
        'method_step[1]': 'Step 2',
        'ingredient[0]': 'Updated Ingredient 1',
        'quantity[0]': '2 cups',
        'ingredient[1]': 'Updated Ingredient 2',
        'quantity[1]': '1 tablespoon',
        'admin_description': 'Updated Admin Description',
        'product_link': 'Updated Product Link',
        'product_text': 'Updated Product Text',
        'product_image': 'Updated Product Image',
    })

    # Check if the response status code is 302 (Found/Redirect) for successful recipe update
    assert response_post.status_code == 302


def test_edit_recipe_route_unauthenticated_user():
    client = app.test_client()
    # Simulate a GET request to the edit_recipe route as an unauthenticated user
    
    recipe_id = '654b76ec44739e9d4e1a84ab'

    # Simulate a GET request to the edit_recipe route with the specified recipe ID
    response = client.get(f'/edit_recipe/{recipe_id}')

    # Check if the response status code is 302 (Found/Redirect) for unauthenticated user
    assert response.status_code == 302


def test_manage_categories_route_admin():
    client = app.test_client()

    # Simulate setting a user session for an admin
    with client.session_transaction() as sess:
        sess['user'] = 'admin'

    # Simulate a GET request to the manage_categories route
    response = client.get('/manage_categories')

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200


def test_manage_categories_route_non_admin():
    client = app.test_client()

    # Simulate setting a user session for a non-admin user
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    # Simulate a GET request to the manage_categories route
    response = client.get('/manage_categories')

    # Check if the response status code is 200 (OK) or another status code that you expect (e.g., 302 for unauthorized access)
    assert response.status_code == 200


def test_sign_out_route():
    client = app.test_client()

    # Simulate setting a user session
    with client.session_transaction() as sess:
        sess['user'] = 'testuser66'

    # Simulate a GET request to the sign_out route
    response = client.get('/sign_out')

    # Check if the response status code is 302 (Found/Redirect) after signing out
    assert response.status_code == 302

    # Check if the user is removed from the session
    with client.session_transaction() as sess:
        user = sess.get('user')
        assert user is None
