import os
import wave

import librosa
import soundfile

wav_dir = ""
path_noises = ""


def get_duration(wav_file):
    """
    input:
        wav_file: (string) path to file

    output:
        duration: (int) duration of the wav file
    """
    with wave.open(wav_file, 'rb') as wf:
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()

        duration = num_frames / frame_rate  # Calculate the duration
    return duration


def count_dir(path_dir):
    """
    input:
        path_dir: (string) path to directory

    output:
        count: (int) how many files are in this directory
    """
    count = 0
    # Iterate directory
    for path in os.listdir(path_dir):
        # check if current path is a file
        if os.path.isfile(os.path.join(path_dir, path)):
            count += 1
    return count


def size_seg(wav_file_dir, number):
    """
    input:
        wav_file_dir: (string) represent the audio directory
        number: (int) the number of the noises

    output:
        segment_size: (int) how many groups will be if we divide the number of files by the number of exist noises
        flag: (boolean) represent if there will be a rest or not
    """
    global mod, side_ret
    flag = False
    if count_dir(wav_file_dir) % number == 0:
        segment_size = int(count_dir(wav_file_dir) / number)
    else:
        segment_size = count_dir(wav_file_dir) / number
        plus = segment_size - int(segment_size)  # add the modulo thar segment_size have
        mod = int(count_dir(path_noises)*plus)
        side_ret = int(mod/count_dir(path_noises))
        segment_size = int(segment_size)
        segment_size = segment_size + side_ret
        flag = True
    return segment_size, flag


def update_noise(current_noise_path):
    """
    input:
        current_noise: (string) path to noise

    output:
        noise: (string) the next noise in the directory of noises
    """
    current_noise_file = current_noise_path.split("\\")[-1]
    flag_current = False
    list_noises = os.listdir(path_noises)

    if current_noise_file == list_noises[-1]:
        print(f'End of process: no more files!')
        return

    else:
        for noise_file in list_noises:
            if flag_current:
                return noise_file

            if current_noise_file == noise_file:
                flag_current = True


def resize_noise(wav_path, duration_seconds):
    """
    input:
        wav_path: (string) to be cut
        duration_seconds: (seconds) what length will be the temporary noise

    return:
          path: (string) path of the temp noise audio after adjust the time
    """

    audio, sr = librosa.load(wav_path, sr=44100)
    splited_filename = audio[:int(duration_seconds * sr)]  # Truncate the audio signal to the desired duration

    wav_name_with_type = wav_path.split("\\")[-1]
    wav_name_without_type = wav_name_with_type.split(".")[0]

    # path_temp_noises = f'C:\\Users\\hille\\PycharmProjects\\Sentiment-Analysis-Noise_Reduction\\data\\training' \
    #                    f'\\temp_noises'

    path_temp_noises = f'.\\..\\data\\training\\temp_noises'
    if not os.path.exists(path_temp_noises):
        os.mkdir(path_temp_noises)

    path = os.path.join(path_temp_noises, f'{wav_name_without_type}_noised_{duration_seconds}.wav')
    soundfile.write(path, splited_filename, sr)  # Write the truncated audio signal to the temporary WAV file
    return path


def balance_sounds(wav_noise_arr):
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

    if not os.path.exists(os.path.join(directory_path)):
        # create the folder which will contain the noisy data
        os.mkdir(directory_path)

    size_seg_ret, flag_plus = size_seg(wav_dir, count_dir(path_noises))  # find how many wav files will be selected fot each noise
    print(f'{size_seg_ret}%%{flag_plus}')

    counter_segment = 0  # until the size of as segment
    counter_all = 0

    noise_path = os.path.join(path_noises,
                              os.listdir(path_noises)[0])  # create the init path to noise(the first in the list)
    noise = os.listdir(path_noises)[0]

    for w_file in os.listdir(wav_dir):
        w_file_path = os.path.join(wav_dir, w_file)

        if flag_plus:  # if there is one file that is odd from the segments - we skip it
            flag_plus = False
            continue

        if counter_segment == int(size_seg_ret):  # get path for a new noise and init the counter
            if counter_all == count_dir(wav_dir):
                print(f'End of process: {count_dir(wav_dir)} audio files passed with noise!')
            noise = update_noise(os.path.join(noise_path, noise))
            if noise is None:
                print("No more noises!")
                return
            noise_path = os.path.join(path_noises, noise)
            counter_segment = 0

        if get_duration(w_file_path) < get_duration(noise_path):
            new_noise_path = resize_noise(noise_path, int(get_duration(w_file_path)))

        audio_arr, sr1 = librosa.load(w_file_path)  # get the array of numbers which represents the audio
        noise_arr, sr2 = librosa.load(new_noise_path)

        if sr1 != sr2:
            noise_arr_new = librosa.resample(noise_arr, sr2,
                                             sr1)  # Resample audio_arr to the same sample rate as noise_arr

        noise_arr_new = balance_sounds(noise_arr)

        noise_audio = [sum(x) for x in zip(audio_arr, noise_arr_new)]
        path_to_noisy_audio = f'{directory_path}\\noised_{w_file}'
        soundfile.write(path_to_noisy_audio, noise_audio, sr1)  # Save the mixed audio data as a new audio file
        print(f'{counter_all}___{counter_segment} new file {path_to_noisy_audio} was added with {noise} noise')
        counter_segment += 1
        counter_all += 1


if __name__ == '__main__':

    wav_dir = f'.\\..\\data\\training\\Actor_01'  # you can replace the relative path to dir which have audio
    path_noises = f'.\\noises'  # you can change the path to a dir which have noise
    dir_noiser_holdout()
