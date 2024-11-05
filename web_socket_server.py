import asyncio
import websockets
import soundfile as sf
import numpy as np
import os

async def convert_wav_to_flac(websocket, path):
    async for message in websocket:
        # Save the received audio data to a temporary WAV file
        wav_file_path = "temp.wav"
        with open(wav_file_path, "wb") as wav_file:
            wav_file.write(message)

        # Convert WAV to FLAC
        flac_file_path = "temp.flac"
        try:
            # Read the WAV file and write to FLAC
            data, samplerate = sf.read(wav_file_path)
            sf.write(flac_file_path, data, samplerate, format='FLAC')
            print(f"Converted {wav_file_path} to {flac_file_path}")

            # Read back the FLAC file and send it to the client
            with open(flac_file_path, "rb") as flac_file:
                flac_data = flac_file.read()
                await websocket.send(flac_data)
        except Exception as e:
            print(f"Error converting file: {e}")
            await websocket.send(b"Error converting file.")

        # Clean up temporary files
        os.remove(wav_file_path)
        if os.path.exists(flac_file_path):
            os.remove(flac_file_path)

start_server = websockets.serve(convert_wav_to_flac, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_forever()
