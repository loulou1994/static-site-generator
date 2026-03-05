from utils import source_to_target, generate_page, generate_pages_recursive
import sys


def main():
    source_to_target("static", "docs")

    base_url = sys.argv[1] if len(sys.argv) > 1 else "/"

    generate_pages_recursive("./content", "./template.html", "./docs", base_url)
    # generate_page("./content/index.md", "./template.html", "./public/index.html")

main()