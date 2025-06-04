import shutil
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp

from common.cleanuplib import cleanup
from common.fix_img import FixImg


def main():
    uploads = (Path(__file__) / '../../uploads').resolve()
    cleanup_tmp = Path(mkdtemp(dir=uploads, prefix='cleanup-'))

    for item in uploads.glob('week-*.html'):
        if item.is_file():
            print(f'Cleaning {item}')
            content = item.read_text()
            clean_content = cleanup(content)
            fix_img = FixImg(clean_content, resource_prefix=item.stem + '--')
            item_tmp = Path(cleanup_tmp) / item.name
            item_tmp.write_text(fix_img.new_html)

    commit_folder(cleanup_tmp, uploads)


def commit_folder(cleanup_tmp, uploads):
    cleaned = uploads / 'cleaned'
    if cleaned.exists():
        cleaned_old = uploads / 'old'
        cleaned_old.mkdir(exist_ok=True)
        old_rename = 'cleaned_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        cleaned_old = cleaned_old / old_rename
        shutil.move(cleaned, cleaned_old)
    cleanup_tmp.rename(cleanup_tmp.with_name('cleaned'))


if __name__ == '__main__':
    main()
