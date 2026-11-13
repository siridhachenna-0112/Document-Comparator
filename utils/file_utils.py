import os


SUPPORTED_EXTENSIONS = [
    ".txt",
    ".docx"
]


def is_supported_file(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    return extension in SUPPORTED_EXTENSIONS


def get_file_name(file_path):

    return os.path.basename(
        file_path
    )


def get_file_extension(file_path):

    return os.path.splitext(
        file_path
    )[1].lower()