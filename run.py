from pathlib import Path

def checkData():
    projectPath = Path(__file__).parent

    # valorant 根目錄
    images = projectPath / "images"
    labels = projectPath / "labels"

    images.mkdir(parents=True, exist_ok=True)
    labels.mkdir(parents=True, exist_ok=True)

    # images 子資料夾
    trainImg = images / "train"
    valImg = images / "val"
    testImg = images / "test"

    trainImg.mkdir(parents=True, exist_ok=True)
    valImg.mkdir(parents=True, exist_ok=True)
    testImg.mkdir(parents=True, exist_ok=True)

    # labels 子資料夾
    trainLbl = labels / "train"
    valLbl = labels / "val"
    testLbl = labels / "test"
    
    trainLbl.mkdir(parents=True, exist_ok=True)
    valLbl.mkdir(parents=True, exist_ok=True)
    testLbl.mkdir(parents=True, exist_ok=True)
    



checkData()

