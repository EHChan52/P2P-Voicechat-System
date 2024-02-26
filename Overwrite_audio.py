import wave

def Overwrite_audio(target_file, source_file, overwrite_start_time):
    # time in seconds
    output_file = 'overwrited_' + target_file

    with wave.open(source_file, 'rb') as input_wave:
        
        source_params = input_wave.getparams()

        source_frames = input_wave.readframes(source_params.nframes)

    with wave.open(target_file, 'rb') as input_wave:
        
        target_params = input_wave.getparams()

        target_end_frame = int(overwrite_start_time * target_params.framerate)

        front_target_frames = input_wave.readframes(target_end_frame)

        input_wave.setpos(target_end_frame + source_params.nframes)

        back_target_frames = input_wave.readframes(target_params.nframes - input_wave.tell())

    with wave.open(output_file, 'wb') as output_wave:
        
        output_wave.setparams(target_params)
        
        overwrited_frames = front_target_frames + source_frames + back_target_frames

        output_wave.writeframes(overwrited_frames)
    return None
