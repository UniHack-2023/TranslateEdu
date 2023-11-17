# import all the modules that we will need to use
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

path = "D:\TTS\TTS\.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])
syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)
txt_file_path = input("Text file:")
with open(txt_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

outputs = syn.tts(text)
syn.save_wav(outputs, "audio-1.wav")