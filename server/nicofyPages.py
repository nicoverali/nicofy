PAGES_DIRECTORY = '../pages/'
SVG_DIRECTORY = '../assets/svgs/'
SERVER_ADDRESS = 'localhost:8000/'
JS_DIRECTORY = '../js/'

def get_Base_Layer():
    base = open(PAGES_DIRECTORY + 'base-layer.html')
    base_content = base.read()
    footer = open(PAGES_DIRECTORY + 'footer.html')
    footer_content = footer.read()
    base.close()
    footer.close()
    return base_content.replace('<!-- Footer -->', footer_content)

def get_Content_Of(file_path):
    oFile = open(file_path,'r')
    cFile = oFile.read()
    return cFile

def replace_Content(base, content):
    base_replaced = base.replace('<!-- Content -->', content)
    return base_replaced

def replace_BodyClass(base, class_name):
    base_replaced = base.replace('<!-- Body Class -->', class_name)
    return base_replaced

def replace_All_SVG(content):
    ocurrences = content.count('<!-- SVG:')
    index = 0
    for i in range(ocurrences):
        from_index = content.find('<!-- SVG:', index)
        to_index = content.find(' #-->', index)
        path = SVG_DIRECTORY + content[(from_index + 9):to_index]
        content = content.replace(content[from_index:to_index + 4], get_Content_Of(path))
        index = to_index
    return content

def replace(content, new_content, tag):
    from_index = content.find('<!-- ' + tag)
    to_index = content.find(' -->')
    content = content.replace(content[from_index:to_index + 4], new_content)
    return content


def get_Home():
    home = open(PAGES_DIRECTORY + 'home.html')
    home_content = home.read()
    home_content = replace_All_SVG(home_content)
    base = get_Base_Layer()
    base = replace_Content(base, home_content)
    base = replace_BodyClass(base, 'home')
    home.close()
    return base

def get_Redirect(new_link):
    redirect_page = open(PAGES_DIRECTORY + 'redirect.html')
    page_content = redirect_page.read()
    page_content = replace(page_content, new_link, 'Redirect Link')
    base = get_Base_Layer()
    base = replace_Content(base, page_content)
    base = replace_BodyClass(base, 'redirect-page')
    redirect-page.close()
    return base

def get_404_Notfound():
    notfound_page = open(PAGES_DIRECTORY + '404-notfound.html')
    page_content = notfound_page.read()
    base = get_Base_Layer()
    base = replace_Content(base, page_content)
    base = replace_BodyClass(base, '404-notfound')
    notfound_page.close()
    return base

def get_Succeed(url):
    succeed_page = open(PAGES_DIRECTORY + 'succeed.html')
    page_content = succeed_page.read()
    page_content = replace(page_content, url, 'New Link')
    base = get_Base_Layer()
    base = replace_Content(base, page_content)
    base = replace_BodyClass(base, 'succeed-page')
    succeed_page.close()
    return base
