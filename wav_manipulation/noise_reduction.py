import os
import tempfile
import wave
from random import random

import librosa
import soundfile
from pydub import AudioSegment
import numpy as np

wav_dir = ""
changes = {}  # a dict which contain {key: value} as {name_noise: list_of_files}
count_changes = {}  # a dict which contain {key: value} as {name_noise: amount_of_files_changed}
path_noises = ""


def get_duration(wav_file):
    """
    input:
        wav_file: path to file

    output:
        duration: duration of the wav file
    """
    with wave.open(wav_file, 'rb') as wf:
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()

        duration = num_frames / frame_rate  # Calculate the duration
    return duration


def count_dir(path_dir):
    """
    input:
        dir: path to directory

    output:
        count: how many files are in this directory
    """
    count = 0
    # Iterate directory
    for path in os.listdir(path_dir):
        # check if current path is a file
        if os.path.isfile(os.path.join(path_dir, path)):
            count += 1
    return count


def size_seg(number):
    """
    input:
        number: int

    output:
        segment_size: how many groups will be if we divide the number of files by the number of exist noises
        bool: represent if there will be a rest or not
    """
    global wav_dir
    print(count_dir(wav_dir))
    bool = False
    if count_dir(wav_dir) % number == 0:
        segment_size = count_dir(wav_dir) / number
    else:
        segment_size = count_dir(wav_dir) / number
        bool = True
    return segment_size, bool


def update_noise(current_noise_path):
    """
    input:
        current_noise: path to noise

    output:
        noise: the next noise in the directory of noises
    """
    current_noise_file = current_noise_path.split("\\")[-1]
    flag_current = False
    list_noises = os.listdir(path_noises)

    if current_noise_file == list_noises[-1]:
        return 1

    else:
        for noise_file in list_noises:
            if flag_current:
                return noise_file

            if current_noise_file == noise_file:
                flag_current = True


def resize_noise(wav_path, duration_seconds):
    audio, sr = librosa.load(wav_path, sr=44100)
    splited_filename = audio[:int(duration_seconds * sr)]  # Truncate the audio signal to the desired duration

    path_temp_noises = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\temp_noises"
    wav_name_with_type = wav_path.split("\\")[-1]
    wav_name = wav_name_with_type.split(".")[-1]
    path = os.path.join(path_temp_noises, f'{wav_name}_noised_{duration_seconds}.wav')
    soundfile.write(path, splited_filename, sr)  # Write the truncated audio signal to the temporary WAV file
    return path


def balance_sounds(wav_audio_arr, wav_noise_arr):
    return wav_noise_arr / 4


def dir_noiser_holdout():
    """
    the function return a directory which contain the dataset but with the noise.
    the 'size_seg' return segment_size which represent the size of each group.
    group is segment of the audio dir, all the group are equals.
    each group will be colored with one of the noises that in the "noises" folder.
    """

    global directory_path, noise, noise_arr_new, new_noise_path, new_directory_name, parent_directory, parent_directory, parent_directory
    parent_directory = os.path.dirname(wav_dir)  # Get the parent directory of the given path
    parent_directory_name = f'{os.path.basename(wav_dir)}_noised'

    directory_path = os.path.join(parent_directory,
                                  parent_directory_name)  # Create the new directory by joining the parent directory with the new directory name

    if not os.path.exists(os.path.join(os.path.dirname(wav_dir), f'{os.path.basename(wav_dir)}_noised')):
        # create the folder which will contain the noisy data
        os.mkdir(directory_path)


    size_seg_ret, flag_plus = size_seg(
        count_dir(path_noises))  # find how many wav files will be selected fot each noise
    name_main_dir = os.path.dirname(wav_dir)
    path_to_noisy_audio = f'{name_main_dir}_noised'
    print(f'{size_seg_ret}%%{flag_plus}')

    counter = 0  # until the size of as segment

    noise_path = os.path.join(path_noises,
                              os.listdir(path_noises)[0])  # create the init path to noise(the first in the list)
    noise = os.listdir(path_noises)[0]

    for w_file in os.listdir(wav_dir):
        w_file_path = os.path.join(wav_dir, w_file)

        if flag_plus:  # if there is one file that is odd from the segments - we skip it
            flag_plus = False
            continue

        if counter == int(size_seg_ret):  # get path for a new noise and init the counter
            noise = update_noise(noise_path)
            noise_path = os.path.join(path_noises, noise)
            counter = 0

        if get_duration(w_file_path) < get_duration(noise_path):
            new_noise_path = resize_noise(noise_path, int(get_duration(w_file_path)))

        audio_arr, sr1 = librosa.load(w_file_path)  # get the array of numbers which represents the audio
        noise_arr, sr2 = librosa.load(new_noise_path)

        if sr1 != sr2:
            noise_arr_new = librosa.resample(noise_arr, sr2,
                                             sr1)  # Resample audio_arr to the same sample rate as noise_arr

        noise_arr_new = balance_sounds(audio_arr, noise_arr)

        noise_audio = [sum(x) for x in zip(audio_arr, noise_arr_new)]
        path_to_noisy_audio = f'{directory_path}\\noised_{w_file}'
        soundfile.write(path_to_noisy_audio, noise_audio, sr1)  # Save the mixed audio data as a new audio file
        print(f'{counter} new file {path_to_noisy_audio} was added with {noise} noise')
        counter += 1


if __name__ == '__main__':
    ################################
    w_file = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02\\02_01_01_01_dogs-sitting_disgust.wav"
    wav_dir = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_01"
    noise = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\wav_manipulation\\noises\\heavy_rain_and_thunder.wav"
    try_path = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02"
    path_to_noise = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02_noised"
    path_noises = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\wav_manipulation\\noises"

    # if get_duration(noise) != get_duration(w_file):
    #     noise = resize_noise(noise, get_duration(w_file))
    #     print("ok")
    #
    # path_noise = f'{path_to_noise}\\new_noise_less.wav'
    #
    # audio_arr, sr1 = librosa.load(w_file, sr=44100)  # get the array of numbers which represents the audio
    # noise_arr, sr2 = librosa.load(noise, sr=44100)
    # print("noisyyyyy")
    # if sr1 != sr2:
    #     noise_arr = librosa.resample(noise_arr, sr2, sr1)  # Resample y2 to the same sample rate as y1
    # audio_arr, noise_arr = balance_sounds(audio_arr, noise_arr)
    # noise_audio = [sum(x) for x in zip(audio_arr, noise_arr)]
    #
    # path_noise = f'{path_to_noise}\\new_noise.wav'
    # soundfile.write(path_noise, noise_audio, sr1)
    ################################
    dir_noiser_holdout()
