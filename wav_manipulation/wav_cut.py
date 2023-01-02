from pydub import AudioSegment
import pandas as pd
import math


def single_split_by_ms(from_ms, to_ms, split_filename, file_path):
    filepath = file_path + '\\' + split_filename
    audio = AudioSegment.from_wav(filepath)
    new_split_filename = audio[int(from_ms):int(to_ms)]
    interval = f'_{from_ms}_{to_ms}'  # mcreate for the path of the new file
    my_path = "C:\\Users\\hille\\Documents\\University\\third year\\first semster\\language procces and sound blocks\\wav_file\\" + split_filename.split('.')[0] + interval + ".wav"
    new_split_filename.export(my_path, format="wav")
#'21:34:14.245'

def h_to_ms(str_hour):
    save_string_hour = str_hour
    str_hour = str_hour.split(':')  # get the three parts: hour, minute, second+ms **(the seconds and ms will be split by '.')
    hours = int(str_hour[0]) * 1000 * 60 * 60
    minutes = int(str_hour[1]) * 1000 * 60
    seconds = int((str_hour[2].split('.'))[0])* 1000 * 1
    ms = int((str_hour[2].split('.'))[1]) * 1
    sum = hours + minutes + seconds + ms
    # the sum of the ms we convert hour to ms + min to ms + second to ms + ms to ms (which is the specific amount of ms)
    return (sum, save_string_hour)

#there are 60*60*1000 ms in one hour
#there are 60*1000 ms in one minutes
#there are 1000 ms in one second
'''
def ms_to_string(ms):
    #calculate hour
    hour = 0
    if ms >= 60*60*1000: #if the ms can create an hour and if not : hour = 0
        while ms - 3600 * 1000 * hour > 0: #if the ms can create more that one hour and return the total hours
            hour += 1
    tot_h = hour
    ms = ms - (60 * 60 * 1000 * tot_h)
    print(f'ms - (60 * 60 * 1000 * tot_h) = {ms}' )

    # calculate minute
    minute = 0
    if ms >= 60*1000:
        while ms - 60 * 1000 * minute > 0:
            minute += 1
    tot_m = minute
    ms = ms - (60 * 1000 * tot_m)
    print(f'ms - (60 * 1000 * tot_m) = {ms}')

    # calculate second
    second = 0
    if ms >= 1000:
        while ms - 1000 * second > 0:
            second += 1
    tot_s = second
    ms = ms - (1000 * tot_s)
    print(f'ms - (1000 * tot_s) = {ms}')

    # calculate ms
    tot_ms = ms
    print(f'ms = {ms}')

    print(f'{tot_h}:{tot_m}:{tot_s}:{tot_ms}')
    return f'{tot_h}:{tot_m}:{tot_s}:{tot_ms}'
'''



def multi_split(list_of_times, audio_file, audio_path):  # give a list of time's interval which convert to ms and split.
    for i in range(len(list_of_times) - 1):
        # single_split_by_ms(self, int(fromH_to_S(list_of_times[i])), int(fromH_to_S(list_of_times[i+1])), audio_file)
        single_split_by_ms(int(list_of_times[i]), int(list_of_times[i + 1]), audio_file, audio_path, )


def convert_csv(path_csv_file):
    csv_df = pd.read_csv(path_csv_file, names= ['Utterance', 'Speaker', 'Emotion', 'Scene_ID', 'Utterance_ID', 'Season', 'Episode', 'Start_Time', 'End_Time'], skiprows=[0])
    utterance = csv_df['Utterance'].tolist()
    start_Time = csv_df['Start_Time'].tolist()
    end_Time = csv_df['End_Time'].tolist()
    print(utterance)
    print(start_Time)
    print(end_Time)
    print(h_to_ms(start_Time[2]))

if __name__ == '__main__':
    folder = "C:\\Users\\hille\\Documents\\University\\third year\\first semster\\language procces and sound blocks\\wav_file"
    file = "megadeth.wav"

    # spliter.single_split_by_ms(0, (spliter.get_duration()/2)*1000, file, folder)
    #multi_split([4, 800, 3, 323, 2345, 3423], file, folder)
    h_to_ms('4:50:32.67')
    print(h_to_ms('4:50:32.67')[1])
    #folder1 = "C:\\Users\\hille\\Documents\\University\\third year\\first semster\\language procces and sound blocks\\dataset-friends.csv"
    #convert_csv(folder1)
