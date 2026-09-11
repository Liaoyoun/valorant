import torch
from ultralytics import YOLO
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
        print(f"請將資料分別放入：{', '.join(missing)}")
        return False
    
    return True

# 檢查並建立 data.yaml
def checkYaml():

# 取得 valorant 專案根目錄
    projectPath = Path(__file__).parent

# data.yaml 路徑
    yamlFile = projectPath / "data.yaml"

# data.yaml 不存在時自動建立
    if not yamlFile.exists():

# 預設 YOLO 資料集設定
        content ="""path: .
train: images/train
val: images/val
test: images/test

names:
    0: enemy
"""

# 寫入 data.yaml
        yamlFile.write_text(content, encoding="utf-8")
        print("已自動建立 data.yaml")

    return True

# 檢查 GPU 與 CUDA 環境
def checkEnv():

# CUDA 無法使用時停止
    if not torch.cuda.is_available():
        print("CUDA 無法使用")
        return False

# 取得 GPU 名稱
    gpu = torch.cuda.get_device_name(0)

    print(f"GPU:{gpu}")
    return True

def trainModel():
        model = YOLO("yolo11s.pt")
        model.train(data="data.yaml",
                    epochs=100,
                    imgsz=320,
                    batch=16,
                    device=0,
                    patience=10,
                    project="runs"
        )

# 主程式
def main():

# 檢查並建立 data.yaml
    checkYaml()
# 檢查資料集，資料不足時停止程式
    if not checkData():
        return

    if not checkEnv():
        return

    trainModel()

main()

