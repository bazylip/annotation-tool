import xml.etree.ElementTree as ET
import typing
import os
import pathlib
import json
from PIL import Image, ImageDraw
from PIL import ImageFile
from collections import namedtuple

ImageFile.LOAD_TRUNCATED_IMAGES = True
Coords = namedtuple("Coords", ["x_min", "y_min", "x_max", "y_max"])

CONFIG_PATH = "configs/config.json"
with open(CONFIG_PATH, "r") as json_config:
    CONFIG = json.load(json_config)

TMP_IMG_NAME = CONFIG["TMP_IMG_NAME"]
ZOOM_SIZE = CONFIG["ZOOM_SIZE"]


def get_image_name(annotations_path: str) -> str:
    """
    Get path of the image included in annotations file

    :param annotations_path: Path of annotations file
    :return: Image name
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()
    return root.find("filename").text


def parse_single_annotations_file(annotations_path: str) -> typing.List[Coords]:
    """
    Return list containing coordinates of all cells in a single image from annotations file

    :param annotations_path: Path of annotations file
    :return: List of cell coordinates in the image
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()

    coords_list = []

    for bndbox in root.iter("bndbox"):
        coords_list.append(
            Coords(
                int(bndbox.find("xmin").text),
                int(bndbox.find("ymin").text),
                int(bndbox.find("xmax").text),
                int(bndbox.find("ymax").text),
            )
        )

    return coords_list


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


def get_label(annotations_path: str, coords: Coords) -> str:
    """
    Get label of the cell

    :param annotations_path: Path of annotations file
    :param coords: Coordinates of cell to be labeled
    :return: Cell label
    """
    tree = ET.parse(annotations_path)
    root = tree.getroot()
    for candidate_object in root.findall("object"):
        if compare_bndbox(candidate_object.find("bndbox"), coords):
            return candidate_object.find("name").text
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


def crop_cell_from_image(
    img_path: str, coords: Coords, tmp_directory_path: pathlib.Path, resize: float = 1.5, zoom: bool = False
) -> Image:
    """
    Return cropped cell from image

    :param img_path: Path of image
    :param coords: Coords of cell to be cropped
    :param tmp_directory_path: Path to save tmp image
    :param resize: Resize factor to make picture bigger/smaller
    :return: Cropped cell
    """
    img = Image.open(img_path)
    img_width, img_height = img.size
    if zoom:
        x_min = max(coords.x_min - ZOOM_SIZE, 0)
        y_min = max(coords.y_min - ZOOM_SIZE, 0)
        x_max = min(coords.x_max + ZOOM_SIZE, img_width)
        y_max = min(coords.y_max + ZOOM_SIZE, img_height)
        crop_rectangle = (x_min, y_min, x_max, y_max)
    else:
        crop_rectangle = (coords.x_min, coords.y_min, coords.x_max, coords.y_max)

    cropped_img = img.crop(crop_rectangle)

    if zoom:
        draw_img = ImageDraw.Draw(cropped_img)
        crop_width, crop_height = cropped_img.size

        x_min = ZOOM_SIZE if coords.x_min - ZOOM_SIZE >= 0 else coords.x_min
        y_min = ZOOM_SIZE if coords.y_min - ZOOM_SIZE >= 0 else coords.y_min
        x_max = (
            crop_width - ZOOM_SIZE if coords.x_max + ZOOM_SIZE <= img_width else x_min + (coords.x_max - coords.x_min)
        )
        y_max = (
            crop_height - ZOOM_SIZE
            if coords.y_max + ZOOM_SIZE <= img_height
            else y_min + (coords.y_max - coords.y_min)
        )

        shape = [(x_min, y_min), (x_max, y_max)]
        draw_img.rectangle(shape, outline="red", width=1)
        print("drawing...")

    cropped_img = cropped_img.resize([int(resize * dim) for dim in cropped_img.size], Image.ANTIALIAS)
    save_path = os.path.join(tmp_directory_path, TMP_IMG_NAME)
    cropped_img.save(save_path)
    return save_path
