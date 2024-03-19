from pathlib import Path

from pydub import AudioSegment
from tqdm import tqdm


def conver_to_wav():

    ## LOAD FILES
    file_dir = Path.cwd()
    wav_list = list(file_dir.glob("*"))


    ## CONVERT TO WAV
    for i in tqdm(range(len(wav_list))):
        file_name = wav_list[i].stem
        file_extension = wav_list[i].suffix[1:]

        # NO EXTENSION
        if file_extension == "":
            continue

        # FROM MP3
        elif file_extension == "mp3":
            sound = AudioSegment.from_mp3(wav_list[i])
            sound.export(f"{file_dir}/{file_name}.wav".format(i), format="wav")

        # FROM OGG
        elif file_extension == "ogg":
            sound = AudioSegment.from_ogg(wav_list[i])
            sound.export(f"{file_dir}/{file_name}.wav".format(i), format="wav")

        # FROM ETC
        else:
            sound = AudioSegment.from_file(wav_list[i], file_extension)
            sound.export(f"{file_dir}/{file_name}.wav".format(i), format="wav")


if __name__ == "__main__":
    conver_to_wav()
    print("DONE! 👋 🌊 〰️")
