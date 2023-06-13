from pathlib import Path
import os
import json

from markdown import markdown
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class AuthenticationError(Exception):
    pass


class GoogleDocWritter():
    def __init__(self, webpage, blog_post, template, folder_id, path_to_google_creds=None):
        if path_to_google_creds:
            self.path_to_google_creds = path_to_google_creds
        else:
            self.path_to_google_creds = Path(__file__).parent.absolute()
        self.webpage = webpage
        self.blog_post = blog_post
        self.template = template
        self.folder_id = folder_id

        self.gauth = None
        self.drive = None
    
    def write_creds(self):
        """ Write service account credentials to disk based on environment variables."""
        credentials = {
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
        }
        with open(os.path.join(self.path_to_google_creds, os.getenv("GOOGLE_CREDENTIALS_FILENAME")), "w+") as f:
            f.write(json.dumps(credentials))
    
    def authenticate(self):
        """Authenticate to use google docs."""
        secret_file_path = os.path.join(self.path_to_google_creds, os.getenv("GOOGLE_CREDENTIALS_FILENAME"))
        if not os.path.exists(secret_file_path):
            raise ValueError('Can not find secret file in the provided path')

        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": secret_file_path,
            }
        }
        
        self.gauth = GoogleAuth(settings=settings)
        self.gauth.ServiceAuth()
    
    def generate_html_post(self):
        """Convert from markdown to html and paste content in html template"""
        htmlpost = markdown(self.blog_post)
        return self.template.format(blog_text=htmlpost)

    def create_file(self, htmldoc):
        """Create google doc in given folder, paste html content and return url"""
        if self.gauth:
            self.drive = GoogleDrive(self.gauth)
            gdoc = self.drive.CreateFile(
                {
                    'parents': [{'id': self.folder_id}],
                    "title": f"Demo - {self.webpage}",
                    "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
            )
            gdoc.SetContentString(htmldoc)
            gdoc.Upload()
            return gdoc
        else:
            raise AuthenticationError("Missing authentication")
    
    def upload_blog_post(self):
        """Generate new google doc document with blog post"""
        self.write_creds()
        self.authenticate()
        htmldoc = self.generate_html_post()
        gdoc = self.create_file(htmldoc)
        return gdoc 
        