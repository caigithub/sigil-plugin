# Split EPUB
## Description
Cleanly divide one EPUB into several volumes with a single marker.
## Steps
- add `<hr class="file_splitter" />` into the pages
- run the plugin
## Example
- original epub :
    ```
        page 1
        page 2
        page 3 - contains <hr class="file_splitter" />
        page 4
        page 5 - contains <hr class="file_splitter" />
        page 6
    ```
- splitted epubs:
    ```
        volumn 1
            page 1
            page 2
        volumn 2
            page 3
            page 4
        volumn 3
            page 5
            page 6
    ```
## Contact
- github : https://github.com/caigithub/sigil-plugin
- email : caiaccount@163.com