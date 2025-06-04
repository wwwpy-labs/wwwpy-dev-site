# language=html
from dataclasses import dataclass, field

from common.fix_img import FixImg, Link

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

    assert target.links == [
        Link('p1-image-00.png'),
        Link('p1-logger-levels.gif'),
        Link('p1-image-01.png'),
    ]
