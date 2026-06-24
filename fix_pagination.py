import os
import re

template_dir = 'templates'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Match the options block for pagination
            # Usually looks like:
            # <option value="5" {% if per_page == 5 %}selected{% endif %}>5</option>
            # <option value="15" {% if per_page == 15 %}selected{% endif %}>15</option>
            # <option value="25" {% if per_page == 25 %}selected{% endif %}>25</option>
            # <option value="50" {% if per_page == 50 %}selected{% endif %}>50</option>
            
            new_content = re.sub(
                r'<option value="5"[^>]*>5</option>\s*<option value="15"[^>]*>15</option>\s*<option value="25"[^>]*>25</option>\s*<option value="50"[^>]*>50</option>',
                '''<option value="10" {% if per_page == 10 %}selected{% endif %}>10</option>
                                <option value="15" {% if per_page == 15 %}selected{% endif %}>15</option>
                                <option value="25" {% if per_page == 25 %}selected{% endif %}>25</option>''',
                content
            )
            
            new_content = re.sub(
                r'<option value="5"[^>]*>5</option>\s*<option value="15"[^>]*>15</option>\s*<option value="25"[^>]*>25</option>\s*<option value="50"[^>]*>50</option>',
                '''<option value="10" {% if per_page==10 %}selected{% endif %}>10</option>
                                <option value="15" {% if per_page==15 %}selected{% endif %}>15</option>
                                <option value="25" {% if per_page==25 %}selected{% endif %}>25</option>''',
                new_content
            )
            
            # for the case where there is == without spaces
            if 'value="5"' in new_content and 'value="50"' in new_content:
                new_content = re.sub(
                    r'<option value="5"[ \t]+{% if per_page==5 %\}selected{% endif %}>5</option>\s*<option value="15"[ \t]+{% if per_page==15 %\}selected{% endif %}>15</option>\s*<option value="25"[ \t]+{% if per_page==25 %\}selected{% endif %}>25</option>\s*<option value="50"[ \t]+{% if per_page==50 %\}selected{% endif %}>50</option>',
                    '''<option value="10" {% if per_page==10 %}selected{% endif %}>10</option>
                                <option value="15" {% if per_page==15 %}selected{% endif %}>15</option>
                                <option value="25" {% if per_page==25 %}selected{% endif %}>25</option>''',
                    new_content
                )
                
            if content != new_content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Updated {path}")
