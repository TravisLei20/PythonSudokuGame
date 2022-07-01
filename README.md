# PythonSudokuGame

This was a personal project that I started doing in my free time.
I started doing it because I was doing a Kata on codewars that required me to create an algorithm that solved a sudoku puzzle.

Upon completion, I decided that I wanted to take this algorithm and make it into a Raspberry Pi project.
I wanted to be able to take a picture of an empty sudoku puzzle and have the algorithm spit out the correct answers for said puzzle.
After doing some research and buying a camera I was able to use the Raspberry Pi camera to take a picture of a sudoku puzzle in the format of:

  400390072
  005000010
  010057806
  004002000
  070980000
  092005001
  001004050
  800160000
  009000007
  
 and solve it.
 I, however, wasn't able to take a picture of a sudoku puzzle without the zero(representing empty spaces) and with the lines of the board.
 
 Because of this I wanted to see if I could upload an image to PyCharm and have it read the puzzle.
 Once again, I found that it could only read the format above and not a normal picture of a sudoku puzzle.
 
 After this I decided that I was going to do more research on image reading software/image processing and in the mean time move onto a new project.
 
 A week or so went by and I was browsing YouTube in search of fun python projects when I came across a video showing that someone also created a sudoku project.
 Their sudoku project didn't include image processing but it did include a GUI that allowed the user to play the game on their computer.
 
 After a few days of working on it I completed this project with the image processing software pytesseract and GUI software PyGame, for now. 
 Date: (7/1/2022)
 
 In the future I want to be able to achieve my original goal of capturing an image of a sudoku game and output the completed/finished board.
