# plugin.py  –  Sigil 2.7  –  remove missing manifest items (API version)


def is_id_valid(book_container, id):
    try:
        book_container.readfile(id)
        return True
    except Exception:
        return False


def run(book_container):
    invalid_count = 0
    error_count = 0
    for mid, href, media_type in book_container.manifest_iter():
        print(f"[check] {media_type} {mid} = {href}")

        try:
            if not is_id_valid(book_container, mid):
                invalid_count += 1
                print("\tinvalid, try to remove")

                book_container.deletefile(mid)
        except Exception as e:
            error_count += 1
            print(f"\tError : {str(e)}")

    print(f"Total invalid : {invalid_count}")
    print(f"Total error: {error_count}")

    return 0
