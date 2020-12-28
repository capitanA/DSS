from log_file import LogRowsOperator
from features import Features
from helper import ownship_position


def start():
    with open('A96_ScP_R1_interpolatedLog.csv', newline='') as myFile:
        logrowsoperator = LogRowsOperator()
        log_objects = logrowsoperator.read_file(myFile)
    features = Features(log_objects, "pushing",900)



if __name__ == "__main__":
    start()
