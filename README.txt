Readme.txt

Your README file should include the following:
* A short description of your software and what it does.

Logic Quest is an educational game that allows users to learn propositional logic statements. This game involves many different screens and user interaction for game play. The 2 main game modes include training mode which allows ample time for users to think through solutions and even save/quit the game and continue their progress later on. Lightning mode is a fast pace environment where users must think under pressure to answer as many questions as possible before the timer runs out. Scores are saved and users can compete for the top spot on the leader board. Instructor mode allows educators to go through all available questions, view solutions and even add their own customized questions.


* A list of the required libraries and third party tools required to run or build your software (include version numbers).
Python version 3.1
Pygame 2.5.2

Install Python 3.10
Step 1:
Download Python: Go to the official Python website's download page for Windows at python.org. Look for Python 3.10, and download the Windows installer executable for your system (32-bit or 64-bit).
Step 2: Once the download is complete, run the installer. Ensure to check the box that says "Add Python 3.10 to PATH" at the bottom of the installer window. This step is crucial as it makes Python accessible from the command line.
Step 3:
Click on "Install Now" and wait for the installation to complete.
Step 4:
Verify Installation: Open the Command Prompt (you can search for 'cmd' in the Start menu) and type python --version. If Python is installed correctly, it should display something like Python 3.10.x.

Install Pygame 2.5.2
Step 1:
Make sure you have python 3.10
Step 2:
Open Command Prompt
Step 3:
In the Command Prompt, type the following command: python -m pip install pygame==2.5.2
Step 4:
Verify installation: In the Command Prompt, type the following command: python -m pygame --version
The expected output is. “2.5.2”
  

* A detailed step by step guide for building your software (compiling it from source code). This should include details on how to obtain and install any third party libraries.
    Just run the Sign_In.py file in the root directory of the repository. 

* A detailed step by step guide on how to run your already built (compiled) software.
    To run the software, simply run the Sign_In.py file in the root directory of the repository.

* A user guide, that explains how to use your software.
From the Sign in page users must sign in with a username, by entering the optional keys “instructor” or “developer” users can enter the instructor/developer features.
After the sign in screen users reach a main menu screen, with multiple options. The Leaderboard selection brings users to a leaderboard screen where they can compete against other users for the top score. From the settings page users have the ability to adjust volume settings by using intuitive + and - buttons. By clicking load game the user will automatically re-enter into the training mode at the last level where they left off. Additional security is not required as users are already signed into the game by this point.

For users by clicking start game provides new additional options They can start a new game in Training Mode or Lightning mode. The tutorial screen provides detailed instructions on game play and user shortcuts. By starting a new training mode game, users can play with unlimited time and think through solutions. Game play is done by dragging options from the bottom into the centre submission square, this will provide correct/wrong answer feedback. If a question is too challenging users can skip to the next question with the next question button. By clicking P on the keyboard users can resume game play, save game, or exit the game.

In the lightning mode there is a time limit per question of 10 seconds, users have the opportunity to answer as many questions as they can to get a high score, when a user is unable to answer the question in 10 seconds the game play ends and the score is saved and if high enough updated on the leaderboard. They can click esc on the keyboard to exit the game mode.


For instructors/developers pressing the start game tab offers different options being an instructor mode and a developer mode instead of lightning mode and training mode. In the instructor mode you can go back and forth between questions with the Next Question and Prev Question buttons. Reveal question solutions with the See Answer button. A significant feature in instructor mode is the Ability to add questions with the Add Question button. This launches an overlaid window with many text box prompts. The instructor must fill in all the information for question description, question solution, question difficulty and 4 options to submit the new question into the game. It is important that the instructor ensure that one of the 4 options be the correct solution. By clicking the submit button the question is loaded into the game and by clicking return the add question window is closed returning to instructor mode.

In the developer mode screen this provides developers useful information to check gameplay works properly. It includes the timer from the lightning mode ensuring that all features related to the timer function correctly. Also when moving any of the draggable options the left side of the screen will print the collisions that occur so the developer knows the game mechanics are functioning correctly. As well the developer will be prompted of “wrong” and “correct” when dragging options to the submission box to understand that the options are correct.


* If your software uses accounts, a password, or pin you must include any account username/password, pin, etc. required to use your software.

In our software users can enter any username they want to enter game play, by entering an optional “instructor” or “developer” key users can access the instructor and developer features.

* You must also include details on how to access your teacher mode and steps to build/install it if it is a separate program.

To access the teacher mode the functionality is built in. From the sign in page an existing user must enter the instructor key “instructor”. Once signed in from the main menu users select the Start Game tab and then can click the Instructor Mode tab to access all features of the instructor mode.


* Anything else that would be helpful for the TA marking your project to know.


This README file should be in the root directory of your repository and in your submitted zip archive.
