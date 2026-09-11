import os
import xml.etree.ElementTree as ET

classes = {
    "en": 0,
    "enHead": 1,
    "ally": 2,
    "allyHead": 3
}

xmlPath = "labels/test"
labelPath = "labels/test"


def convertBox(imgWidth, imgHeight, xmin, ymin, xmax, ymax):
    xCenter = ((xmin + xmax) / 2) / imgWidth
    yCenter = ((ymin + ymax) / 2) / imgHeight

    boxWidth = (xmax - xmin) / imgWidth
    boxHeight = (ymax - ymin) / imgHeight

    return xCenter, yCenter, boxWidth, boxHeight


def convertVocToYolo():
    if not os.path.exists(xmlPath):
        print(f"找不到資料夾：{xmlPath}")
        return

    xmlFiles = [
        file for file in os.listdir(xmlPath)
        if file.lower().endswith(".xml")
    ]

    if len(xmlFiles) == 0:
        print("找不到 XML")
        return

    success = 0
    fail = 0

    for file in xmlFiles:
        filePath = os.path.join(xmlPath, file)

        try:
            tree = ET.parse(filePath)
            root = tree.getroot()

            size = root.find("size")

            if size is None:
                print(f"[錯誤] {file} 找不到圖片尺寸")
                fail += 1
                continue

            imgWidth = int(size.find("width").text)
            imgHeight = int(size.find("height").text)

            name = os.path.splitext(file)[0]
            txtPath = os.path.join(labelPath, name + ".txt")

            lines = []

            for obj in root.findall("object"):
                className = obj.find("name").text.strip()

                if className not in classes:
                    print(f"[跳過] {file} 未知類別：{className}")
                    continue

                classId = classes[className]

                box = obj.find("bndbox")

                if box is None:
                    print(f"[跳過] {file} 的 {className} 找不到框")
                    continue

                xmin = float(box.find("xmin").text)
                ymin = float(box.find("ymin").text)
                xmax = float(box.find("xmax").text)
                ymax = float(box.find("ymax").text)

                xCenter, yCenter, boxWidth, boxHeight = convertBox(
                    imgWidth,
                    imgHeight,
                    xmin,
                    ymin,
                    xmax,
                    ymax
                )

                line = (
                    f"{classId} "
                    f"{xCenter:.6f} "
                    f"{yCenter:.6f} "
                    f"{boxWidth:.6f} "
                    f"{boxHeight:.6f}"
                )

                lines.append(line)

            with open(txtPath, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line + "\n")

            os.remove(filePath)

            print(f"[完成] {file} -> {name}.txt，已刪除 XML")
            success += 1

        except Exception as e:
            print(f"[失敗] {file}: {e}")
            fail += 1

    print()
    print("==========")
    print("轉換完成")
    print(f"成功：{success}")
    print(f"失敗：{fail}")
    print("==========")


def main():
    convertVocToYolo()


main()