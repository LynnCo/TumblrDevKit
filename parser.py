import re

def _sub_var_tumblr_to_jinja(match):
    match = match.group(0).lower()
    match = re.sub(r'\-', '_', match)
    match = '{'+match+'}'
    return match

def _sub_block_start(match):
    match = match.group(0).lower()
    var = match[7:-1]
    match = '{% if '+var+' %}'
    return match

def _sub_block_end(match):
    return '{% endif %}'

def _sub_post_variables_and_blocks(match):
    match = match.group(0).lower()
    match = 'post.'+match
    return match

def _sub_post_types(match):
    match = match.group(0).lower()
    match = 'type==\"'+match+'\"'
    return match

def parse_theme(path):
    POST_TYPES       = ['text','photopanorama','photoset','quote','link','chat','audio','video','answer']
    RE_POSTS         = r'(?ism)((\{block:(posts)\}).*?(\{\/block:\3\}))'
    RE_POST_TYPES    = r'(?ism)\{block:('+'|'.join(POST_TYPES)+r')\}.*?\{\/block:(\1)\}'
    RE_VARIABLEs     = r'(?ism)\{\w+\}'
    RE_BLOCKS        = r'(?ism)\{block:(\w+)\}.*?\{\/block:(/1)\}'

    
    # pull out posts block
    posts_index = re.search(RE_POSTS, html)
    posts = html[posts_index.start():posts_index.end()]
    # reformat (TYPE) to (posts.type == TYPE)
    posts = re.sub(RE_POST_TYPES, _sub_post_types, posts)
    # reformat (VAR) to (posts.VAR)
    posts = re.sub(RE_POST_VARIABLE, _sub_post_variables_and_blocks, posts)
    # reformat (BOOL) to (posts.BOOL)
    posts = re.sub(RE_POST_BLOCK, _sub_post_variables_and_blocks, posts)

    # return posts to rest of HTML
    html = html[:posts_index.start()] + posts + html[posts_index.end():]
    # change tumblr variables to jinja variables
    html = re.sub(RE_VARIABLE, _sub_var_tumblr_to_jinja, html)
    # swap every block except posts to an if block
    html = re.sub(RE_BLOCK_START, _sub_block_start, html)
    html = re.sub(RE_BLOCK_END, _sub_block_end, html)
    # swap the posts block to a for block
    html = re.sub(RE_POSTS_START, '{% for post in posts %}', html)
    html = re.sub(RE_POSTS_END, '{% endfor %}', html)


    return html