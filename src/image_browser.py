import xml.etree.ElementTree as ET
import typing
from collections import namedtuple

Coords = namedtuple("Coords", ["x_min", "y_min", "x_max", "y_max"])


def parse_single_image(annotations_path: str) -> typing.Generator:
    """
    Return list containing coordinates of all cells in a single image from annotation file

    :param annotations_path: Path to annotations file
    :return: List of cell coordinates in the image
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()

    for bndbox in root.iter("bndbox"):
        yield Coords(
            bndbox.find("xmin").text, bndbox.find("ymin").text, bndbox.find("xmax").text, bndbox.find("ymax").text
        )


def set_label(annotations_path: str, coords: Coords, label: str) -> ET.ElementTree:
    """
    Set label of the cell

    :param annotations_path: Path to annotations file
    :param coords: Coordinates of cell to be labeled
    :param label: Label string
    :return: Modified XML Element Tree
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()
    for candidate_object in root.findall("object"):
        if compare_bndbox(candidate_object.find("bndbox"), coords):
            candidate_object.find("name").text = label
            return tree
    raise LookupError("Could not find cell with given coords")


def compare_bndbox(candidate: ET.Element, coords: Coords) -> bool:
    """
    Check if cadidate "object" XML element has same coords

    :param candidate: "object" XML element
    :param coords: Coords to match
    :return: True if matched, False otherwise
    """
    status = (
        candidate.find("xmin").text == coords.x_min
        and candidate.find("xmax").text == coords.x_max
        and candidate.find("ymin").text == coords.y_min
        and candidate.find("ymax").text == coords.y_max
    )
    return status


if __name__ == "__main__":
    annotations_file = "/home/bazyli/projects/dataset_leukocytes/annotations_test/1_00002.xml"
    for coords in parse_single_image(annotations_file):
        set_label(annotations_file, coords, "dummy value").write(annotations_file)
        print(f"x_min: {coords.x_min}, y_min: {coords.y_min}, x_max: {coords.x_max}, y_max: {coords.y_max}")
