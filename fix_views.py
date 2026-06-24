import os
import re

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # replace get('per_page', 5) -> get('per_page', 10)
            new_content = content.replace("request.GET.get('per_page', 10)", "request.GET.get('per_page', 10)")
            # replace [10, 15, 25] -> [10, 15, 25]
            new_content = new_content.replace("[10, 15, 25]", "[10, 15, 25]")
            # replace per_page = 10 -> per_page = 10
            # Be careful with per_page = 10, it usually comes right after
            new_content = re.sub(r'per_page\s*=\s*5', 'per_page = 10', new_content)
            
            if content != new_content:
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"Updated {path}")
