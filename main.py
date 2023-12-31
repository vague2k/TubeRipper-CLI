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
    """The start of the program, `CheckVideoLink()` will handle all of the logic for downloading
    the video
    """

    cls()
    video_link = input("Enter a video or playlist link you'd like to download as MP3: ")

    if video_link == "exit":
        sys.exit()

    else:
        CheckVideoLink(video_link)


def CheckVideoLink(url: str):
    """Checks to see if a youtube link is either a "watch", "share", or "playlist" link
        as these would be the only acceptable links to convert and ergo, valid links.

    Parameters
    ----------
    `url : str`
        the url of the youtube video
    """

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
    """Downloads a single YouTube video.

    Parameters
    ----------
    `video_link : str`
        The link inputed by the user
    """

    cls()
    print(Fore.GREEN + "In Progress..." + Style.RESET_ALL)

    video = YouTube(video_link).streams.filter(only_audio=True).first()
    print(Fore.GREEN + "Downloading Video..." + Style.RESET_ALL + f' "{video.title}"')

    out_file = video.download(output_path=DESKTOP)
    RenameExt(out_file)
    print(Fore.GREEN + "Success! Your mp3 has been downloaded" + Style.RESET_ALL)
    time.sleep(3)
    main()


def DownloadPlaylist(video_link: str):
    """Downloads an entire YouTube playlist.

    Parameters
    ----------
    `video_link : str`
        The link inputed by the user
    """

    cls()
    playlist = Playlist(video_link)
    print(Fore.GREEN + "In Progress..." + Style.RESET_ALL + f" {playlist.title}")

    for video in tqdm(playlist.videos):
        print(
            Fore.GREEN + " Downloading Video..." + Style.RESET_ALL + f' "{video.title}"'
        )
        out_file = (
            video.streams.filter(only_audio=True).first().download(output_path=DESKTOP)
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


def RenameExt(out_file: str):
    """Renames the extension of the downloaded YouTube video, as these videos are
    initially downloaded as MP4s.

    Parameters
    ----------
    `out_file : str`
        The original downloaded MP4 file.
    """

    try:
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)

    except FileExistsError as error:
        print(
            Fore.RED
            + f"\nFile already exists, please try again. Restarting"
            + Style.RESET_ALL
        )
        path = os.path.join(DESKTOP, out_file)
        os.remove(path)
        time.sleep(3)
        main()


if __name__ == "__main__":
    main()
