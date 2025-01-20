import os
import re
import importlib
import inspect


def get_docstring_from_class(class_path):
    try:
        # Split the full path into module path and object name
        module_path = '.'.join(class_path.split('.')[:-1])
        object_name = class_path.split('.')[-1]
        
        obj = None
        # First try direct import
        try:
            module = importlib.import_module(module_path)
            obj = getattr(module, object_name)
        except (ImportError, AttributeError):
            # If that fails and it's a packaged module, try with module name
            if 'packaged_modules' in module_path:
                try:
                    # Get the last component of the module path
                    module_name = module_path.split('.')[-1]
                    # Insert the module name before the class
                    new_module_path = f"{module_path}.{module_name}"
                    module = importlib.import_module(new_module_path)
                    obj = getattr(module, object_name)
                except (ImportError, AttributeError):
                    pass
            # If that fails and it's a logging function, try with utils path
            elif module_path == 'datasets.logging':
                try:
                    module = importlib.import_module('datasets.utils.logging')
                    obj = getattr(module, object_name)
                except (ImportError, AttributeError):
                    pass
        
        if obj is None:
            return f"[[autodoc]] {class_path}: Could not import {class_path}"
            
        # Get the docstring
        docstring = obj.__doc__
        if docstring:
            # If it's a function, we want to include the signature
            if inspect.isfunction(obj):
                signature = str(inspect.signature(obj))
                return f"```python\ndef {object_name}{signature}:\n```\n\n{docstring.strip()}"
            return docstring.strip()
        return f"No docstring found for {class_path}"
    except Exception as e:
        return f"[[autodoc]] {class_path}: {str(e)}"


def process_markdown_file(file_path):
    try:
        print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all [[autodoc]] directives
        pattern = r'\[\[autodoc\]\]\s+([^\s]+)'
        matches = re.finditer(pattern, content)
        
        # Replace each [[autodoc]] directive with the actual docstring
        for match in matches:
            class_path = match.group(1)
            docstring = get_docstring_from_class(class_path)
            content = content.replace(match.group(0), docstring)
        
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Completed processing {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.mdx') or file.endswith('.md'):  # Added .mdx extension
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)


if __name__ == "__main__":
    # Add the datasets source directory to the Python path
    import sys
    sys.path.append(os.path.abspath("src"))
    
    # Process all markdown files in docs/source/en
    process_directory("docs/source")