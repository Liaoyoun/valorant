import torch
import json
import shutil

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

# 檢查並建立 data.yaml

def checkYaml():

# 取得 valorant 專案根目錄

    projectPath = Path(__file__).parent

# data.yaml 路徑

    yamlFile = projectPath / "data.yaml"

# 預設 YOLO 資料集設定

    content = """path: .
train: images/train
val: images/val
test: images/test

names:
  0: en
  1: enHead
  2: ally
"""

# data.yaml 不存在或內容不同時重新建立

    if (
        not yamlFile.exists()
        or yamlFile.read_text(
            encoding="utf-8"
        ).strip() != content.strip()
    ):

# 寫入 data.yaml

        yamlFile.write_text(
            content,
            encoding="utf-8"
        )

        print(
            "已自動建立或修正 data.yaml"
        )

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

# 檢查並建立模型資料夾

def checkModel():

# 取得專案根目錄
    projectPath = Path(__file__).parent

# 歷史訓練資料夾
    historyPath = projectPath / "history"

# 最佳訓練資料夾
    bestPath = projectPath / "best"

# 資料夾不存在時自動建立
    historyPath.mkdir(parents=True, exist_ok=True)
    bestPath.mkdir(parents=True, exist_ok=True)

    return historyPath, bestPath

# 從歷史訓練恢復最佳模型

def recover(historyPath, bestPath):

# 尋找訓練結果的 info.json

    infoFiles = list(
        historyPath.glob("**/info.json")
)

# 沒有歷史資訊

    if not infoFiles:
        return None

    models = []

    for infoPath in infoFiles:

        try:

            info = json.loads(
                infoPath.read_text(encoding="utf-8")
            )

# 該次訓練的模型最佳

            modelPath =(
                infoPath.parent
                / "weights"
                / "best.pt"
            )

            if not modelPath.exists():
                continue

            if modelPath.stat().st_size == 0:
                continue

# 確認模型能正常載入

            YOLO(str(modelPath))

            models.append(
                (
                    info["mAP50-95"],
                    info["mAP50"],
                    modelPath,
                    infoPath
                )
            )

        except Exception:
            continue

# 沒有任何有效模型

    if not models:
        return None    

# mAP50-95 優先，mAP50 當第二比較條件

    bestModel = max(
        models,
        key = lambda model: (
            model[0],
            model[1]
        )
    )

    modelPath = bestModel[2]
    infoPath = bestModel[3]


# 清除 best 資料夾舊資料

    for file in bestPath.iterdir():

        if file.is_file():
            file.unlink()

# 恢復 best.pt

    shutil.copy2(
        modelPath,
        bestPath /"best.pt"

)

# 恢復 info.json

    shutil.copy2(
        infoPath,
        bestPath / "info.json"
    )

# 如果歷史模型有 TensorRT ，也一起恢復

    enginePath = modelPath.with_suffix(".engine")

    if enginePath.exists():

        shutil.copy2(
            enginePath,
            bestPath /  "best.engine"
        )

    print(
        f"已從 history 恢復最佳模型：{modelPath}"
    )

    return bestPath / "best.pt"

# 尋找下一輪需要用到的模型

def findModel(historyPath, bestPath):

# 最佳模型位置

    bestModel = bestPath / "best.pt"

# 有最佳模型

    if bestModel.exists():

# 檢查是否為空

        if bestModel.stat().st_size == 0:

            print("best.pt 為空檔案")

        else:

            try:

# 測試模型是否能正常載入

                YOLO(str(bestModel))

                print(
                    f"已經找到最佳模型：{bestModel}"
                )

                return bestModel

            except Exception:

                print("best.pt 無法載入")

# best 不存在或已損毀時

    print("嘗試從 history 恢復最佳模型")

    historyModel =recover(
        historyPath,
        bestPath
    )

# history 成功找到最佳模型

    if historyModel is not None:

        return historyModel

# best 與 history 都沒有可用模型

    print("沒有舊模型，使用 yolo11s.pt")

    return "yolo11s.pt"

# 儲存本次訓練模型資訊

def saveInfo(bestModel):

# 找到本次 run 資料夾

    runPath = bestModel.parent.parent

# 載入最佳模型

    model =YOLO(str(bestModel))

# 驗證最佳模型

    result = model.val(
        data = "data.yaml",
        imgsz =1600,
        device = 0,
        verbose = False
    )


# 建立模型資訊

    info = {
        "run": runPath.name,
        "precision": float(result.box.mp),
        "recall": float(result.box.mr),
        "mAP50": float(result.box.map50),
        "mAP50-95": float(result.box.map),
# 各類別 mAP50-95

        "enMap50-95": float(
            result.box.maps[0]
        ),

        "enHeadMap50-95": float(
            result.box.maps[1]
        ),

        "allyMap50-95": float(
            result.box.maps[2]
        )
    }



# info.json 路徑

    infoFile = runPath / "info.json"

# 寫入 JSON

    infoFile.write_text(
        json.dumps(
            info,
            ensure_ascii = False,
            indent = 4
        ),
        encoding = "utf-8"
    )

    print(
        f"以建立模型資訊：{infoFile}"
    )

    return info

# 訓練 YOLO 模型

def trainModel(modelPath, historyPath):

    model = YOLO(str(modelPath))

    model.train(
        data="data.yaml",
        epochs=150,
        imgsz=1600,
        batch=2,
        device=0,
        patience=40,

        optimizer="AdamW",
        lr0=0.0008,


        project=str(historyPath),
        name="run",
        exist_ok=False
    )

# 取得本次訓練最佳模型路徑

    bestPath = Path(model.trainer.best)

# 將最佳模型路徑回傳給主程式

    return bestPath

# 將模型轉換為 TensorRT

def TensorRT(bestModel):

# 載入訓練完成的最佳模型

    model = YOLO(str(bestModel))

# 匯出 FP32 TensorRT Engine

    enginePath = model.export(
        format="engine",
        imgsz=1600,
        batch=1,
        device=0
    )

    return Path(enginePath)

# 更新最佳訓練結果

def updateBest(
    newModel,
    enginePath,
    newInfo,
    bestPath
):
    bestInfoPath = bestPath /"info.json"

# best 還沒有任何資料

    if not bestInfoPath.exists():

        better = True

    else:

        try:

            bestInfo = json.loads(
                bestInfoPath.read_text(
                    encoding = "utf-8"
                )
            )

# mAP50-95 優先

            newScore = (
                newInfo["mAP50-95"],
                newInfo["mAP50"]
            )

            oldScore =(
                bestInfo["mAP50-95"],
                bestInfo["mAP50"]
            )

            better = newScore > oldScore

        except Exception:

# best 資訊壞掉

            better = True

# 新模型不是最佳

    if not better:

        print("本輪模型沒有超越目前最佳模型")
        return False

# 清除 best 資料夾舊資料

    for file in bestPath.iterdir():

        if file.is_file():
            file.unlink()

# 複製新的最佳模型

    shutil.copy2(
        newModel,
        bestPath / "best.pt"
    )

    shutil.copy2(
        enginePath,
        bestPath / "best.engine"
    )

# 找到此次 run 的 info.json

    infoFile = (
        newModel.parent.parent
        / "info.json"
    )

    shutil.copy2(
        infoFile,
        bestPath / "info.json"

    )

    print(
        f"新的最佳模型：{newInfo['run']}"
    )

    return True

# 主程式

def main():

# 檢查並建立 data.yaml

    checkYaml()

# 檢查資料集，資料不足時停止程式

    if not checkData():
        return

# 檢查 GPU 與 CUDA

    if not checkEnv():
        return

# 檢查並建立模型資料夾

    historyPath, bestPath = checkModel()

# 尋找下一輪訓練需要使用的模型

    modelPath = findModel(
        historyPath,
        bestPath
    )

# 開始訓練

    newModel = trainModel(
        modelPath,
        historyPath
    )

# 儲存本次訓練資訊

    newInfo = saveInfo(newModel)

# 將模型轉換為 TensorRT
    
    enginePath = TensorRT(newModel)

# 比較並更新最佳模型
    
    updateBest(
        newModel,
        enginePath,
        newInfo,
        bestPath
    )

if __name__ == "__main__":
    main()

