import os
import wave
import time

# iterate over files in that directory
def List_all_audio(directory):
    audio_list=[]
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
                # construct full file path
                filepath = os.path.join(directory, filename)
                audio_info=[]
                try:
                    with wave.open(filepath, 'rb') as wav_file:
                        #print(f'File: {filename}')
                        
                        # get duration in seconds
                        duration_seconds = wav_file.getnframes() / wav_file.getframerate()
                        # convert it to hh:mm:ss format
                        minutes, seconds = divmod(duration_seconds, 60)
                        hours, minutes = divmod(minutes, 60)
                        duration_str = "%02d:%02d:%02d" % (hours, minutes, seconds)
                        #print(f'Duration: {duration_str}')
                        
                        # get modification time
                        mod_time = os.path.getmtime(filepath)
                        # convert it to a readable format
                        mod_time = time.strftime('%Y-%m-%d', time.localtime(mod_time))
                        #print(f'Last modified: {mod_time}')
                        audio_info=[filename,duration_str,mod_time]
                except wave.Error as e:
                    print(f'Could not process file {filename}: {str(e)}')
                audio_list.append(audio_info) 
    return audio_list