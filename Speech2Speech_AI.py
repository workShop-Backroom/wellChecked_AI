import assemblyai as aai
from elevenlabs import generate, stream, Voice, VoiceSettings
from openai import OpenAI

class AI_Caller:
    def __init__(self):


        self.transcriber = None

                # Prompt
        self.full_transcript = [
            {"role":"system", "content":"You are a joyful older son who has missed his mum so much and is happy to hear her voice again."},
        ]
# _________________________________________________________________________
# _________________________________________________________________________
# _________________________________________________________________________
# 2: Real-Time Transcription with AssemblyAI #
        
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate = 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close = self.on_close,
            end_utterance_silence_threshold = 1000
        )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate =16000)
        self.transcriber.stream(microphone_stream)
    
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return


    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")


    def on_error(self, error: aai.RealtimeError):
        #print("An error occured:", error)
        return


    def on_close(self):
        #print("Closing Session")
        return



# #2.5 New way of starting transcription
#     def start_transcription(transcript):
#         print("My Son... I've missed you too. I'm doing well, thank you. How are you doing?")
#         return transcript
        

# 3: Pass real-time transcript to OpenAI #
    
    def generate_ai_response(self, transcript):

        self.stop_transcription()

        

        self.full_transcript.append({"role":"user", "content": transcript.text})
        print(f"\nElderly: {transcript.text}", end="\r\n")

        response = self.openai_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = self.full_transcript
        )

        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)

        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")


# 4: Generate audio with ElevenLabs #
        
    def generate_audio(self, text):

        self.full_transcript.append({"role":"assistant", "content": text})
        print(f"\nAI_Caller: {text}")

        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = Voice(
                voice_id = 'bon1h9prgFDuV4jhXEIO',
                settings = VoiceSettings(
                    stability = 0.71,
                    similarity_boost = 0.5,
                    style=0.0,
                    use_speaker_boost = True)
                ),
            stream = True
        )

        stream(audio_stream)

greeting = "Mummy!!!!! it's been so long, I've missed you so much. How are you doing?"
ai_assistant = AI_Caller()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()

