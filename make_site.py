import sys, os, json
import PIL.Image

this_path = os.path.abspath(os.path.dirname(__file__))


class Gallery:
    def __init__(self, title, dir, name, preview_index, desc):
        self.title = escape(title)
        self.dir = dir
        self.name = name
        self.preview_index = preview_index
        self.desc = desc
        self.images = []

    def link(self):
        return "g_" + self.name + ".html"
    def preview_img(self, d):
        return d.imgs[self.preview_index]

class Image:
    def __init__(self, gal, gid, pid, filename, desc, alttext, exclude):
        self.gal = gal
        self.gid = gid  # id of the gallery
        self.pid = pid  # id of the image
        self.dir = gal.dir
        self.filename = filename
        self.desc = escape(desc)
        self.title = escape(alttext)
        self.exclude = exclude

    def full(self):
        return "imgs/" + self.dir + "/" + self.filename
    def disp(self):
        return "imgs/" + self.dir + "/disps/disps_" + self.filename
    def page(self):
        return "i_" + self.dir + "_" + os.path.splitext(self.filename)[0] + ".html"

class Data:
    def __init__(self):
        self.gal = {}  # map gid to Gallery
        self.gal_by_name = {}
        self.imgs = {}  # map pid to Image


def strip_path(p):
    return '/'.join(p.split('/')[2:])

def read_wp():
    gal_j = json.load(open(os.path.join(this_path, "galleries.json"), encoding="utf-8"))
    imgs_j = json.load(open(os.path.join(this_path, "images.json"), encoding="utf-8"))

    d = Data()  
    for g in gal_j:
        gal = Gallery(g["title"], strip_path(g["path"]), g["name"], g["previewpic"], g["galdesc"])
        d.gal[g["gid"]] = gal
        d.gal_by_name[g["name"]] = gal

    for p in imgs_j:
        gid = p["galleryid"]
        pid = p["pid"]
        img = Image(d.gal[gid], gid, pid, p["filename"], p["description"], p["alttext"], p["exclude"] == "1")
        d.imgs[pid] = img
        if not img.exclude:
            d.gal[img.gid].images.append(img)

    return d

def div(*args, cls, idd=None):
    sid = "" if idd is None else ' id="'+idd+'"'
    return f'<div class="{cls}"{sid}>{"".join(args)}</div>'

def a(*text, href, cls):
    if isinstance(text, tuple):
        text = "".join(text)
    return f'<a href="{href}" class="{cls}">{text}</a>'

def escape(s):
    return s.replace('\\"', '&quot;').replace('"', '&quot;').replace('\\', '').replace("\'", "'")

def img(src, title=None, cls=""):
    titl = "" if title is None else title
    return f'<img src="{src}"{titl} class="{cls}">'


def make_template(filename, content, call=""):
    t = open(os.path.join(this_path, "template.html"), encoding="utf-8").read()
    t = t.replace("{content}", content).replace("{main_call}", call)
    out_path = os.path.join(this_path, "out", filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(t)
    print("wrote", out_path)


INCLUDE_GALLERIES = ["drawing", "painting", "new_works", "hatachana", "bezalel"]

def create_main(d):
    items = []
    for name in INCLUDE_GALLERIES:
        gal = d.gal_by_name[name]
        items.append(div(a(img(src=gal.preview_img(d).full(), cls="main_gal_img"),
                           div(gal.title, cls="main_gal_text"), href=gal.link(), cls="gal_a"), cls="gal"))
    cont = div(*items, cls="gal_menu")
    make_template("index.html", cont)


def make_galleries_text_menu(d):
    items = []
    items.append( a(div("אודות", cls="gal_text_menu_item"), href="about.html", cls="gal_text_a") )
    for name in INCLUDE_GALLERIES:
        gal = d.gal_by_name[name]
        #items.append(div(a(gal.title, href=gal.link(), cls="gal_text_a"), cls="gal_text_menu_item"))
        items.append(a(div(gal.title, cls="gal_text_menu_item"), href=gal.link(), cls="gal_text_a"))
    return div(*items, cls="gal_text_menu")


def make_gal_disp_lst(gal):
    items = []
    for im in gal.images:
        if im.exclude:
            continue
        items.append(div(a(img(src=im.disp(), title=im.desc, cls="disp_im"), href=im.page(), cls="disp_im_a"), cls="disp_im_div"))
    return div(*items, cls="disps", idd="disps")


def create_gal_pages(d):
    for name in INCLUDE_GALLERIES:
        gal = d.gal_by_name[name]
        cont = make_galleries_text_menu(d)
        cont += div(div(gal.title, cls="gal_title"),
                    make_gal_disp_lst(gal), cls="gal_view", idd="gal_view")
        make_template(gal.link(), cont, "order_disps()")


def create_img_pages(d):
    for name in INCLUDE_GALLERIES:
        gal = d.gal_by_name[name]
        # need to go over images in gallery to have a good order
        for i, im in enumerate(gal.images):
            pim = PIL.Image.open(os.path.join(this_path, "out", im.full()))
            w, h = pim.size
            im_cls = "im_vert" if h > w else "im_horz"
            im_next = gal.images[(i + 1) % len(gal.images)]
            im_prev = gal.images[(i - 1) % len(gal.images)]

            cont = make_galleries_text_menu(d)
            cont += div(div(im.title, cls="im_title"),
                        div(im.desc, cls="im_desc"),
                        div(a(div(div(cls="im_next_circ"), cls="im_next_div"), href=im_next.page(), cls="im_next_a"),
                            a(img(src=im.full(), cls="im_full_img", title=im.title), href=im.full(), cls="im_full_a"),
                            a(div(div(cls="im_prev_circ"), cls="im_prev_div"), href=im_prev.page(),cls="im_prev_a"),
                            cls="im_full_div"),
                        cls=im_cls)
            cont += make_gal_disp_lst(im.gal)
            make_template(im.page(), cont, "order_disps()")

def create_about():
    make_template("about.html", open(os.path.join(this_path, "about.html"), encoding="utf-8").read())

def main():
    d = read_wp()
    create_main(d)
    create_gal_pages(d)
    create_img_pages(d)
    create_about()

    print("done")


if __name__ == "__main__":
    main()
