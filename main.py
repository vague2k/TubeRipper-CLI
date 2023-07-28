import os
import re
import sys
import time

from colorama import Fore, Style
from pytube import Playlist, YouTube
from pytube.cli import on_progress
from tqdm import tqdm

from src.cls import cls

DESKTOP = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")


def main():
    cls()
    video_link = input("Enter a video or playlist link you'd like to download as MP3: ")

    if video_link == "exit":
        sys.exit()

    else:
        CheckVideoLink(video_link)


def CheckVideoLink(url: str):
    if re.search("youtube.com/watch[?]", url) is not None:
        DownloadVideo(video_link=url)

    elif re.search("youtu[.]be", url) is not None:
        DownloadVideo(video_link=url)

    elif re.search("youtube.com/playlist[?]", url) is not None:
        DownloadPlaylist(video_link=url)

    else:
        print("The url you typed was invalid. Please try again")
        time.sleep(3)
        main()


def DownloadVideo(video_link: str):
    cls()
    print(Fore.GREEN + "In Progress..." + Style.RESET_ALL)

    try:
        video = YouTube(video_link).streams.filter(only_audio=True).first()
        print(
            Fore.GREEN + "Downloading Video..." + Style.RESET_ALL + f' "{video.title}"'
        )

        out_file = video.download(output_path=DESKTOP)
        RenameExt(out_file)
        print(Fore.GREEN + "Success! Your mp3 has been downloaded" + Style.RESET_ALL)
        time.sleep(3)
        main()

    except:
        print(
            Fore.RED
            + "Looks like something went wrong... don't know how you managed to do that..."
            + Style.RESET_ALL
        )
        time.sleep(3)
        main()


def DownloadPlaylist(video_link: str):
    cls()
    playlist = Playlist(video_link)
    print(Fore.GREEN + "In Progress..." + Style.RESET_ALL + f" {playlist.title}")

    try:
        for video in tqdm(playlist.videos):
            print(
                Fore.GREEN
                + " Downloading Video..."
                + Style.RESET_ALL
                + f' "{video.title}"'
            )
            out_file = (
                video.streams.filter(only_audio=True)
                .first()
                .download(output_path=DESKTOP)
            )
            RenameExt(out_file)
            print(Fore.GREEN + "Success!" + Style.RESET_ALL)
            time.sleep(1)
            cls()

        print(
            Fore.GREEN
            + "The following videos from playlist: "
            + Style.RESET_ALL
            + f"{playlist.title}\n"
        )
        for video in playlist.videos:
            print(f"    {video.title}")

        print(Fore.GREEN + "\nHave been downloaded! Happy Listening!" + Style.RESET_ALL)
        time.sleep(3)
        main()

    except:
        print(
            Fore.RED
            + "Looks like something went wrong... don't know how you managed to do that..."
            + Style.RESET_ALL
        )
        time.sleep(3)
        main()


def RenameExt(out_file: str):
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)


if __name__ == "__main__":
    main()
