import customtkinter as cstk
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

voices_id = {
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Callum": "N2lVS1w4EtoT3dr4eOWO",
    "Charlotte": "XB0fDUnXU5powFXDhCwa",
    "Matilda": "XrExE9yKIg1WjnnlVkGX"
}


def text_to_speech_file(text: str, id: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path


cstk.set_appearance_mode("system")
cstk.set_default_color_theme("dark-blue")

root = cstk.CTk()
root.title("TTS Generator")
root.geometry("1000x700")
root.resizable(True, True)

# Variable to store the selected voice ID
selected_voice_id = cstk.StringVar(value=voices_id["Adam"])

# Create and place the label
label = cstk.CTkLabel(root, text="Selected Voice:")
label.grid(row=0, column=1, padx=(0, 30), pady=10, sticky='w')
label.configure(font=("Arial", 20))


# Create and place the combo box
def combobox_callback(choice):
    selected_voice_id.set(voices_id[choice])
    print("combobox dropdown clicked:", choice, "with ID:", selected_voice_id.get())


combobox = cstk.CTkComboBox(root, values=list(voices_id.keys()), command=combobox_callback,
                            variable=cstk.StringVar(value="Adam"))
combobox.configure(state="readonly",height=10, font=("Arial", 20))
combobox.grid(row=0, column=1, padx=(150, 20), pady=10, sticky='w')  # Place combo box in the second column

textbox = cstk.CTkTextbox(root)
textbox.insert("0.0", "new text to insert")  # insert at line 0 character 0
textbox.delete("0.0", "end")  # delete all text
textbox.configure(state="normal", width=450, font=("Italic", 20),
                  scrollbar_button_color="#301934", scrollbar_button_hover_color="purple")
textbox.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 50), sticky='nsew')

button = cstk.CTkButton(root, text="Generate",
                        command=lambda: text_to_speech_file(textbox.get("0.0", "end").strip(), selected_voice_id.get()))
button.configure(state="normal", width=250, height=100, font=("Arial", 20))
button.grid(row=2, column=0, columnspan=2, pady=(0, 50))

# Configure grid row and column weights to make the layout responsive
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
