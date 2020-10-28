import xml.etree.ElementTree as ET
import typing
from PIL import Image
from collections import namedtuple

Coords = namedtuple("Coords", ["x_min", "y_min", "x_max", "y_max"])
IMG_RESIZE = 3


def get_image_name(annotations_path: str) -> str:
    """
    Get path of the image included in annotations file

    :param annotations_path: Path of annotations file
    :return: Image name
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()
    return root.find("path").text


def parse_single_image(annotations_path: str) -> typing.Generator:
    """
    Return list containing coordinates of all cells in a single image from annotations file

    :param annotations_path: Path of annotations file
    :return: List of cell coordinates in the image
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()

    for bndbox in root.iter("bndbox"):
        yield Coords(
            int(bndbox.find("xmin").text),
            int(bndbox.find("ymin").text),
            int(bndbox.find("xmax").text),
            int(bndbox.find("ymax").text),
        )


def set_label(annotations_path: str, coords: Coords, label: str) -> ET.ElementTree:
    """
    Set label of the cell

    :param annotations_path: Path of annotations file
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
        int(candidate.find("xmin").text) == coords.x_min
        and int(candidate.find("xmax").text) == coords.x_max
        and int(candidate.find("ymin").text) == coords.y_min
        and int(candidate.find("ymax").text) == coords.y_max
    )
    return status


def crop_cell_from_image(img_path: str, coords: Coords) -> Image:
    """
    Return cropped cell from image

    :param img_path: Path of image
    :param coords: Coords of cell to be cropped
    :return: Cropped cell
    """
    img = Image.open(img_path)
    crop_rectangle = (coords.x_min, coords.y_min, coords.x_max, coords.y_max)
    cropped_img = img.crop(crop_rectangle)
    cropped_img = cropped_img.resize([int(IMG_RESIZE * dim) for dim in cropped_img.size], Image.ANTIALIAS)
    return cropped_img


if __name__ == "__main__":
    annotations_file = "/home/bazyli/projects/dataset_leukocytes/annotations_test/1_00002.xml"
    for coords in parse_single_image(annotations_file):
        set_label(annotations_file, coords, "dummy value").write(annotations_file)
        print(f"x_min: {coords.x_min}, y_min: {coords.y_min}, x_max: {coords.x_max}, y_max: {coords.y_max}")
