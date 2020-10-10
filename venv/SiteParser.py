from bs4 import BeautifulSoup
url = "Site/site.html"

DOM_tree = []

# , '[ ID : ', tag['id'] , ' ]'
def parse_DOM_tree(tag,added_str):
    print(tag)
    print(tag.name)
    DOM_tree.append(''.join([added_str ,tag.name]))
    for child in tag.children:
        parse_DOM_tree(child,'  ')


def walker(soup,added_str):
    if soup.name is not None:
        for child in soup.children:
            # process node
            if child.name is not None:
                DOM_tree.append(''.join(''.join([added_str, child.name])))
                # print(str(child.name))
                walker(child,'\t   ')


def get_DOM_tree():
    f = open(url, "r")
    site_code = ''.join(f.readlines())
    f.close()
    site = BeautifulSoup(site_code, 'html.parser')
    walker(site.body, '')
    return DOM_tree

