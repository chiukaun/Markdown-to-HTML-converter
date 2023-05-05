
import os
import markdown
from PIL import Image
from caption import ImageCaptionExtension
import shutil
import datetime
import nltk
import re
from bs4 import BeautifulSoup

import openai
import tiktoken 
import constant
openai.api_key = constant.api_key  

# def extract_image_paths(filename):
#     # Open the markdown file
#     with open(filename, "r") as file:
#         markdown_text = file.read()
        

#     # Replace relative path to absolute, "%20" to space
#     markdown_text = markdown_text.replace("../005-Files", "/Users/chiukaun/Documents/Combogic-Blog-git/005-Files")
#     markdown_text = markdown_text.replace("%20", " ")

#     # Split the markdown text by lines
#     markdown_lines = markdown_text.splitlines()

#     # Extract the image paths from the markdown lines
#     image_paths = []
#     for line in markdown_lines:
#         if line.startswith("!"):
#             # Extract the path from the image syntax
#             path_start = line.find("(") + 1
#             path_end = line.find(")")
#             image_path = line[path_start:path_end]
#             print(image_path)
#             image_paths.append(image_path)

#     # Return the list of image paths
#     return image_paths

# def convert_to_webp(filename):
#     # Open the markdown file
#     with open(filename, "r") as file:
#         markdown_text = file.read()

#     # Replace relative path to absolute, "%20" to space
#     markdown_text = markdown_text.replace("../005-Files", "/Users/chiukaun/Documents/Combogic-Blog-git/005-Files")
#     markdown_text = markdown_text.replace("%20", " ")
#     markdown_lines = markdown_text.splitlines()

#     # Extract the image paths from the markdown lines
#     image_paths = []
#     for line in markdown_lines:
#         if line.startswith("!"):
#             # Extract the path from the image syntax
#             path_start = line.find("(") + 1
#             path_end = line.find(")")
#             image_path = line[path_start:path_end]
#             print(image_path)
#             image_paths.append(image_path)

#     # Make directory in desired path: ************** It's set in desktop for testing
#     destination = f"/Users/chiukaun/Desktop/{os.path.splitext(os.path.split(filename)[1])[0]}"
#     os.mkdir(destination)

#     # Convert image to WebP format and make a copy to destination
#     for image in image_paths:
#         im = Image.open(image)
#         source_file = os.path.splitext(image)[0] + ".webp"
#         im.save(source_file, "webp")
#         image_name = os.path.split(source_file)[1]
#         destination_file = os.path.join(destination, image_name)
#         shutil.copyfile(source_file, destination_file)
#         print(f"source_file:{source_file}, destination_file:{destination_file}, saved.")
#         os.remove(image)
    
#     # Replace any image format names to webp and write it back

#     for i, line in enumerate(markdown_lines):
#         if line.startswith("!"):
#             line = line.replace("/Users/chiukaun/Documents/Combogic-Blog-git/005-Files", "../005-Files")
#             line = line.replace(" ", "%20")
#             path_start = line.find("(") + 1
#             path_end = line.find(")")
#             image_path = line[path_start:path_end]
#             webp_path_md = os.path.splitext(image_path)[0] + ".webp"
#             markdown_lines[i] = re.sub(r'\(.*?\)', f'({webp_path_md})', line)
#     markdown_content = '\n'.join(markdown_lines)
#     with open(filename, "w") as file:
#         file.write(markdown_content)



# file = input("Enter file path: ").strip("'")
# convert_to_webp(file)


# # Define input and output paths
# input_path = "/path/to/markdown/file.md"
# output_dir = "/Users/username/Desktop/"

# # Define regular expression to match image references in markdown
# img_pattern = r"!\[(.*)\]\((.*)\)"

# # Load markdown file
# with open(input_path, "r") as f:
#     markdown_text = f.read()

# # Convert all referenced images to .webp format and rename them to alt text
# for match in re.finditer(img_pattern, markdown_text):
#     alt_text = match.group(1)
#     img_path = match.group(2)
#     img_name = os.path.basename(img_path)
#     img_name_without_ext, img_ext = os.path.splitext(img_name)
#     output_name = alt_text + ".webp"
#     output_path = os.path.join(output_dir, output_name)
#     with Image.open(img_path) as img:
#         img.save(output_path, "webp")
#     markdown_text = markdown_text.replace(img_path, output_name)
#     os.rename(img_path, os.path.join(os.path.dirname(img_path), alt_text + img_ext))

# # Write updated markdown file to output directory
# output_path = os.path.join(output_dir, os.path.basename(input_path))
# with open(output_path, "w") as f:
#     f.write(markdown_text)



# Get all image paths
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
        source_file = os.path.split(image)[0] + image_names[i] + ".webp"
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
            webp_path_md = os.path.split(image_path)[0] + image_names[i] + ".webp"
            markdown_lines[i] = re.sub(r'\(.*?\)', f'({webp_path_md})', line)
    markdown_content = '\n'.join(markdown_lines)
    with open(filename, "w") as file:
        file.write(markdown_content)

file = input("Enter file path: ").strip("'")
convert_to_webp(file)





def split_text(text):
        """Splitting text base on max_chunk_size"""
        max_token_size = 2000
        chunks = []
        current_chunk = ""

        # Tokenize the input text into sentences
        sentences = nltk.sent_tokenize(text)  
        
        for sentence in sentences:
            # Add the sentence to the current chunk if it's not too big
            if len(sentence) < max_token_size:
                current_chunk += sentence
            else:
                # Add the current chunk to the list of chunks and start a new one
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add any remaining text as a final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        print(chunks)
        return chunks
def generate_summary(text):
    """Generate summary by while-looping chunks of text to GPT-3.5 to form summarization"""
    token_total = 0
    while len(text) > 2000:    # Get token length with tiktoken
        input_chunks = split_text(text)   # Split text by 1000 characters
        print(f"Summarize start, there are {len(input_chunks)} chunks to summarize.")
        output_chunks = []
        for i, chunk in enumerate(input_chunks):
            token_count = len(tiktoken.get_encoding("gpt2").encode(chunk))   # count token usage
            print(f"Summarizing, token used in this round: {token_count}")
            response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[ 
                        {"role": "system", "content": "you are a helpful assistant who's skilled at writing in Traditional Chinese"}, 
                        {"role": "user", "content": "Your task is to analyze the text I give you generate a brief while engaging summary for article preview. This summary must engage the readers. You must write in Tradional Chinese. This summary must be less than 100 words. Do not mention that it's a HTML content. Do not report anything unrelated to the subject of article. Your job is to make the summary as engaging as possible. You should generate the summary from the following text: {}".format(chunk)} ]
                    )
            summary = response["choices"][0]["message"]["content"]
            output_chunks.append(summary)
            text = " ".join(output_chunks)  
            token_total += token_count
            print("chunk{0} summarized.".format(i))
    print("Summary generized.")
    return text 

soup = BeautifulSoup(html_content, 'html.parser')
html_text = soup.get_text()
summary = generate_summary(html_text)