import html2text
from urllib.parse import urlparse

class CustomHTML2Text(html2text.HTML2Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_text = False

    def handle_starttag(self, tag, attrs):
        # Modify href and src attributes
       
        attrs = [(attr, urlparse(value).scheme + '://' +urlparse(value).netloc+ ''.join(urlparse(value).path[:10]))
             if attr in ['href', 'src'] and isinstance(value, str) else (attr, value)
             for attr, value in attrs]
        
        # Only include 'src' and 'href' attributes
        if tag == 'img':
            attrs = [(attr, value) for attr, value in attrs if attr == 'src']
        elif tag == 'a':
            attrs = [(attr, value) for attr, value in attrs if attr == 'href']
        else:
            attrs = []

        
        # Call the parent class's handle_starttag method with the modified attrs
        super().handle_starttag(tag, attrs)

        # Check if the tag has style="font-size:0px" and set the flag
        for attr, value in attrs:
            if attr == 'style' and 'font-size:0px' in value:
                self.ignore_text = True

    def handle_endtag(self, tag):
        # Call the parent class's handle_endtag method
        super().handle_endtag(tag)
        # Reset the flag when a tag ends
        self.ignore_text = False

    def handle_data(self, data, *args):
        # Only handle the data if the flag is not set
        if not self.ignore_text:
            super().handle_data(data)

    def handle_tag(self, tag, attrs, start):
        super().handle_tag(tag, attrs, start)

        if tag == 'input' and start:
            type_attr = dict(attrs).get('type', '')
            src_attr = dict(attrs).get('src', '')
            
            if type_attr and type_attr == 'image':
                self.o('[input type="%s"' % type_attr)
            
            if src_attr:
                self.o(' src="%s"]' % src_attr)