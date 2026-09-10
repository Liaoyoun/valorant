from pathlib import Path

# 檢查並建立 YOLO 資料集資料夾
def checkData():

    # 取得 valorant 專案根目錄
    projectPath = Path(__file__).parent

    # valorant 根目錄下的主要資料夾
    images = projectPath / "images"
    labels = projectPath / "labels"

    # 建立主要資料夾
    images.mkdir(parents=True, exist_ok=True)
    labels.mkdir(parents=True, exist_ok=True)

    # images 子資料夾路徑
    trainImg = images / "train"
    valImg = images / "val"
    testImg = images / "test"

    # 建立 images 子資料夾
    trainImg.mkdir(parents=True, exist_ok=True)
    valImg.mkdir(parents=True, exist_ok=True)
    testImg.mkdir(parents=True, exist_ok=True)

    # labels 子資料夾路徑
    trainLbl = labels / "train"
    valLbl = labels / "val"
    testLbl = labels / "test"

    # 建立 labels 子資料夾
    trainLbl.mkdir(parents=True, exist_ok=True)
    valLbl.mkdir(parents=True, exist_ok=True)
    testLbl.mkdir(parents=True, exist_ok=True)

    # 儲存沒有資料的資料夾
    missing = []

    # 檢查 images 資料
    if not any(trainImg.iterdir()):
        missing.append("images/train")
    if not any(valImg.iterdir()):
        missing.append("images/val")
    if not any(testImg.iterdir()):
        missing.append("images/test")

    # 檢查 labels 資料
    if not any(trainLbl.iterdir()):
        missing.append("labels/train")
    if not any(valLbl.iterdir()):
        missing.append("labels/val")
    if not any(testLbl.iterdir()):
        missing.append("labels/test")

    # 有空資料夾時統一顯示一次提示
    if missing:
        print(f"請將資夾分別放入:{', '.join(missing)}")
        return False
    
    return True


def checkYaml():
    # 取得 valorant 專案根目錄
    projectPath = Path(__file__).parent

    # 檢查並建立 data.yaml
    yamlFile = projectPath / "data.yaml"
    if not yamlFile.exists():
        content ="""path: .
train: images/train
val: images/val
test: images/test

names:
    0: enemy
"""
    
        yamlFile.write_text(content, encoding="utf-8")
        print("已自動建立 data.yaml")

    return True


def main():
    checkYaml()

    if not checkData():
        return


main()