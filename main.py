import scratchattach
# https://scratch.mit.edu/projects/959972477/

# url = input("put project url here ") + "/"
def parse(url):
    if url[0:24] == "https://scratch.mit.edu/" and not (url[24:] == ""):
        if url.split("/")[3] == "projects":
            if url.split("/")[5] == "fullscreen":
                return ["prof", url.split("/")[4]]
            if "#comments-" in url.split("/")[5]:
                return ["pcom", url.split("/")[4], url.split("/")[5].replace("#comments-","")]
            return ["pro",url.split("/")[4]]

        elif url.split("/")[3] == "users":
            return ["use",url.split("/")[4]]

        elif url.split("/")[3] == "studios":
            if "#comments-" in url.split("/")[6]:
                return ["scom", int(url.split("/")[4]), url.split("/")[6].replace("#comments-","")]
            return ["stu",int(url.split("/")[4])]

        elif url.split("/")[3] == "discuss" and url.split("/")[4] == "topic":
            return ["for", url.split("/")[5]]


    else:
        return None