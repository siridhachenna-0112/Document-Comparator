import os
import zipfile
import xml.etree.ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/"
         "wordprocessingml/2006/main"
}


def read_txt_file(file_path):

    with open(file_path, "r", encoding="utf-8",
              errors="replace") as file:
        return file.read()


def read_docx_file(file_path):

    lines = []

    with zipfile.ZipFile(file_path, "r") as archive:

        xml_content = archive.read("word/document.xml")
        root = ET.fromstring(xml_content)

        body = root.find("w:body", NS)

        for element in body:

            tag = element.tag.split("}")[-1]

            if tag == "p":

                text = "".join(
                    node.text or ""
                    for node in element.findall(".//w:t", NS)
                )

                lines.append(text)

            elif tag == "tbl":

                for row in element.findall("w:tr", NS):

                    cells = []

                    for cell in row.findall("w:tc", NS):

                        cell_text = "".join(
                            node.text or ""
                            for node in cell.findall(".//w:t", NS)
                        )

                        cells.append(cell_text.strip())

                    lines.append(" | ".join(cells))

    return "\n".join(lines)


def read_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return read_txt_file(file_path)

    elif extension == ".docx":
        return read_docx_file(file_path)

    else:
        raise ValueError("Unsupported file type")


def extract_docx_images(file_path, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    extracted_images = []

    with zipfile.ZipFile(file_path, "r") as archive:

        for filename in archive.namelist():

            if filename.startswith("word/media/"):

                image_name = os.path.basename(filename)

                if not image_name:
                    continue

                output_path = os.path.join(
                    output_folder, image_name
                )

                with open(output_path, "wb") as output_file:

                    output_file.write(archive.read(filename))

                extracted_images.append(output_path)

    return extracted_images
