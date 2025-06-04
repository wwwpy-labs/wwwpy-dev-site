# language=html

from common.fix_img import FixImg

html = """
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
    target = FixImg(html, 'p1-')

    only_new_alt = [link.new_alt for link in target.links]

    assert only_new_alt == [
        'p1-image-00.png',
        'p1-logger-levels.gif',
        'p1-image-01.png',
    ]


def test_src():
    target = FixImg(html, 'p1-')

    only_src = [link.src for link in target.links]

    assert only_src == [
        'https://wwwpy.dev/1',
        'https://wwwpy.dev/2',
        'https://wwwpy.dev/3',
    ]