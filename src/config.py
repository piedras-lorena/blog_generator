PROMPTS = {
    'summary': """Write a concise summary of the following:

    
    {text}
    
    
    CONCISE SUMMARY IN SPANISH:""",
    'blog_post': """
    Eres un Gestor de Contenido responsable de desarrollar y ejecutar estrategias de contenido, centrándote específicamente en escribir entradas de blog atractivas e informativas en español. Tu rol implica crear contenido convincente que conecte con la audiencia objetivo, optimizarlo para los motores de búsqueda y gestionar el calendario de contenidos.
    
    Crea una entrada de blog en español de {length} palabras sobre {topic} usando Markdown para una empresa que tiene el siguiente contenido en su página web
    
    "{summary}"
    
    ENTRADA DE BLOG CON MARKDOWN:""",
    'blog_post_no_summary': """
    Eres un Gestor de Contenido responsable de desarrollar y ejecutar estrategias de contenido, centrándote específicamente en escribir entradas de blog atractivas e informativas en español. Tu rol implica crear contenido convincente que conecte con la audiencia objetivo, optimizarlo para los motores de búsqueda y gestionar el calendario de contenidos.
    
    Crea una entrada de blog en español de {length} palabras sobre {topic} usando Markdown.
    
    ENTRADA DE BLOG CON MARKDOWN:"""
}

BLOG_TEMPLATE = """<h1></h1>
<p> [Demo] </p>
<p><em>¡Hola! Muchas gracias por tu interés en Blogggs. Este artículo es un ejemplo del trabajo 
que realizamos y una probadita del tipo de posts que podemos hacer para tu marca.</em></p>
<br>
<p><em>Tómalo como un regalo y siéntete libre de publicarlo en tu blog</em> 😉</p>
<br>
<hr>
<br>
{blog_text}
<br>
<hr>
<br>
<br>
<p><strong>¿Te gustó lo que leíste y te gustaría que empezáramos a colaborar contigo?</strong></p>
<br>
<p><em>Puedes elegir el plan que más te acomode a través de <a href="http://www.blogggs.com/comenzar">www.blogggs.com/comenzar</a>.</em></p>
<p><em>Si tienes alguna duda antes de contratar, escríbenos a <a href="mailto:agustin@blogggs.com">agustin@blogggs.com</a>.</em></p>
<br>
<p><em>¡Saludos y esperamos escuchar de ti muy pronto!</em></p>
<br>
<p><em>Si NO te gustó el contenido, agradeceríamos mucho tu feedback a través de <a href="https://forms.gle/R9FFLyKVEui5dCZG6">esta liga</a>.</em></p>"""

FOLDER_ID = '1bHUB2-YELFEl690aDzhs_zzOTYntAiTk'