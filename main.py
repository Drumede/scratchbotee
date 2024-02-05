import scratchattach
# https://scratch.mit.edu/projects/959972477/

# url = input("put project url here ") + "/"
def parse(url):
    if url[0:24] == "https://scratch.mit.edu/" and not (url[24:] == ""):
        if url.split("/")[3] == "projects":
            return ["pro",url.split("/")[4]]

        elif url.split("/")[3] == "users":
            return ["use",url.split("/")[4]]

        elif url.split("/")[3] == "studios":
            return ["stu",int(url.split("/")[4])]

        elif url.split("/")[3] == "discuss" and url.split("/")[4] == "topic":
            return ["for", url.split("/")[5]]
    else:
        return None