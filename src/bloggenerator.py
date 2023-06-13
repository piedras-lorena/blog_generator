import re

from langchain.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain import LLMChain

import validators

class BlogGenerator:
    """This class generates a blog entrance for a company. 
    Taking as an input the company website and blog topic.

    Args:
        webpage (str): Url of the company's web page
        blog_topic (str): Topic we're going the create the blog about
        llm_summary (ChatOpenAI): llm model we're using to generate a summary of the company's webpage
        llm_blog (ChatOpenAI): llm model we're using to generate the blog
        summary_prompt (str): Prompt we're using to generate the webpage summary
        blog_prompt (str): Prompt we're using to generate the blog post
        blog_prompt_no_summary (str): Prompt we're using to generate the blog post when we don't have a company webpage summary
        length (int): Number of words to inlcude in blog
        verbose (bool): If true will print the outputs of each part
    """

    def __init__(
        self, webpage, blog_topic,
        llm_summary, llm_blog,
        summary_prompt, blog_prompt,
        blog_prompt_no_summary,
        length=1000, verbose=True
    ):
        if validators.url(webpage):
            self.webpage = webpage
        else:
            # TODO: If url is not valid generate blog post without url content
            self.webpage = ''
            print(f'Invalid url: {webpage}')
            # raise ValueError('Invalid URL')
        self.blog_topic = blog_topic
        self.llm_summary = llm_summary
        self.llm_blog = llm_blog
        self.summary_prompt = summary_prompt
        self.blog_prompt = blog_prompt
        self.blog_prompt_no_summary = blog_prompt_no_summary
        self.length = length
        self.verbose = verbose
        
        self.url_content = []
        self.docs = []
        self.company_summary = ''
    
    def load_url_content(self):
        """Function that gets html text from webpage

        Attributes:
            webpage (str): Url of the company's web page
            url_content (list): List containing webpage content in a string
        """
        url_content = []
        # Retrieve webpage content if we have a valid url
        if len(self.webpage) > 0:
            urls = [self.webpage]
            loader = UnstructuredURLLoader(urls=urls)
            url_content = loader.load()
            if len(url_content) == 0:
                print('Unable to retrieve URL content')
            else:
                if self.verbose:
                    print(f'1 Retrieved the following content from webpage: {url_content[0].page_content}')
        return url_content

    def split_document(self, content):
        """Function that splits text to make sure that we don't get over our llm's character limits

        Attributes:
            url_content (list): List containing webpage content in a string
            docs (list): List containing documents with text split by CharacterTextSplitter
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 4000,
            chunk_overlap  = 200,
            length_function = len,
        )
        texts = text_splitter.split_text(content)
        return [Document(page_content=t) for t in texts]
    
    def summarize_docs(self, docs):
        """Summarize webpage content

        Attributes:
            summary_prompt (str): Prompt we're using to generate the webpage summary
            company_summary (str): Summary of company's website
        """
        summarize_template = PromptTemplate(template=self.summary_prompt, input_variables=["text"])
        chain = load_summarize_chain(
            self.llm_summary, chain_type="stuff", prompt=summarize_template)
        company_summary = chain.run(docs)
        # When more than one document is summarized the response is "[num] Webpage summary: [Summary]"
        self.company_summary = re.sub('^[0-9]+ Webpage summary: ', '', company_summary)
        if self.verbose:
            print(f'2 Webpage summary: {self.company_summary}')
    
    def write_blog_post(self):
        """Get LLM to write a blog post by using the webpage summary and topic

        Attributes:
            blog_prompt (str): Prompt we're using to generate the blog post
            blog_topic (str): Topic we're going the create the blog about
            company_summary (str): Summary of company's website
        
        Returns:
            String with blog content in Markdown
        """
        if len(self.company_summary) > 0:
            blog_template = PromptTemplate(
                template=self.blog_prompt, input_variables=["length","topic", "summary"])
            summary_chain = LLMChain(
                llm=self.llm_blog,
                prompt=blog_template
            )
            return summary_chain.run(
                {'length': self.length, 'topic':self.blog_topic, 'summary':self.company_summary})
        # Create blog post without webpage content
        else:
            blog_template = PromptTemplate(
                template=self.blog_prompt_no_summary, input_variables=["length","topic"])
            summary_chain = LLMChain(
                llm=self.llm_blog,
                prompt=blog_template
            )
            return summary_chain.run(
                {'length': self.length, 'topic':self.blog_topic})

    
    def generate_blog_post(self):
        """Write blog post for a company from scratch.
        
        Returns:
            String with blog content in Markdown
        """
        url_content = self.load_url_content()
        if len(url_content) > 0:
            docs = self.split_document(url_content[0].page_content)
            self.summarize_docs(docs)
        return self.write_blog_post()
