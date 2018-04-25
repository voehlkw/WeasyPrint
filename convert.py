from weasyprint import HTML, CSS


def get_toc(bookmarks, format, page_offset=0, level=0):
    return ''.join([format % (str(page_offset + page), title, get_toc(children, format, page_offset, level + 1))
                    for title, (page, x, y), children in bookmarks])


def get_toc_doc(bookmarks, outline_format='%s', toc_format='%s', styles=None):
    toc_len = len(HTML(string=toc_format % get_toc(bookmarks, outline_format)).render(stylesheets=styles).pages)
    return HTML(string=toc_format % get_toc(bookmarks, outline_format, toc_len + 1)).render(stylesheets=styles)


def add_toc(document, **kwargs):
    toc = get_toc_doc(document.make_bookmark_tree(), **kwargs)
    return document.copy([page for doc in (toc, document) for page in doc.pages])


def convert_book(filename):
    doc = HTML(filename).render(
        [CSS('assets/css/main.css'), CSS('assets/css/content.css'), ])
    doc = add_toc(doc,
                  outline_format='<div class="entry"><div class="page">%s</div><div class="title">%s</div><div class="children">%s</div></div>',
                  toc_format='<div class="toc">%s</div>',
                  styles=[CSS('assets/css/main.css'), CSS('assets/css/toc.css'), ])
    doc.write_pdf(filename + '.pdf')


def benchmark(func):
    from time import time
    start = time()
    func()
    return time() - start


print("%fs" % benchmark(lambda: convert_book('test/print_test_modified.html')))