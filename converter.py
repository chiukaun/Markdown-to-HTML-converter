
import os
import markdown
from PIL import Image
from caption import ImageCaptionExtension
import shutil
import datetime

# Get all image paths
def extract_image_paths(markdown_file):
    # Open the markdown file
    with open(markdown_file, "r") as file:
        # Read the contents of the file into a string
        markdown_text = file.read()

    # Replace relative path to absolute, "%20" to space
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
            image_paths.append(image_path)

    # Return the list of image paths
    return image_paths


# Convert all images to webp inplace and make a copy in designated path
def convert_to_webp(markdown_file):
    # Open image file
    image_paths = extract_image_paths(markdown_file)
    cover_image_path = f"/Users/chiukaun/Desktop/{markdown_file}/{os.path.split(image_paths[0])[1]}"

    # Make directory in desired path: ************** It's set in desktop for testing
    destination = f"/Users/chiukaun/Desktop/{markdown_file}"
    os.mkdir(destination)

    # Convert image to WebP format and make a copy to destination
    for image in image_paths:
        im = Image.open(image)
        source_file = os.path.splitext(image)[0] + ".webp"
        im.save(source_file, "webp")
        image_name = os.path.split(source_file)[1]
        destination_file = os.path.join(destination, image_name)
        shutil.copyfile(source_file, destination_file)
        print(f"source_file:{source_file}, destination_file:{destination_file}, saved.")
        
# Convert Markdown to HTML
def convert_markdown_to_html(filename):
    # Read markdown file
    with open(filename, 'r') as f:
        markdown_content = f.read()

    # Convert markdown to html
    html_content = markdown.markdown(markdown_content, extensions=[ImageCaptionExtension()])

    # Replace path
    html_content = html_content.replace("../005-Files/", f"/img/blog/{filename}/")

    # Generate a general description of this article using openAI API
    import openai
    import constant
    openai.api_key = constant.api_key 
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[ 
                {"role": "system", "content": "you are a helpful assistant who provides deep insight and skilled at writing SEO content in Traditional Chinese"}, 
                {"role": "user", "content": "Your task is to analyze the text I give you generate a brief while engaging summary for article preview. This summary must engage the readers. Do not mention that it's a HTML content. Do not report anything unrelated to the subject of article. Your job is to make the summary as engaging as possible. You should generate the summary from the following text: {}".format(html_content)} ]
            )
    summary = response["choices"][0]["message"]["content"]

    # Get metadata
    html_lines = html_content.splitlines()
    for line in html_lines:
        if line.startswith("<h1>"):
            # Extract the path from the image syntax
            start = line.find("<h1>") + 4
            end = line.find("</h1>")
            title = line[start:end]
        
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    image_paths = extract_image_paths(filename)
    cover_image_path = f"/Users/chiukaun/Desktop/{filename}/{os.path.split(image_paths[0])[1]}"
    
    # Trim out h1 and cover photo




    # Duplicate template to write in
    source_file = "/Users/chiukaun/Desktop/pthon_scripts/artice_uploader/template.html"
    duplicate_file = f"/Users/chiukaun/Desktop/{os.path.splitext(filename)[0]}.html"
    shutil.copyfile(source_file, duplicate_file)

    # Write html content to file
    with open(duplicate_file, 'r') as f:
        template = f.read()
        template = template.replace("****這邊輸入標題", title)
        template = template.replace("2023-1-11", date_string)
        template = template.replace("/img/blog/封面圖片.jpg", cover_image_path)
        template = template.replace("****for SEO的描述", summary)

    with open(duplicate_file, "w") as f:
        f.write(template + "\n")
        f.write(html_content)
        f.write('{{/ content-ch }}')


# convert_to_webp("test.md")
convert_markdown_to_html("test.md")






# filename
# ![alt_text](../005-Files/1%201.webp)
# <p><img alt="alt_text" src="../005-Files/1%201.webp" /></p>

# 
#         <figure>
#             <img src="/img/blog/{filename}/{os.path.split(../005-Files/1%201.webp)[1]}" alt="{alt_text}">
#             <figcaption>{caption}</figcaption>
#         </figure>
# 