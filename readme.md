# Transcriptor
This python project lets you create multiple transcripts with youtube links on Google Colab with Whisper AI.

## Questions
### Why Google Colab?
I used Google Colab because of my internet speed & free GPU usage. It works flawlessly in Turkish language (which I used this to get the transcripts on Google Oyun ve Uygulama Akademisi education videos).

## Features
- Downloads multiple links on the `youtube_urls.txt` file.
- Creates transcripts for every mp3 file it downloaded.
- Automatically deletes mp3 files after creating its transcript.
- Uses `youtube-dl` as in nightly mode to remove some bugs from the new latest version.

### Dependencies
- Python 3.x (which Google Colab has)
- whisper
- torch

### Executing the Program
- Firstly, create yourself a google colab and change runtime type to make it as a GPU.
- After that, create a `youtube_urls.txt` - You can find the example in our repo.
- Creating urls.txt, use `!chmod 755 main.sh` and do `!./main.sh` in notebook to install everything and the program will open itself.
- After program finishes its job, download the .txt files and you are good to go!
- Do not forget to open the tab while it does it job, otherwise your files in colab will be deleted!

## For Issues and Questions
Dont feel shy to ask your questions/problems in issues tab! You can also contribute the code in Pull requests tab.
