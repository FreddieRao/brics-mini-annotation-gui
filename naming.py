# pip install SpeechRecognition pygame keyboard
import os
import pygame
import speech_recognition as sr
import keyboard


# Initialize Pygame for audio playback
pygame.init()
pygame.mixer.init()

def load_names(file_path):
    with open(file_path, 'r') as file:
        names = file.readlines()
    names = [name.strip() for name in names]
    return names

def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def record_audio(output_file):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    # print(audio)
    with open(output_file, "wb") as f:
        f.write(audio.get_wav_data())
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Service unavailable"

def send_control_space():
    keyboard.send("ctrl+space")

def log_video(name, log_file='video_log.txt'):
    with open(log_file, 'a') as file:
        file.write(f'{name}\n')

# Main execution logic
names = load_names('names.txt')
for name in names:
    print(f"Option 1: Load the next name: {name} and play pre-recorded audio")
    print("Option 2: Record a new audio and use speech to text to transcript it to the new name")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        play_audio(f'{name}.mp3')  # Ensure audio files match the name format
    elif choice == '2':
        new_name = record_audio(f'{name}_new.wav')
        log_video(new_name)
    input("Press Enter to continue...")  # Wait for user confirmation
    send_control_space()  # Send ctrl+space to start video recording
    log_video(name)  # Log video details
