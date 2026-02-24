from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "sequences/U5.txt"

# -- Open and read the file
file_contents = Path(FILENAME).read_text()
body = file_contents.split("\n", 1)[1]

# -- Print the contents on the console
print("Body of the U5.txt file:")
print(body)