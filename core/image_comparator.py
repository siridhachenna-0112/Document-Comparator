import os
import hashlib

from PIL import Image, ImageChops


def file_hash(file_path):

    sha = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


def image_similarity(image1_path, image2_path):

    try:

        image1 = Image.open(
            image1_path
        ).convert("RGB")

        image2 = Image.open(
            image2_path
        ).convert("RGB")

        # Resize second image if dimensions differ
        if image1.size != image2.size:

            image2 = image2.resize(
                image1.size
            )

        difference = ImageChops.difference(
            image1,
            image2
        )

        histogram = difference.histogram()

        total_pixels = (
            image1.size[0] *
            image1.size[1]
        )

        if total_pixels == 0:
            return 100.0

        difference_sum = sum(
            value * (index % 256)
            for index, value
            in enumerate(histogram)
        )

        max_difference = (
            total_pixels *
            3 *
            255
        )

        similarity = (
            1 -
            difference_sum /
            max_difference
        ) * 100

        similarity = max(
            0,
            min(100, similarity)
        )

        return round(
            similarity,
            2
        )

    except Exception:
        return 0.0


def compare_image_folders(
    folder1,
    folder2
):

    images1 = {}

    images2 = {}

    for filename in os.listdir(folder1):

        path = os.path.join(
            folder1,
            filename
        )

        if os.path.isfile(path):

            images1[filename] = path

    for filename in os.listdir(folder2):

        path = os.path.join(
            folder2,
            filename
        )

        if os.path.isfile(path):

            images2[filename] = path

    all_names = sorted(
        set(images1.keys()) |
        set(images2.keys())
    )

    results = []

    for name in all_names:

        if name in images1 and name in images2:

            hash1 = file_hash(
                images1[name]
            )

            hash2 = file_hash(
                images2[name]
            )

            if hash1 == hash2:

                results.append({
                    "image": name,
                    "status": "SAME",
                    "similarity": 100.0,
                    "file1": images1[name],
                    "file2": images2[name]
                })

            else:

                similarity = image_similarity(
                    images1[name],
                    images2[name]
                )

                results.append({
                    "image": name,
                    "status": "MODIFIED",
                    "similarity": similarity,
                    "file1": images1[name],
                    "file2": images2[name]
                })

        elif name in images1:

            results.append({
                "image": name,
                "status": "DELETED",
                "similarity": 0.0,
                "file1": images1[name],
                "file2": None
            })

        else:

            results.append({
                "image": name,
                "status": "ADDED",
                "similarity": 0.0,
                "file1": None,
                "file2": images2[name]
            })

    return results