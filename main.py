import re, os, torch
import whisper
import subprocess

def is_valid_youtube_uri(url):
    regex = (
      r"(https?://)?(www\.)?"
      "(youtube|youtu|youtube-nocookie)\.(com|be)/"
      "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    match = re.match(regex, url)
    return match is not None

def download_video_as_mp3(url):
  command = ["./youtube-dl", "--get-filename", "--output", "%(title)s.%(ext)s", url]
  result = subprocess.run(command, capture_output=True, text=True)
  filename = result.stdout.strip().replace(".mp4", "")

  subprocess.run(["./youtube-dl", "-f", "140", "--output", filename, url], capture_output=True, text=True)
  return filename

def transcribe_audio(filename, device="cpu"):
  if torch.cuda.is_available():
    device = "cuda"
  
  model = whisper.load_model("./models/medium.pt", device=device)
  result = model.transcribe(filename)
  return result["text"]

def main():
  with open("youtube_urls.txt", "r") as file:
    for line in file:
      youtube_url = line.strip()
      
      print(f"Processing {youtube_url}")
      if is_valid_youtube_uri(youtube_url):
        filename = download_video_as_mp3(youtube_url)
        print(f"Downloaded and saved as {filename}")

        result = transcribe_audio(filename)
        output_name = filename.replace(".mp3", "")

        with open(f"{output_name}-transcript.txt", "w", encoding="utf-8") as transcript_file:
          transcript_file.write(result)
        
        os.remove(filename)
        print(f"Transcript saved as {filename}-transcript.txt")
      else:
        print(f"Invalid Youtube URL: {youtube_url} - Please check the URL and try again.")

if __name__ == "__main__":
  main()