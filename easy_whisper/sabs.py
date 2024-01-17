from pydub import AudioSegment
from pydub.silence import split_on_silence
    
def split_audio_by_silence(input_file, input_dir, msl, sth):
    tmp_dir = os.path.join(input_dir,'tmp')
    
    audio = AudioSegment.from_file(input_file)

    segments = split_on_silence(
        audio,
        min_silence_len = msl,
        silence_thresh = sth,
        keep_silence = True
    )

    for i, segment in enumerate(segments):
        output_file = os.path.join(tmp_dir,f"{i:02d}-S.wav")
        segment.export(output_file, format="wav")

