from weasyprint import HTML, CSS, document, Document, Page
from weasyprint.fonts import FontConfiguration

font_config = FontConfiguration()
html = HTML('http://localhost:5000/myview/method1/abc1')
# html2 = HTML('http://localhost:5000/myview/method1/abc1')
'''
html = HTML(string="""
<h1>The title</h1>
<p>
Apparently we had reached a great height in the atmosphere, 
for the sky was a dead black, and the stars had ceased to twinkle. 
By the same illusion which lifts the horizon of the sea to the level 
of the spectator on a hillside, the sable cloud beneath was dished out, 
and the car seemed to float in the middle of an immense dark sphere, 
whose upper half was strewn with silver. Looking down into the dark gulf below, 
I could see a ruddy light streaming through a rift in the clouds.
</p>
<div>one two three中文</div>
"""
            )
css = CSS(string="""
    @font-face {
        font-family: Gentium;
        src: url(https://fonts.googleapis.com/css?family=Gentium+Basic);
    }
    @font-face {
        font-family: KozGoPro;
        src: url('KozGoPro-Regular.otf');
    }
    h1, p { font-family: Gentium }

     """, font_config=font_config)
'''
css=CSS(string="""
@page { 
 size: a4 portrait;
    margin: 5mm 5mm 5mm 5mm;
    counter-increment: page;
    @bottom-center {
        content: '(c) XX COMPANY - Page ' counter(page);
        white-space: pre;
        color: grey;
    }

}

""")

html.write_pdf('./example.pdf', stylesheets=[css])
# d1 = html.render(stylesheets=[css])
# # d2 = html2.render(stylesheets=[css])
#
# all_pages = []
#
# # for doc in d1, d2:
# for doc in d1:
#     for p in doc.pages:
#         all_pages.append(p)
#
# pdf_file = d1.copy(all_pages)
#
# pdf = pdf_file.write_pdf('./example.pdf')
#
# print(1)
'''
def verpdf(request, pk):
    odet = get_object_or_404(Note, pk = pk)
    template = get_template('pdfnot.html')
    template1 = get_template('pdfnot2.html')
    p1 = template.render({'odet': odet}).encode(encoding="ISO-8859-1")
    p2 = template1.render({'note':odet}).encode(encoding="ISO-8859-1")
    pdf1 = HTML(string=p1)
    pdf2 = HTML(string=p2)
    pdf11 = pdf1.render()
    pdf12 = pdf2.render()

    val = []

    for doc in pdf11, pdf12:
        for p in doc.pages:
            val.append(p)

    pdf_file = pdf11.copy(val).write_pdf() # use metadata of pdf11

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return http_response
'''