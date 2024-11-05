import asyncio
import websockets

async def send_wav_file(file_path):
    async with websockets.connect("ws://localhost:8765") as websocket:
        with open(file_path, "rb") as wav_file:
            wav_data = wav_file.read()
            await websocket.send(wav_data)
            print("WAV file sent.")

            # Receive converted FLAC data
            flac_data = await websocket.recv()
            with open("converted.flac", "wb") as flac_file:
                flac_file.write(flac_data)
            print("FLAC file received and saved.")

# Replace 'your_audio.wav' with the path to your WAV file
asyncio.get_event_loop().run_until_complete(send_wav_file("your_audio.wav"))
