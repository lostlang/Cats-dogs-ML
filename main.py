import tarfile
import os
import fnmatch
import shutil
import random
from PIL import Image, ImageOps


def unzip_data(name, path_files):
    with tarfile.TarFile(name, 'r') as tar_ref:
        tar_ref.extractall(path_files)


def inspect_photo(path_to_data_set):
    tag_photo = {}
    for file in os.listdir(path_to_data_set):
        pet_name = "_".join(file.split("_")[:-1]).lower()
        if pet_name in tag_photo.keys():
            tag_photo[pet_name] += 1
        else:
            tag_photo[pet_name] = 1
    for tag in tag_photo.keys():
        tag_photo[tag] = int(tag_photo[tag] / 2)
    return tag_photo


def reorganize_data_set(path_to_dataset, name_tags):
    dir_dataset = "dataset"
    dir_train = "train"

    # Create folders
    try:
        os.mkdir(dir_dataset)
    except FileExistsError:
        pass
    try:
        os.mkdir("/".join([dir_dataset, dir_train]))
    except FileExistsError:
        pass
    for tag in name_tags:
        try:
            os.mkdir("/".join([dir_dataset, dir_train, tag]))
        except FileExistsError:
            pass

    # Organize file
    for file_name in os.listdir(path_to_dataset):
        tag = "_".join(file_name.split("_")[:-1]).lower()
        number_file = file_name.split(".")[0].split("_")[-1]
        if fnmatch.fnmatch(file_name, '*.txt'):
            with open("/".join([dir_dataset, dir_train, tag])+".txt", "a") as file:
                with open("/".join([path_to_dataset, file_name]), "r") as input_file:
                    file.write(number_file)
                    file.write(" ")
                    file.write(input_file.readline())
                    file.write("\n")
        else:
            shutil.copy("/".join([path_to_dataset, file_name]),
                        "/".join([dir_dataset, dir_train, tag]))


def split_to_train_test(tags_and_amount, percent):
    dir_dataset = "dataset"
    dir_train = "train"
    dir_test = "test"

    try:
        os.mkdir("/".join([dir_dataset, dir_test]))
    except FileExistsError:
        pass

    for item in tags_and_amount.items():
        list_random = list(range(item[1]))
        random.shuffle(list_random)
        list_random = list_random[:round(item[1] * percent / 100)]
        list_random.sort()

        with open("/".join([dir_dataset, dir_test, "info"]) + ".txt", "a") as file:
            with open("/".join([dir_dataset, dir_train, item[0]]) + ".txt", "r") as input_file:
                line = 0
                text = ""
                dir_item = "/".join([dir_dataset, dir_train, item[0]])
                list_files = os.listdir(dir_item)
                for i in list_random:
                    shutil.copy("/".join([dir_item, list_files[i]]),
                                "/".join([dir_dataset, dir_test]))
                    os.remove("/".join([dir_item, list_files[i]]))
                    while line <= i:
                        line += 1
                        text = input_file.readline()
                    file.write(item[0])
                    file.write(" ")
                    file.write(text)


def normalize_train_data_and_generate_new_sample(tags_and_amount, need_sample, need_image_size):
    dir_dataset = "dataset"
    dir_train = "train"
    dir_normalize = "normal"
    new_dir = "/".join([dir_dataset, dir_normalize])

    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass

    for tag in tags_and_amount.keys():
        file_list = os.listdir("/".join([dir_dataset, dir_train, tag]))
        with open("/".join([dir_dataset, dir_train, tag]) + ".txt", "r") as all_info:
            i = 0
            for line in all_info:
                image_info = line.strip().split()
                if fnmatch.fnmatch(file_list[i].split(".")[0], f'*_{image_info[0]}'):
                    i += 1
                    image_name = "/".join([dir_dataset, dir_train, tag, file_list[i]])
                    if tags_and_amount[tag] / need_sample > 1:
                        new_image(image_name, new_dir, need_image_size, 1)
                    elif tags_and_amount[tag] / need_sample > 0.75:
                        new_image(image_name, new_dir, need_image_size, 2)
                    elif tags_and_amount[tag] / need_sample > 0.5:
                        new_image(image_name, new_dir, need_image_size, 3)
                    else:
                        new_image(image_name, new_dir, need_image_size, 4)
                    break
            break


def new_image(old_name, path_to_new, new_size, amount):
    image = Image.open(old_name)
    bw = Image.new("L", (new_size, new_size))
    bw.paste(image.resize((round(new_size * image.size[0] / max(image.size)),
                           round(new_size * image.size[1] / max(image.size)))))
    name = "sample_{}.{}"
    new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
    bw.save("/".join([path_to_new, new_name]))

    bw_mirror = ImageOps.mirror(bw)

    new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
    bw_mirror.save("/".join([path_to_new, new_name]))

    if amount > 1:
        bw_r5 = bw.rotate(5)
        bw_mirror_r5 = bw_mirror.rotate(5)
        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw_r5.save("/".join([path_to_new, new_name]))

        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw_mirror_r5.save("/".join([path_to_new, new_name]))

    if amount > 2:
        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw.rotate(-5).save("/".join([path_to_new, new_name]))

        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw_mirror.rotate(-5).save("/".join([path_to_new, new_name]))
    if amount > 3:
        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw_r5.rotate(-5).save("/".join([path_to_new, new_name]))

        new_name = name.format(len(os.listdir(path_to_new)), old_name.split(".")[-1])
        bw_mirror_r5.rotate(-5).save("/".join([path_to_new, new_name]))


if __name__ == "__main__":
    name_dataset = "cats_dogs_dataset.tar"
    path_dataset = name_dataset.split(".")[0]
    test_percent = 10

    #unzip_data(name_dataset, path_dataset)

    animal_amount = inspect_photo(path_dataset)

    #reorganize_data_set(path_dataset, animal_amount.keys())

    #split_to_train_test(animal_amount, test_percent)

    animal_amount = {tag: round(animal_amount[tag] * 0.9) for tag in animal_amount.keys()}

    normalize_train_data_and_generate_new_sample(animal_amount, 200,  200)


