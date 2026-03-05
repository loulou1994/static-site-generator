import os
import shutil

from block_markdown import markdown_to_html_node, extract_title


def source_to_target(source, target):
    root_dir = os.getcwd()

    try:
        abs_source = os.path.abspath(os.path.join(root_dir, source))
        abs_target = os.path.abspath(os.path.join(root_dir, target))

        if not abs_source.startswith(root_dir) or not abs_target.startswith(root_dir):
            return "Error: Not allowed to copy outside root directory"

        if not os.path.exists(abs_source):
            return "Error: Source does not exist"

        if os.path.exists(abs_target):
            shutil.rmtree(abs_target)

        os.mkdir(abs_target)

        if os.path.isfile(abs_source):
            shutil.copy(abs_source, abs_target)
            return

        files = os.listdir(abs_source)

        for file in files:
            nested_source = f"{abs_source}/{file}"
            nested_target = f"{target}/{file}"

            if os.path.isfile(nested_source):
                shutil.copy(nested_source, target)
                continue

            source_to_target(nested_source, nested_target)

    except Exception as e:
        return f"Error happened while copying source file: {str(e)}"


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        print("Error: something occured while processing file " + str(e))


def write_file(file_path: str, text: str):
    try:
        with open(file_path, "w") as file:
            file.write(text)

    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error occured: {e}")


def generate_page(from_path, template_path, dest_path, base_url):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = read_file(from_path)
    html_template = read_file(template_path)
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    if html_string is None or html_template is None:
        raise Exception("couldn't process files")

    full_html = html_template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_string)
    full_html = full_html.replace("href=\"/", f"href=\"{base_url}")
    full_html = full_html.replace("src=\"/", f"src=\"{base_url}")

    write_file(dest_path, full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_url):
    root_dir = os.getcwd()

    try:
        abs_dir_path_src = os.path.abspath(os.path.join(root_dir, dir_path_content))
        abs_dir_path_dest = os.path.abspath(os.path.join(root_dir, dest_dir_path))
        abs_tmplt_path = os.path.abspath(os.path.join(root_dir, template_path))

        if (
            not abs_dir_path_src.startswith(root_dir)
            or not abs_dir_path_dest.startswith(root_dir)
            or not abs_tmplt_path.startswith(root_dir)
        ):
            raise Exception("Error: Not allowed to copy outside root directory")

        if (
            not os.path.exists(abs_dir_path_src)
            or not os.path.exists(abs_dir_path_dest)
            or not os.path.exists(template_path)
        ):
            raise Exception("Error: Source or Dest or Template html do not exist")

        files = os.listdir(dir_path_content)

        for file in files:
            nested_source = f"{abs_dir_path_src}/{file}"
            nested_target = f"{abs_dir_path_dest}/{os.path.splitext(file)[0]}"

            if os.path.isfile(nested_source):
                generate_page(nested_source, abs_tmplt_path, f"{nested_target}.html", base_url)
                continue

            os.mkdir(nested_target)
            generate_pages_recursive(nested_source, abs_tmplt_path, nested_target, base_url)

    except Exception as e:
        print(f"Couldn't process page generation -> {e}")
