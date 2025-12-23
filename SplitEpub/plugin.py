import os
import tempfile
from pathlib import Path
from sigil_bs4 import BeautifulSoup
from epub_utils import unzip_epub_to_dir, epub_zip_up_book_contents

SPLITTER = "file_splitter"


def run(book_container):
    vol_id_2_href_list = {}
    vol_idx = 1
    print(f"volumn {vol_idx}")
    for mid, href in book_container.text_iter():
        html_bytes = book_container.readfile(mid)
        soup = BeautifulSoup(html_bytes, "lxml-xml")

        is_split_here = bool(soup.find("hr", class_=SPLITTER))
        if is_split_here:
            vol_idx += 1
            print(f"volumn {vol_idx}")

        vol_id_2_href_list.setdefault(vol_idx, []).append(href)

        print(f"\t {href}")

    epub_path = book_container.get_epub_filepath()
    base_name = os.path.splitext(os.path.basename(epub_path))[0]
    output_folder = os.path.dirname(epub_path)

    for new_vol, new_vol_pages_href in vol_id_2_href_list.items():
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            print(f"{new_vol} create temp {tmp_path}")

            unzip_epub_to_dir(epub_path, tmp_dir)

            for remove_vol, pages_to_remove in vol_id_2_href_list.items():
                if remove_vol == new_vol:
                    continue
                for href in pages_to_remove:
                    file_path = tmp_path / "EPUB" / href
                    if file_path.exists():
                        file_path.unlink()

            out_epub = os.path.join(output_folder, f"{base_name}_Vol{new_vol}.epub")
            epub_zip_up_book_contents(tmp_dir, out_epub)
            print(f"{new_vol} create epub {out_epub}")

    print(f"\nFinished: {len(vol_id_2_href_list)} volumes created.")
    return 0
