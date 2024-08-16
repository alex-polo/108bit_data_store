import os.path


def create_directory(folder_name: str) -> None:
    path: str = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(path) is False:
        os.mkdir(path)
