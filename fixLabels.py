import os
import shutil

labelPath = "labels/train"
backupPath = "labels/trainBackup"

fixMap = {
    15: 2,  # ally
    2: 3,   # allyHead
    3: 0,   # en
    0: 1    # enHead
}


def fixLabels():
    if not os.path.exists(labelPath):
        print("找不到 labels/train")
        return

    # 先備份
    if not os.path.exists(backupPath):
        shutil.copytree(labelPath, backupPath)
        print("已建立備份：labels/trainBackup")

    files = [
        file for file in os.listdir(labelPath)
        if file.endswith(".txt") and file != "classes.txt"
    ]

    fixed = 0
    unknown = 0

    for file in files:
        filePath = os.path.join(labelPath, file)

        with open(filePath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        newLines = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            parts = line.split()
            classId = int(parts[0])

            if classId in fixMap:
                parts[0] = str(fixMap[classId])
                fixed += 1

            elif classId == 1:
                # 如果真的遇到 1，先不要亂改
                print(f"[檢查] {file} 發現 ID 1")
                unknown += 1

            else:
                print(f"[未知] {file} ID：{classId}")
                unknown += 1

            newLines.append(" ".join(parts))

        with open(filePath, "w", encoding="utf-8") as f:
            for line in newLines:
                f.write(line + "\n")

    classesPath = os.path.join(labelPath, "classes.txt")

    with open(classesPath, "w", encoding="utf-8") as f:
        f.write("en\n")
        f.write("enHead\n")
        f.write("ally\n")
        f.write("allyHead\n")

    print()
    print("修復完成")
    print(f"修改標註：{fixed}")
    print(f"需要檢查：{unknown}")


fixLabels()