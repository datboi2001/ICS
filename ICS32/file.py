from pathlib import Path

def make_file(path: Path) -> None:
    for x in range(29):
        lecture = path/f"Lecture{x}.docx"
        lecture.touch()

class Person():
    def __init__(self,):
make_file(Path(r"C:\Users\Manh Dat Nguyen\Desktop\ICS 33"))