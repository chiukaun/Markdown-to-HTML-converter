
import os
import markdown
from PIL import Image
from caption import ImageCaptionExtension
import shutil
import datetime
import nltk
import re


def extract_image_paths(filename):  # Only for metadata purpose
    # Open the markdown file
    with open(filename, "r") as file:
        markdown_text = file.read()
        

    # Replace relative path to absolute, and "%20" to space
    markdown_text = markdown_text.replace("../005-Files", "/Users/chiukaun/Documents/Combogic-Blog-git/005-Files")
    markdown_text = markdown_text.replace("%20", " ")

    # Split the markdown text by lines
    markdown_lines = markdown_text.splitlines()

    # Extract the image paths from the markdown lines
    image_paths = []
    for line in markdown_lines:
        if line.startswith("!"):
            # Extract the path from the image syntax
            path_start = line.find("(") + 1
            path_end = line.find(")")
            image_path = line[path_start:path_end]
            print("found image: " + image_path)
            image_paths.append(image_path)

    # Return the list of image paths
    return image_paths

# Convert all images in file to webp and make a folder on Desktop
def convert_to_webp(filename):
    # Open the markdown file
    with open(filename, "r") as file:
        markdown_text = file.read()

    # Replace relative path to absolute, "%20" to space, make it to lines. 
    markdown_text = markdown_text.replace("../005-Files", "/Users/chiukaun/Documents/Combogic-Blog-git/005-Files")
    markdown_text = markdown_text.replace("%20", " ")
    markdown_lines = markdown_text.splitlines()

    # Extract the image paths from the markdown lines
    image_paths = []
    for line in markdown_lines:
        if line.startswith("!"):
            # Extract the path from the image syntax
            path_start = line.find("(") + 1
            path_end = line.find(")")
            image_path = line[path_start:path_end]
            print(image_path)
            image_paths.append(image_path)

    image_names = []
    for line in markdown_lines:
        if line.startswith("!"):
            # Extract alt text as image name.
            path_start = line.find("[") + 1
            path_end = line.find("]")
            image_name = line[path_start:path_end]
            image_names.append(image_name)

    # Make directory in desired path: ************** set in desktop for testing
    destination = f"/Users/chiukaun/Desktop/{os.path.splitext(os.path.split(filename)[1])[0]}"
    os.mkdir(destination)

    # Convert image to WebP format and make a copy to destination
    for i, image in enumerate(image_paths):
        im = Image.open(image)
        rename = image_names[i] + ".webp"
        source_file = os.path.join(os.path.split(image)[0], rename)
        im.save(source_file, "webp")
        image_name = os.path.split(source_file)[1]
        destination_file = os.path.join(destination, image_name)
        shutil.copyfile(source_file, destination_file)
        print(f"source_file:{source_file}, destination_file:{destination_file}, saved.")
    
    # Replace any image format names to webp and write it back
    j = 0
    for i, line in enumerate(markdown_lines):
        if line.startswith("!"):
            line = line.replace("/Users/chiukaun/Documents/Combogic-Blog-git/005-Files", "../005-Files")
            line = line.replace(" ", "%20")
            path_start = line.find("(") + 1
            path_end = line.find(")")
            image_path = line[path_start:path_end]
            rename2 = image_names[j] + ".webp"
            webp_path_md = os.path.join(os.path.split(image_path)[0], rename2)
            markdown_lines[i] = re.sub(r'\(.*?\)', f'({webp_path_md})', line)
            j += 1
    markdown_content = '\n'.join(markdown_lines)
    with open(filename, "w") as file:
        file.write(markdown_content)


# Convert Markdown to HTML
def convert_markdown_to_html(filename):
    # Read markdown file
    file_NAME = os.path.splitext(os.path.split(filename)[1])[0]
    with open(filename, 'r') as f:
        markdown_content = f.read()
        markdown_content = markdown_content.replace("%20", " ")

    # Convert markdown to html using
    html_content = markdown.markdown(markdown_content, extensions=[ImageCaptionExtension()])
    with open("/Users/chiukaun/Desktop/raw_content.html", "w") as f:
        f.write(html_content)
    
    # Replace path
    html_content = html_content.replace("../005-Files/", f"/img/blog/{file_NAME}/")    

    # Get metadata
    cover_image_url = ""
    html_lines = html_content.splitlines()
    for line in html_lines:
        if line.startswith("<h1>"):
            start = line.find("<h1>") + 4
            end = line.find("</h1>")
            title = line[start:end]
            break
            
        if line.startswith("https://"):
            start_link = line.find('https://')
            end_link = line.find('<figcaption>', start_link)  # Find the next double-quote after the start_link position
            cover_image_url = line[start_link:end_link]
            print(cover_image_url)
            break
    
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    image_paths = extract_image_paths(filename)
    print(image_paths)
    cover_image_path = f"/img/blog/{file_NAME}/{os.path.split(image_paths[0])[1]}"

    # Clean up image link formats
    for i, line in enumerate(html_lines):
        if line.startswith("https://"):
            start_link = line.find('https://')
            end_link = line.find('<figcaption>', start_link)  # Find the next double-quote after the start_link position
            image_url = line[start_link:end_link]
            html_lines[i] = f"<figcaption><a href='{image_url}'>圖片來源</a></figcaption>"                                            
    
    # Trim out h1 and cover photo: the first five lines
    html_lines = html_lines[5:]
    html_content = '\n'.join(html_lines)


    # Duplicate template to write in
    source_file = "/Users/chiukaun/Desktop/pthon_scripts/Markdown-to-HTML-converter/template.html"
    duplicate_file = f"/Users/chiukaun/Desktop/{file_NAME}.html"                #### Duplicate path
    shutil.copyfile(source_file, duplicate_file)

    # Write html content to file
    with open(duplicate_file, 'r+') as f:
        template = f.read()
        template = template.replace("****這邊輸入標題", title)
        template = template.replace("2023-1-11", date_string)
        template = template.replace("/img/blog/封面圖片.jpg", cover_image_path)
        template = template.replace("****for SEO的描述", "summary")
        template = template.replace("https://google.com", cover_image_url)
        template = template.replace("    <!-- ****** TEXT HERE ****** -->", html_content)

    with open(duplicate_file, 'w') as f:
        f.write(template + "\n")

file = input("Enter file path: ").strip("'")
convert_to_webp(file)
convert_markdown_to_html(file)

