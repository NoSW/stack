import sys
import os
import shutil

if __name__ == '__main__':
    html_list = ""

    for file in os.popen("git diff-index --cached --name-only HEAD").read().splitlines():
        if file.endswith(".md"):
            html_file = f"{file}.html"
            shutil.copyfile(file, html_file)
            with open(html_file, 'a') as f:
                f.write("\n<style class=\"fallback\">body{visibility:hidden}</style><script>markdeepOptions={tocStyle:'long'};</script><!-- Markdeep: --><script src=\"https://casual-effects.com/markdeep/latest/markdeep.min.js?\" charset=\"utf-8\"></script>")
            html_list += f" {html_file} "

    if len(html_list) > 0:
        os.system(f"git add {html_list}")