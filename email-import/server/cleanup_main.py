import shutil
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
from turtledemo.sorting_animate import isort

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
            generated_item = Path(cleanup_tmp) / item.name
            generated_item.write_text(fix_img.new_html)
            generate_markdown(generated_item)
            if fix_img.recap_img_html:
                generated_item.with_suffix('.img-recap.html').write_text(fix_img.recap_img_html)

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

def generate_markdown(item: Path):
    markdown_folder = item.parent / 'markdown'
    markdown_folder.mkdir(exist_ok=True)
    markdown_file = markdown_folder / (item.stem + '.html')
    year = 2025
    week = int(item.stem.split('-')[2])
    isoweekday = 1 # 0 means Sunday
    date = datetime.fromisocalendar(year, week, isoweekday).date()
    markdown_content = f"""Title: #title
Date: #date
Category: Weekly planning
"""
    # date is in ISO format YYYY-MM-DD
    # title is `Week {week} plan`
    markdown_content = markdown_content.replace('#title', f'Week {week:0>2} plan')
    markdown_content = markdown_content.replace('#date', date.isoformat())
    markdown_file.write_text(markdown_content + '\n\n' + item.read_text())


if __name__ == '__main__':
    main()
