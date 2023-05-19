from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Tests the functionality of the blogly website"""

    def setUp(self):
        """Clear the tables and set test items before every test"""

        Post.query.delete()
        User.query.delete()
        user = User(first_name='John', last_name='Smith', image_url='https://tinyurl.com/default-pfp')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        post = Post(title='Hello', content='Hello Everyone', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up any failed transactions"""

        db.session.rollback()

    def test_html_home(self):
        """Test to see if the homepage loads properly"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Most Recent Posts</h1>', html)
    def test_html_users(self):
        """Test to see if the users from the database are loaded properly"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn(f'<a href="/users/{self.user_id}">John Smith</a>', html)
    def test_user_edit_form(self):
        """Test to see if the user edit form loads as intended"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" value="John" name="first_name">', html)
            self.assertIn('<input type="text" value="Smith" name="last_name">', html)
            self.assertIn('<input type="url" value="https://tinyurl.com/default-pfp" name="image_url">', html)
    def test_user_delete(self):
        """Test to see if the system deletes and redirects properly"""

        Post.query.delete()
        db.session.commit()
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/users/{self.user_id}">John Smith</a>', html)
    def test_post_delete(self):
        """Test to see if posts are deleted properly"""

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/posts/{ self.post_id }"><h2>Hello</h2></a>', html)
    def test_post_view(self):
        """Test to see if posts are displayed properly"""

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Hello</h1>', html)
            self.assertIn('<p class="post">Hello Everyone</p>', html)