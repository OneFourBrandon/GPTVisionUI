import openai as openai
import customtkinter as ctk


# Globals
global token_label
global token_slider
global gpt_textbox
global prompt_entry
global image_entry


# Generates an AI output from an image and prompt using GPT Vision
def generate_output(prompt, image_url, max_tokens):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        temperature=0.3,  # TODO Make this editable later
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


# Grabs OpenAI api key from a file
def get_api_key():
    key_file = open('api_key.txt', 'r')
    return key_file.readline()


# Changes the token text to the value of the sliderf
def change_token_text(slider_value):
    token_string = "Tokens: " + str(int(slider_value))
    token_label.configure(text=token_string)


# Calls a prompt generation and edits the gpt_textbox
def generate_pressed():
    prompt = prompt_entry.get("0.0", "end")
    image_url = image_entry.get()
    tokens = int(token_slider.get())
    result = generate_output(prompt, image_url, tokens)

    # textbox shit
    gpt_textbox.configure(state="normal")
    gpt_textbox.delete("0.0", "end")
    gpt_textbox.insert("0.0", result)
    gpt_textbox.configure(state="disabled")


if __name__ == '__main__':
    client = openai.OpenAI(api_key=get_api_key())

    # Window
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    window = ctk.CTk()
    window.geometry("720x600")
    window.title("GPT-4-Vision GUI")

    # Frame
    frame = ctk.CTkFrame(master=window)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Labels and entries
    prompt_label = ctk.CTkLabel(master=frame, text="Enter Prompt:")
    prompt_label.pack(anchor="w", padx=10, pady=6)

    prompt_entry = ctk.CTkTextbox(master=frame, width=680, height=70)
    prompt_entry.pack(anchor="w", padx=10)

    image_label = ctk.CTkLabel(master=frame, text="Enter Image URL:")
    image_label.pack(anchor="w", padx=10, pady=6)

    image_entry = ctk.CTkEntry(master=frame, width=680)
    image_entry.pack(anchor="w", padx=10)

    token_label = ctk.CTkLabel(master=frame, text="Tokens: 100")
    token_label.pack(anchor="w", padx=10, pady=6)

    token_slider = ctk.CTkSlider(master=frame, from_=30, to=2000, number_of_steps=500, width=680, command=change_token_text)
    token_slider.pack(anchor="w", padx=10, pady=6)
    token_slider.set(100)

    generate_button = ctk.CTkButton(master=frame, text="Generate", command=generate_pressed)
    generate_button.pack(anchor="w", padx=10, pady=8)

    gpt_textbox = ctk.CTkTextbox(master=frame, width=680, height=300, state="disabled")
    gpt_textbox.pack(anchor="w", padx=10, pady=9)

    window.mainloop()