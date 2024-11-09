from windows import duplicate_files

max_dups = 20
dir_file = "dir_downloads.txt" # output of dir command
fp = open(dir_file, "r")
dir_output = fp.read()
# print(dir_output)
dups = duplicate_files(dir_output)
print("# of duplicate groups:", len(dups), end="\n\n")
for group in dups[:max_dups]:
    for file in group:
        print(file)
    print()