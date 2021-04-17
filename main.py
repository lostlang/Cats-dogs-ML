import tarfile
import os
import fnmatch
import shutil


def unzip_data(name, path_files):
    with tarfile.TarFile(name, 'r') as tar_ref:
        tar_ref.extractall(path_files)


def inspect_photo(path_to_data_set):
    tag_photo = {}
    for file in os.listdir(path_to_data_set):
        pet_name = file.split("_")[0].lower()
        if pet_name in tag_photo.keys():
            tag_photo[pet_name] += 1
        else:
            tag_photo[pet_name] = 1
    for tag in tag_photo.keys():
        tag_photo[tag] = int(tag_photo[tag] / 2)
    return tag_photo


def reorganize_data_set(path_to_data_set, name_tags):
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
    for file_name in os.listdir(path_to_data_set):
        tag = file_name.split("_")[0].lower()
        number_file = file_name.split(".")[0].split("_")[-1]
        if fnmatch.fnmatch(file_name, '*.txt'):
            with open("/".join([dir_dataset, dir_train, tag])+".txt", "a") as file:
                with open("/".join([path_to_data_set, file_name]), "r") as input_file:
                    file.write(number_file)
                    file.write(" ")
                    file.write(input_file.readline())
                    file.write("\n")
        else:
            shutil.copy("/".join([path_to_data_set, file_name]),
                        "/".join([dir_dataset, dir_train, tag]))
        pass


def split_to_train():
    pass


if __name__ == "__main__":
    name_dataset = "cats_dogs_dataset.tar"
    path_dataset = name_dataset.split(".")[0]

    #unzip_data(name_dataset, path_dataset)

    animal_amount = inspect_photo(path_dataset)

    #reorganize_data_set(path_dataset, animal_amount.keys())
