import os
import wave
import librosa as librosa

wav_dir = {}
iterable_wav_dir = os.listdir(wav_dir)
changes = {}  # a dict which contain {key: value} as {name_noise: list_of_files}
count_changes = {}  # a dict which contain {key: value} as {name_noise: amount_of_files_changed}
path_noises = ""


def set_changes(noise_name, file_path):
    """
    input:
        noise_name: path to current noise
        file_path: path to audio file that h

    """
    if noise_name in changes.values():
        changes[noise_name].append(file_path)  # add file of noise do changes
        count_changes[noise_name] += 1  # add 1  to the counter

    else:
        changes[noise_name].append(file_path)  # add file of noise to list of files in current noise_name
        count_changes[noise_name] = 1  # add 1  to the counter


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


def dir_noiser_holdout():
    # create the same audio directory but with amount_noise we choose the noises that we want in list of noises
    size_seg_ret, bool = size_seg(count_dir(path_noises))

    name_main_dir = os.path.dirname(wav_dir)
    name = f'{name_main_dir}_noised'
    os.mkdir()
    for w_file in iterable_wav_dir:
        noise = ""
        audio_arr, sr = librosa.load(w_file)  # get the array of numbers which represents the audio
        noise_arr, sr = librosa.load(noise)
        noise_audio = audio_arr + noise_arr
        w_file_name_without_type = w_file.split(".")[0]
        path_to_noise = f'{name}\\{w_file_name_without_type}_{noise}.wav'
        librosa.output.write_wav(path_to_noise, noise_audio, sr)  # Save the mixed audio data as a new audio file
        set_changes(noise, path_to_noise)
