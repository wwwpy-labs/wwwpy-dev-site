from common.fix_img import FixImg

# language=html
_html = """
<div><img alt="image.png" class="CToWUd a6T" data-bit="iit" data-image-whitelisted="" height="303"
              src="https://wwwpy.dev/1"
              style="cursor: pointer; outline: 0px" tabindex="0" width="484"/><br/></div>
    <div><br/></div>
    <div>Dettagli lavoro sul blog/website:</div>
    <img alt="logger-levels.gif" class="CToWUd a6T" data-bit="iit" data-image-whitelisted="" height="484"
         src="https://wwwpy.dev/2"
         style="cursor: pointer; outline: 0px" tabindex="0" width="428"/>
    <div><br/></div>
    <div>Static site generation attuale:</div>
    <div><img alt="image.png" class="CToWUd a6T" data-bit="iit" data-image-whitelisted="" height="387"
              src="https://wwwpy.dev/3"
              style="cursor: pointer; outline: 0px" tabindex="0" width="484"/></div>
              """


def test_fix_img():
    target = FixImg(_html, 'p1-')

    assert target.links.new_src_list == [link.new_src for link in target.links]

    assert target.links.new_src_list == [
        'p1-image-00.png',
        'p1-logger-levels.gif',
        'p1-image-01.png',
    ]


def test_src():
    target = FixImg(_html, 'p1-')

    assert target.links.only_src_list == [link.src for link in target.links]

    assert target.links.only_src_list == [
        'https://wwwpy.dev/1',
        'https://wwwpy.dev/2',
        'https://wwwpy.dev/3',
    ]


def test_no_src_and_no_alt_should_not_fail():
    html = "<br><img width='3'><hr><img width='4'>"

    target = FixImg(html, 'p1-')

    assert target.links.new_src_list == ['', '']
    assert target.links.only_src_list == ['', '']


def test_location():
    html = "<br><img width='3'><hr><img width='4'><link>"
    target = FixImg(html, 'p1-')

    assert target.links[0].location == (4, 19)
    assert target.links[1].location == (23, 38)


def test_new_html__plain_case():
    html = ("<br><img alt='image.png' src='https://wwwpy.dev/1'><link>"
            "<br><img alt='image.png' src='https://wwwpy.dev/2'>uff")
    target = FixImg(html, 'p1-')

    # we generate an img with only the new src
    assert target.new_html == (
        '<br><img src="p1-image-00.png"><link>'
        '<br><img src="p1-image-01.png">uff'
    )


def test_new_html__width_height():
    html = ("""<br><img alt='image.png' src='https://wwwpy.dev/1' width='123' height="45"><link>"""
            """<br><img alt='image.png' src='https://wwwpy.dev/2' width="67" height='89'><link>uff""")
    target = FixImg(html, 'p1-')

    assert target.links.only_width_list == ['123', '67']
    assert target.links.only_height_list == ['45', '89']


def test_new_html__width_height_in_new_html():
    html = ("""<br><img alt='image.png' src='https://wwwpy.dev/1' width='123' height="45"><link>"""
            """<br><img alt='image.png' src='https://wwwpy.dev/2' width="67" height='89'><link>uff""")
    target = FixImg(html, 'p1-')

    # we need also to keep width and height in new_html
    assert target.new_html == (
        '<br><img src="p1-image-00.png" width="123" height="45"><link>'
        '<br><img src="p1-image-01.png" width="67" height="89"><link>uff'
    )


def test_recap_img():
    html = ("""<br><img alt='image.png' src='https://wwwpy.dev/1' width='123' height="45"><link>"""
            """<br><img alt='image.png' src='https://wwwpy.dev/2' width="67" height='89'><link>uff""")

    target = FixImg(html, 'p1-')
    recap_img_html = target.recap_img_html

    assert """<img src="https://wwwpy.dev/1" alt="p1-image-00.png" width="123" height=45">""" in recap_img_html
    assert """<img src="https://wwwpy.dev/2" alt="p1-image-01.png" width="67" height=89">""" in recap_img_html