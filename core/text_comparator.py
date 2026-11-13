import difflib
import re

def split_lines(text):
    """
    Convert text into a list of lines.
    """

    return text.splitlines()


def calculate_similarity(text1, text2):
    """
    Calculate text similarity percentage.
    """

    matcher = difflib.SequenceMatcher(
        None,
        text1,
        text2
    )

    return round(
        matcher.ratio() * 100,
        2
    )


def compare_lines(text1, text2):

    lines1 = split_lines(text1)
    lines2 = split_lines(text2)

    matcher = difflib.SequenceMatcher(
        None,
        lines1,
        lines2
    )

    operations = []

    added = 0
    deleted = 0
    modified = 0
    unchanged = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":

            for index in range(i2 - i1):

                operations.append({
                    "type": "UNCHANGED",
                    "line1": i1 + index + 1,
                    "line2": j1 + index + 1,
                    "original": lines1[i1 + index],
                    "modified": lines2[j1 + index]
                })

                unchanged += 1

        elif tag == "delete":

            for index in range(i1, i2):

                operations.append({
                    "type": "DELETED",
                    "line1": index + 1,
                    "line2": "-",
                    "original": lines1[index],
                    "modified": ""
                })

                deleted += 1

        elif tag == "insert":

            for index in range(j1, j2):

                operations.append({
                    "type": "ADDED",
                    "line1": "-",
                    "line2": index + 1,
                    "original": "",
                    "modified": lines2[index]
                })

                added += 1

        elif tag == "replace":

            old_count = i2 - i1
            new_count = j2 - j1

            common_count = min(
                old_count,
                new_count
            )

            # Compare corresponding lines
            for index in range(common_count):

                operations.append({
                    "type": "MODIFIED",
                    "line1": i1 + index + 1,
                    "line2": j1 + index + 1,
                    "original": lines1[i1 + index],
                    "modified": lines2[j1 + index]
                })

                modified += 1

            # Remaining old lines = deleted
            if old_count > common_count:

                for index in range(
                    i1 + common_count,
                    i2
                ):

                    operations.append({
                        "type": "DELETED",
                        "line1": index + 1,
                        "line2": "-",
                        "original": lines1[index],
                        "modified": ""
                    })

                    deleted += 1

            # Remaining new lines = added
            if new_count > common_count:

                for index in range(
                    j1 + common_count,
                    j2
                ):

                    operations.append({
                        "type": "ADDED",
                        "line1": "-",
                        "line2": index + 1,
                        "original": "",
                        "modified": lines2[index]
                    })

                    added += 1

    similarity = calculate_similarity(
        text1,
        text2
    )

    return {
        "operations": operations,
        "similarity": similarity,
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "unchanged": unchanged
    }





def word_level_diff(old_text, new_text):

    old_matches = list(re.finditer(r'\S+', old_text))
    new_matches = list(re.finditer(r'\S+', new_text))

    old_words = [m.group() for m in old_matches]
    new_words = [m.group() for m in new_matches]

    matcher = difflib.SequenceMatcher(
        None,
        old_words,
        new_words,
        autojunk=False
    )

    operations = []

    added = 0
    deleted = 0
    modified = 0
    unchanged = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        old_start = old_matches[i1].start() if i1 < i2 else 0
        old_end = old_matches[i2 - 1].end() if i1 < i2 else 0

        new_start = new_matches[j1].start() if j1 < j2 else 0
        new_end = new_matches[j2 - 1].end() if j1 < j2 else 0

        original = old_text[old_start:old_end] if i1 < i2 else ""
        modified_text = new_text[new_start:new_end] if j1 < j2 else ""

        if tag == "equal":
            change_type = "UNCHANGED"
            unchanged += i2 - i1

        elif tag == "delete":
            change_type = "DELETED"
            deleted += i2 - i1

        elif tag == "insert":
            change_type = "ADDED"
            added += j2 - j1

        else:
            change_type = "MODIFIED"
            modified += max(i2 - i1, j2 - j1)

        operations.append({
            "type": change_type,
            "line1": old_text.count("\n", 0, old_start) + 1 if i1 < i2 else "-",
            "line2": new_text.count("\n", 0, new_start) + 1 if j1 < j2 else "-",
            "original": original,
            "modified": modified_text,
            "start1": old_start,
            "end1": old_end,
            "start2": new_start,
            "end2": new_end
        })

    similarity = difflib.SequenceMatcher(
        None,
        old_words,
        new_words,
        autojunk=False
    ).ratio() * 100

    return {
        "operations": operations,
        "similarity": round(similarity, 2),
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "unchanged": unchanged
    }