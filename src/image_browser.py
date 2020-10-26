import xml.etree.ElementTree as ET
import typing
from collections import namedtuple

Coords = namedtuple("Coords", ["x_min", "y_min", "x_max", "y_max"])


def parse_single_image(image_path: str, annotations_path: str) -> typing.Generator:
    """
    Return list containing coordinates of all cells in a single image

    :param image_path: Path to image
    :param annotations_path: Path to annotations file
    :return: List of cell coordinates in the image
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()
    for cell in root.iter("bndbox"):
        yield Coords(
            cell.find("xmin").text,  # type: ignore
            cell.find("ymin").text,  # type: ignore
            cell.find("xmax").text,  # type: ignore
            cell.find("ymax").text,  # type: ignore
        )


if __name__ == "__main__":
    for cell in parse_single_image("", "/home/bazyli/projects/dataset_leukocytes/annotations_test/1_00002.xml"):
        print(f"x_min: {cell.x_min}, y_min: {cell.y_min}, x_max: {cell.x_max}, y_max: {cell.y_max}")
