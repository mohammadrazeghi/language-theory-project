from utils.utils import imageType
from phase0.FA_class import DFA
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    image_list = [0 for _ in range(len(images))]
    temp = 0
    for img in images:
        img_index = images.index(img)
        for json_text in json_fa_list:
            module2.solve(json_text, img)
            if module2.percentage > temp:
                image_list[img_index] = json_fa_list.index(json_text)
                temp = module2.percentage
        temp = 0
    return image_list


if __name__ == "__main__":
    ...