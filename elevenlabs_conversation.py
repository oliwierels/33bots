import os
import queue
import signal
import threading

import sounddevice as sd
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import AudioInterface, Conversation

API_KEY = os.environ["ELEVENLABS_API_KEY"]
AGENT_ID = os.environ["ELEVENLABS_AGENT_ID"]


class SoundDeviceAudioInterface(AudioInterface):
    INPUT_CHUNK = 4000   # 250ms @ 16kHz
    OUTPUT_CHUNK = 1000  # 62.5ms @ 16kHz

    def __init__(self):
        self._input_callback = None
        self._output_queue: queue.Queue[bytes] = queue.Queue()
        self._should_stop = threading.Event()
        self._in_stream = None
        self._out_stream = None
        self._output_thread = None

    def start(self, input_callback):
        self._input_callback = input_callback
        self._should_stop.clear()

        self._in_stream = sd.RawInputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=self.INPUT_CHUNK,
            callback=self._sd_input_callback,
        )
        self._out_stream = sd.RawOutputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=self.OUTPUT_CHUNK,
        )

        self._in_stream.start()
        self._out_stream.start()
        self._output_thread = threading.Thread(target=self._run_output, daemon=True)
        self._output_thread.start()

    def stop(self):
        self._should_stop.set()
        if self._output_thread is not None:
            self._output_thread.join()
        if self._in_stream is not None:
            self._in_stream.stop()
            self._in_stream.close()
        if self._out_stream is not None:
            self._out_stream.stop()
            self._out_stream.close()

    def output(self, audio: bytes):
        self._output_queue.put(audio)

    def interrupt(self):
        try:
            while True:
                self._output_queue.get_nowait()
        except queue.Empty:
            pass

    def _sd_input_callback(self, indata, frames, time, status):
        if status:
            print(f"[Audio input] {status}")
        self._input_callback(bytes(indata))

    def _run_output(self):
        while not self._should_stop.is_set():
            try:
                audio = self._output_queue.get(timeout=0.25)
                self._out_stream.write(audio)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"[Audio output error] {e}")
                break


def main():
    client = ElevenLabs(api_key=API_KEY)
    audio_interface = SoundDeviceAudioInterface()
    _stop_event = threading.Event()

    conversation = Conversation(
        client=client,
        agent_id=AGENT_ID,
        requires_auth=False,
        audio_interface=audio_interface,
        callback_agent_response=lambda text: print(f"Agent: {text}"),
        callback_user_transcript=lambda text: print(f"Ty: {text}"),
    )

    def on_interrupt(sig, frame):
        print("\nKoncze rozmowe...")
        _stop_event.set()

    signal.signal(signal.SIGINT, on_interrupt)

    try:
        conversation.start_session()
    except Exception as e:
        print(f"Blad podczas uruchamiania sesji: {e}")
        return

    print("Rozmowa rozpoczeta - mow swobodnie! (Ctrl+C aby zakonczyc)")

    def _watch_stop():
        _stop_event.wait()
        conversation.end_session()

    threading.Thread(target=_watch_stop, daemon=True).start()

    conversation_id = conversation.wait_for_session_end()
    print(f"Rozmowa zakonczona. ID: {conversation_id}")


if __name__ == "__main__":
    main()
