import os
import shutil


def setup_env():
    if not os.path.exists("env_example"):
        raise ValueError("File env_example not found")

    try:
        shutil.copy2("env_example", ".env")
        print("done")
    except:
        print("smth went wrong")


if __name__ == "__main__":
    setup_env()


# alemibc скрипт для миграций, чтобы он в докере запускался
