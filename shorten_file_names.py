import os


def main():
    path = "C:\\Users\\user-name\\Pictures\\2025-01-01_Holiday\\" # dir path example
    for filename in enumerate(os.listdir(path)):
        src = path + filename[1]
        # '[4:]' will cut the 'IMG_' string from the image file
        dst = path + filename[1][4:]
        os.rename(src, dst)


if __name__ == "__main__":
    main()
