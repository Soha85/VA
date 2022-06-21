import json
import speech_recognition as sr
import os
import sys
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave


def get_vosk(f):
  SetLogLevel(-1)

  if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

  wf = wave.open(f, "rb")
  if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

  model = Model("model")
  rec = KaldiRecognizer(model, wf.getframerate())
  rec.SetWords(True)
  
  results = []
  while True:
    data = wf.readframes(4000)
    if len(data) == 0:
      break  
    if rec.AcceptWaveform(data):
      part_result = json.loads(rec.Result())
      results.append(part_result)
  part_result = json.loads(rec.FinalResult())
  results.append(part_result)
  txt = ""
  for r in results:
    txt = txt + ' ' + r.get('text')
    txt = txt.strip()
  return results, txt

def ST(f):
  try:
    text = ""
    AUDIO_FILE = (str(f))
    analysis , text = get_vosk(AUDIO_FILE)
    return json.dumps({"transcript analysis": analysis, "transcript": text})
  except Exception as err:
    return {"error": str(err)}

if __name__ == "__main__":
    try:
      if (len(sys.argv) > 1):
        ff = sys.argv[1]
        f = sys.argv[1].find('.')
        n = len(sys.argv)
        for i in range(n):
        if (f == -1):
          ff = ff + ".wav"
        obj = ST(ff)
        print(obj)

    except Exception as err:
        print({"error": str(err)})