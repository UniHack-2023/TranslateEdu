import flask
import whisper

model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

   from flask import *
        app = flask.Flask(__name__)
        app.config.from_object('config')                          
        @app.route('/', methods=['GET','POST'])
        def new_task():
            if flask.request.method == 'POST':
               tts = flask.request.form['tts']
            if int(tts) == 3:
               return redirect("/tts1")
            function()
                flask.flash(str(tts)+'is being selected')
                   print str(tts)+"output"
            else:
               flask.flash('Parakrant ---->')
                return flask.render_template("tasks.html")
            return redirect('/') 
    @app.route('/tts1')
    def wav():
        print "wavfile reached"
        return flask.render_template("s1.html")