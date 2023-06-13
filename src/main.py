import dotenv
from pathlib import Path
import os

from langchain.chat_models import ChatOpenAI
import pandas as pd

from bloggenerator import BlogGenerator
from config import *
from googledocwritter import GoogleDocWritter



env_file = os.path.join(Path(__file__).parent.absolute(),'..', '.env')
dotenv.load_dotenv(env_file, override=True)

def main(blog_post_info):
    llm_summary = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
    llm_blog = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)
    blog_post_info.rename(
        columns={
            'Tema del artículo': 'tema_articulo',
            'Página web': 'pagina_web'
            }, inplace=True)
    for row in blog_post_info.itertuples():
        print('-'*5 + f' Running blog post for {row.tema_articulo}')
        blog_generator = BlogGenerator(
            row.pagina_web, row.tema_articulo,
            llm_summary, llm_blog,
            PROMPTS['summary'], PROMPTS['blog_post'],
            PROMPTS['blog_post_no_summary']
        )
        blog_content = blog_generator.generate_blog_post()
        google_doc_writter = GoogleDocWritter(
            webpage=row.pagina_web, blog_post=blog_content,
            template=BLOG_TEMPLATE,
            folder_id=FOLDER_ID
        )
        gdoc = google_doc_writter.upload_blog_post()

if __name__ == '__main__':
    file_path = os.path.join(Path(__file__).parent.absolute(),'Demo Submissions Blogggs - Sheet1.csv')
    blog_post_info = pd.read_csv(file_path)
    blog_post_info.rename(
    columns={
        'Tema del artículo': 'tema_articulo',
        'Página web': 'pagina_web'
        }, inplace=True)
    
    main(blog_post_info)


