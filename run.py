from pathlib import Path

def checkData():
    projectPath = Path(__file__).parent
    images = projectPath / "images"
    labels = projectPath / "labels"

    images.mkdir(parents=True, exist_ok=True)
    trainImg = images / "train"
    valImg = images / "val"
    testImg = images / "test"

    labels.mkdir(parents=True, exist_ok=True)
    trainLbl = labels / "train"
    valLbl = labels / "val"
    testLbl = labels / "test"

    trainImg.mkdir(parents=True, exist_ok=True)
    valImg.mkdir(parents=True, exist_ok=True)
    testImg.mkdir(parents=True, exist_ok=True)
    trainLbl.mkdir(parents=True, exist_ok=True)
    valLbl.mkdir(parents=True, exist_ok=True)
    testLbl.mkdir(parents=True, exist_ok=True)
checkData()

