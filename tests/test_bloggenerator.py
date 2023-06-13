import dotenv
from pathlib import Path
import os
import sys
import unittest
from unittest import mock

from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI

sys.path.append(os.path.join(Path(__file__).parent.absolute(),'..'))
from src.bloggenerator import BlogGenerator
from src.config import PROMPTS

env_file = os.path.join(Path(__file__).parent.absolute(),'..', '.env')
dotenv.load_dotenv(env_file, override=True)


class TestBlogGen(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        cls.blog_generator = BlogGenerator(
            'http://google.com', 'testing',
            cls.llm, cls.llm,
            PROMPTS['summary'], PROMPTS['blog_post'], 
            PROMPTS['blog_post_no_summary'],
            length=50
        )
        test_file = os.path.join(Path(__file__).parent.absolute(),'test.txt')
        with open(test_file) as f:
            cls.test_text = f.read()

    def tearDown(self):
        pass

    def test_init(self):
        blog_gen1 = BlogGenerator(
            'no an url', 'testing',
            None, None,
            '', '', ''
            )
        self.assertEqual(blog_gen1.webpage, '')
        blog_gen2 = BlogGenerator(
            'google.com', 'testing',
            None, None,
            '', '', ''
            )
        self.assertEqual(blog_gen2.webpage, '')

    @mock.patch('src.bloggenerator.UnstructuredURLLoader.load')
    def test_load_url_content(self, mock_load_url):
        mock_load_url.return_value = []
        url_content = self.blog_generator.load_url_content()
        self.assertEqual(url_content, [])
        
        mock_load_url.return_value = [Document(page_content='Heiiiiii')]
        url_content = self.blog_generator.load_url_content()
        self.assertEqual(url_content[0].page_content, 'Heiiiiii')
        self.assertEqual(len(url_content), 1)

    def test_split_document(self):
        docs = self.blog_generator.split_document(self.test_text)
        self.assertEqual(len(docs), 2)

    def test_summarize_docs(self):
        documents = self.blog_generator.split_document(self.test_text)
        self.blog_generator.summarize_docs(documents)
        self.assertTrue(len(self.blog_generator.company_summary) > 0)

    def test_write_blog_post(self):
        self.blog_generator.company_summary = 'La empresa Ben and Frank ofrece envíos y devoluciones gratuitas en toda la República. También ofrecen exámenes de la vista y tienen varias colecciones de productos. Se puede rastrear el pedido y contactarlos por correo electrónico.'
        blog_post = self.blog_generator.write_blog_post()
        self.assertTrue(len(blog_post) > 0)

        self.blog_generator.company_summary = ''
        blog_post = self.blog_generator.write_blog_post()
        self.assertTrue(len(blog_post) > 0)



if __name__ == '__main__':
    unittest.main()
