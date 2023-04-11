
import os
import markdown
from PIL import Image
from caption import ImageCaptionExtension
import shutil
import datetime
import nltk
import re

# import openai
# import tiktoken 
# import constant
# openai.api_key = constant.api_key  

def extract_image_paths(filename):  # Only for metadata purpose
    # Open the markdown file
    with open(filename, "r") as file:
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
            print(image_path)
            image_paths.append(image_path)

    # Return the list of image paths
    return image_paths

# Get all image paths
def convert_to_webp(filename):
    # Open the markdown file
    with open(filename, "r") as file:
        markdown_text = file.read()

    # Replace relative path to absolute, "%20" to space
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

    # Make directory in desired path: ************** It's set in desktop for testing
    destination = f"/Users/chiukaun/Desktop/{os.path.splitext(os.path.split(filename)[1])[0]}"
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
    
    # Replace any image format names to webp and write it back

    for i, line in enumerate(markdown_lines):
        if line.startswith("!"):
            line = line.replace("/Users/chiukaun/Documents/Combogic-Blog-git/005-Files", "../005-Files")
            line = line.replace(" ", "%20")
            path_start = line.find("(") + 1
            path_end = line.find(")")
            image_path = line[path_start:path_end]
            webp_path_md = os.path.splitext(image_path)[0] + ".webp"
            markdown_lines[i] = re.sub(r'\(.*?\)', f'({webp_path_md})', line)
    markdown_content = '\n'.join(markdown_lines)
    with open(filename, "w") as file:
        file.write(markdown_content)


# Convert Markdown to HTML
def convert_markdown_to_html(filename):
    # Read markdown file
    file_NAME = os.path.splitext(os.path.split(filename)[1])[0]
    with open(filename, 'r') as f:
        markdown_content = f.read()

    # Convert markdown to html using
    html_content = markdown.markdown(markdown_content, extensions=[ImageCaptionExtension()])
    with open("/Users/chiukaun/Desktop/raw_content.html", "w") as f:
        f.write(html_content)
    
    # Replace path
    html_content = html_content.replace("../005-Files/", f"/img/blog/{file_NAME}/")

    # Generate a general description of this article using openAI API (currently closed)
    # def split_text(text):
    #     """Splitting text base on max_chunk_size"""
    #     max_token_size = 2000
    #     chunks = []
    #     current_chunk = ""

    #     # Tokenize the input text into sentences
    #     sentences = text.split("。")   # Chinese period
        
    #     for sentence in sentences:
    #         # Add the sentence to the current chunk if it's not too big
    #         if len(sentence) < max_token_size:
    #             current_chunk += sentence
    #         else:
    #             # Add the current chunk to the list of chunks and start a new one
    #             chunks.append(current_chunk.strip())
    #             current_chunk = sentence
        
    #     # Add any remaining text as a final chunk
    #     if current_chunk:
    #         chunks.append(current_chunk.strip())
    #     print(chunks)
    #     return chunks
    # def generate_summary(text):
    #     """Generate summary by while-looping chunks of text to GPT-3.5 to form summarization"""
    #     token_total = 0
    #     while len(tiktoken.get_encoding("gpt2").encode(text)) > 4000:    # Get token length with tiktoken
    #         input_chunks = split_text(text)   # Split text by 4080 tokens
    #         print("Summarize start, there are {} chunks to summarize.".format(len(input_chunks)))
    #         output_chunks = []
    #         for i, chunk in enumerate(input_chunks):
    #             token_count = len(tiktoken.get_encoding("gpt2").encode(chunk))   # count token usage
    #             print("Summarizing, token used in this round: {}".format(token_count))
    #             response = openai.ChatCompletion.create(
    #                         model="gpt-3.5-turbo",
    #                         messages=[ 
    #                         {"role": "system", "content": "you are a helpful assistant who provides deep insight and skilled at writing SEO content in Traditional Chinese"}, 
    #                         {"role": "user", "content": "Your task is to analyze the text I give you generate a brief while engaging summary for article preview. This summary must engage the readers. You must write in Tradional Chinese. This summary must be less than 100 words. Do not mention that it's a HTML content. Do not report anything unrelated to the subject of article. Your job is to make the summary as engaging as possible. You should generate the summary from the following text: {}".format(chunk)} ]
    #                     )
    #             summary = response["choices"][0]["message"]["content"]
    #             output_chunks.append(summary)
    #             text = " ".join(output_chunks)  
    #             token_total += token_count
    #             print("chunk{0} summarized.".format(i))
    #     print("Summary generized.")
    #     return text 

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

    
    # summary = generate_summary(html_content)                                                    #### Currently not working due to length issue
    
    # Trim out h1 and cover photo: the first six lines

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

