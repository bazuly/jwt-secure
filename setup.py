import os
import shutil


def set_up():
    if not os.path.exists("env_example"):
        raise ValueError("File env_example not found")

    try:
        shutil.copy2("env_example", ".env")
        print("done")
    except:
        print("smth went wrong")


if __name__ == "__main__":
    set_up()


# alemibc скрипт для миграций, чтобы он в докере запускался
