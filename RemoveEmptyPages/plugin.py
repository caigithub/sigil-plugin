# plugin.py  –  Remove Empty Pages  (early-exit DOM edition)
# -----------------------------------------------------------
# Edit-type plugin for Sigil.
# Parses each XHTML to a DOM and deletes the file if body.textContent
# contains only white-space.

from lxml import etree as element_tree

XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"


def body_contains_visible_text(body_element) -> bool:
    if (body_element.text or "").strip():
        return True

    for descendant_node in body_element.iter():
        if (descendant_node.text or "").strip():  # text inside tag
            return True
        if (descendant_node.tail or "").strip():  # text after tag
            return True

    return False


def run(book_container):
    """
    Sigil entry point.
    book_container gives access to the EPUB.
    Return 0 to commit changes, anything else rolls back.
    """
    removed_count = 0

    for manifest_id, href_attribute in book_container.text_iter():
        try:
            file_bytes = book_container.readfile(manifest_id)
            if not file_bytes:
                continue
            file_bytes = file_bytes.encode("utf-8")

            parser = element_tree.HTMLParser(
                recover=True, no_network=True, huge_tree=False
            )
            document = element_tree.fromstring(file_bytes, parser)

            body_element = document.find("body")
            if body_element is None:
                book_container.deletefile(manifest_id)
                removed_count += 1
                print(f"Remove page, no body : {href_attribute}  (id={manifest_id})")
                continue

            if body_contains_visible_text(body_element):
                continue

            book_container.deletefile(manifest_id)
            removed_count += 1
            print(
                f"Remove page, no text content : {href_attribute}  (id={manifest_id})"
            )

        except Exception as e:
            print(
                f"Error processing file {href_attribute} (id={manifest_id}): {str(e)}"
            )
            continue

    # Report
    if removed_count:
        print(f"\nTotal empty pages removed: {removed_count}")
    else:
        print("No empty pages found.")

    return 0
