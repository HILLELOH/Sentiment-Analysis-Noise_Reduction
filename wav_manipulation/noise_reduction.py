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

        # Calculate the duration
        duration = num_frames / frame_rate
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
    print('File count:', count)
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

    bool = False
    if count_dir(wav_dir) % number == 0:
        segment_size = count_dir(wav_dir) / number
    else:
        segment_size = count_dir(wav_dir) / number
        bool = True
    return segment_size, bool


def update_noise(current_noise):
    """
    input:
        current_noise: path to noise

    output:
        noise: the next noise in the directory of noises
    """
    flag_current = False
    for noise in os.listdir(path_noises):
        if flag_current:
            return noise

        if current_noise == noise:
            flag_current = True


def resize_noise(wav_path, duration_seconds):

    audio, sr = librosa.load(wav_path, sr=44100)
    splited_filename = audio[:int(duration_seconds*sr)]  # Truncate the audio signal to the desired duration

    path_temp_noises = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\temp_noises"
    wav_name_with_type = wav_path.split("\\")[-1]
    wav_name = wav_name_with_type.split(".")[-1]
    path = os.path.join(path_temp_noises, f'{wav_name}_noised.wav')
    print(path)
    soundfile.write(path, splited_filename, sr)  # Write the truncated audio signal to the temporary WAV file
    return path


def dir_noiser_holdout():
    """
    the function return a directory which contain the dataset but with the noise.
    the 'size_seg' return segment_size which represent the size of each group.
    group is segment of the audio dir, all the group are equals.
    each group will be colored with one of the noises that in the "noises" folder.
    """

    global new_directory_path, noise, noise_arr_new
    if not os.path.exists(os.path.join(os.path.dirname(wav_dir), f'{os.path.basename(wav_dir)}_noised')):
        parent_directory = os.path.dirname(wav_dir)  # Get the parent directory of the given path
        new_directory_name = f'{os.path.basename(wav_dir)}_noised'

        new_directory_path = os.path.join(parent_directory,
                                          new_directory_name)  # Create the new directory by joining the parent directory with the new directory name
        os.mkdir(new_directory_path)  # Create the new directory

    size_seg_ret, flag_plus = size_seg(count_dir(path_noises))

    name_main_dir = os.path.dirname(wav_dir)
    name = f'{name_main_dir}_noised'

    counter = 0
    noise_path = os.path.join(path_noises, os.listdir(path_noises)[0])

    for w_file in os.listdir(wav_dir):
        w_file_path = os.path.join(wav_dir, w_file)

        if flag_plus:
            flag_plus = False
            continue

        if counter == size_seg_ret:
            noise = update_noise(os.listdir(path_noises)[0])
            noise_path = os.path.join(os.path.dirname(path_noises), noise)
            counter = 0

        if get_duration(w_file_path) < get_duration(noise_path):
            new_noise_path = resize_noise(noise_path, int(get_duration(w_file_path)))
            audio_arr, sr1 = librosa.load(w_file_path)  # get the array of numbers which represents the audio
            noise_arr, sr2 = librosa.load(new_noise_path)

            if sr1 != sr2:
                noise_arr_new = librosa.resample(noise_arr, sr2, sr1)  # Resample y2 to the same sample rate as y1

            # Concatenate the audio data arrays
            new_noised = np.concatenate((audio_arr, noise_arr_new))

            path_to_noise = f'{new_directory_path}\\{w_file}'
            # Write the concatenated audio data to a new WAV file
            soundfile.write(path_to_noise, new_noised, sr1)
            noise_audio = [sum(x) for x in zip(audio_arr, noise_arr_new)]
            soundfile.write(path_to_noise, noise_audio, sr1)  # Save the mixed audio data as a new audio file
            counter += 1

        elif get_duration(w_file) >= get_duration(noise_path):
            audio_arr, sr1 = librosa.load(w_file, sr=44100)  # get the array of numbers which represents the audio
            noise_arr, sr2 = librosa.load(noise, sr=44100)
            if sr1 != sr2:
                noise_arr = librosa.resample(noise_arr, sr2, sr1)  # Resample y2 to the same sample rate as y1
            noise_audio = [sum(x) for x in zip(audio_arr, noise_arr)]
            path_to_noise = f'{new_directory_path}\\{w_file_path}'

            soundfile.write(path_to_noise, noise_audio, sr1)  # Save the mixed audio data as a new audio file
            counter += 1


if __name__ == '__main__':
    # noise_path = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\wav_manipulation\\noises"
    # dataset_clean = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02"
    #
    # wav_dir = dataset_clean
    # path_noises = noise_path
    # dir_noiser_holdout()
################################
    w_file = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02\\02_01_01_01_dogs-sitting_disgust.wav"
    noise = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\wav_manipulation\\noises\\baby_crying.wav"
    try_path = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02"
    path_to_noise = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training\\Actor_02_noised"

    if get_duration(noise) > get_duration(w_file):
        resize_noise(noise, get_duration(w_file))
        print("ok")

    audio_arr, sr1 = librosa.load(w_file, sr=44100)  # get the array of numbers which represents the audio
    noise_arr, sr2 = librosa.load(noise, sr=44100)
    print(audio_arr)
    if sr1 != sr2:
        noise_arr = librosa.resample(noise_arr, sr2, sr1)  # Resample y2 to the same sample rate as y1

    noise_audio = [sum(x) for x in zip(audio_arr, noise_arr)]

    path_noise = f'{path_to_noise}\\new_noise.wav'
    soundfile.write(path_noise, noise_audio, sr1)
################################
    # noise = "C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\wav_manipulation\\noises\\baby_crying.wav"
    # str = resize_noise(noise, 16)
    # print(str)