import json
import dotenv
from pathlib import Path
import time
import os
import sys
import unittest
from unittest import mock

from pydrive2.auth import AuthenticationError


sys.path.append(os.path.join(Path(__file__).parent.absolute(),'..'))
from src.googledocwritter import GoogleDocWritter
from src.config import *

env_file = os.path.join(Path(__file__).parent.absolute(),'..', '.env')
dotenv.load_dotenv(env_file, override=True)

class TestBlogGen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_file = os.path.join(Path(__file__).parent.absolute(),'blog_test.txt')
        with open(test_file) as f:
            blog_post = f.read()
        
        cls.google_doc_writter = GoogleDocWritter(
            webpage="test.com", blog_post=blog_post,
            template=BLOG_TEMPLATE,
            folder_id=FOLDER_ID
            )
    
    def test_write_creds(self):
        self.google_doc_writter.write_creds()

        secret_path = os.path.join(self.google_doc_writter.path_to_google_creds, os.getenv("GOOGLE_CREDENTIALS_FILENAME"))
        print(secret_path)
        with open(secret_path) as f:
            creds = json.load(f)

        self.assertEqual(os.getenv("GOOGLE_PRIVATE_KEY_ID"), creds['private_key_id'])
        self.assertEqual(os.getenv("GOOGLE_PRIVATE_KEY"), creds['private_key'])
    
    def test_authenticate(self):
        try:
            self.google_doc_writter.authenticate()
        except AuthenticationError:
            self.fail("wasn't able to authenticate")
    
    def test_generate_html_post(self):
        google_doc_writter = GoogleDocWritter(
            webpage="test.com", blog_post='# Testing',
            template="""<p>The name of the post is </p> <br> {blog_text}""",
            folder_id=FOLDER_ID
            )
        html_post = google_doc_writter.generate_html_post()
        html_post_target = """<p>The name of the post is </p> <br> <h1>Testing</h1>"""
        self.assertEqual(html_post, html_post_target)
    
    def test_create_file(self):
        google_doc_writter = GoogleDocWritter(
            webpage="test.com", blog_post='# Testing',
            template="""<h1></h1><p>The name of the post is </p> <br> {blog_text}""",
            folder_id=FOLDER_ID
            )
        
        google_doc_writter.write_creds()
        google_doc_writter.authenticate()
        html_post = google_doc_writter.generate_html_post()
        gdoc = google_doc_writter.create_file(html_post)
        time.sleep(10)

        # Check if file exists in google docs
        file_list = google_doc_writter.drive.ListFile(
            {
                "q": '"{}" in parents and title="{}" and trashed=false'.format(
                    FOLDER_ID, 'Demo - test.com'
                )
            }
        ).GetList()
        print(len(file_list))
        self.assertTrue(len(file_list) > 0)
        gdoc.Trash()  # Move file to trash.
        gdoc.UnTrash()  # Move file out of trash.
        gdoc.Delete()
    
if __name__ == '__main__':
    unittest.main()



