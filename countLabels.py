from pathlib import Path


projectPath = Path(__file__).parent
labelsPath = projectPath / "labels"

classes = {
    0: "en",
    1: "enHead",
    2: "ally"
}


def countFolder(folderName):

    folderPath = labelsPath / folderName

    count = {
        "en": 0,
        "enHead": 0,
        "ally": 0
    }

    total = 0

    for file in folderPath.glob("*.txt"):

        if file.name == "classes.txt":
            continue

        lines = file.read_text(
            encoding="utf-8"
        ).splitlines()

        for line in lines:

            if not line.strip():
                continue

            parts = line.split()

            try:
                classId = int(parts[0])
            except ValueError:
                continue

            if classId in classes:

                className = classes[classId]

                count[className] += 1
                total += 1

    return count, total


def main():

    for folder in ["train", "val", "test"]:

        count, total = countFolder(folder)

        print()
        print(f"========== {folder} ==========")
        print(f"en      : {count['en']}")
        print(f"enHead  : {count['enHead']}")
        print(f"ally    : {count['ally']}")
        print(f"總標註數 : {total}")


if __name__ == "__main__":
    main()