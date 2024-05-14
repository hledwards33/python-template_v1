import markdown

path = r"C:\Users\GV147BE\PycharmProjects\python-template\README.md"

with open(path, 'r') as f:
    markdown_string = f.read()

# 2
html_string = markdown.markdown(markdown_string)

print()