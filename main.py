import markdown_strings as md

response = md.header("Main Title\n", 1)
response += md.header("Sub Title", 2)
print(response)