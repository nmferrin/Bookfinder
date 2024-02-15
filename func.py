import re

def process_description(description):
    ''' Process description on book page to clean content and remove random links '''
    if isinstance(description, dict):
        description_text = description.get('value', '')
    else:
        description_text = description
    
    # Convert markdown links to HTML links
    description_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', description_text)
    
    # Replace escaped newline characters with HTML line breaks
    description_text = description_text.replace('\r\n', '<br>')
    
    return description_text