from os import listdir

files = listdir("app/wordlists")
txt_files = [f for f in files if f.endswith(".txt")]
# change the featured files here
featured_files = ["animals.txt", "countries.txt", "colors.txt"]

wordlist_dict = []
for file in txt_files:

    name = file[:-4]

    wordlist_dict.append(
        {
            "name": name.replace("_", " "),
            "file": file,
            "featured": True if file in featured_files else False,
        }
    )
