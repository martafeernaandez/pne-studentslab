text = "  Hello, World! Welcome to Python Programming.  "

stripped = text.strip()
print("Stripped: ", stripped)
print("Number of words: ", len(text.split()))
print("Title case: ", text.title())
print("Starts with hello: ", stripped.startswith('Hello'))
print("Ends with ing: ", stripped.endswith('ing.'))
print("Python position: ", stripped.find('Python'))
print("Joined: ", "-".join(text.split()))