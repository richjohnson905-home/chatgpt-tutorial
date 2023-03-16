import openai
import os
import gradio as gr

openai.api_key = os.getenv("OPENAI_API_KEY")

message_history = []
# message_history = [{"role": "user", 
                    # "content": "You are a joke bot. I will specify the subject matter in my messages, \
                    #     and you will reply with a joke that includes the subjects I mention in my \
                    #     messages. Reply only with jokes to further input. If you understand, say OK"
                    # },
                    # {"role": "assistant", 
                    #  "content": "OK"}]

def predict(input):
    # tokenize the input sentence
    message_history.append({"role": "user", "content": f"{input}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for  i in range(0, len(message_history)-1, 2)]
    return response

# def chat(inp, role="user"):
#     message_history.append({"role": role, "content": inp})
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=message_history
#     )
#     reply_content = completion.choices[0].message.content
#     print(reply_content)
#     message_history.append({"role": "assistant", "content": reply_content})
#     return reply_content


def main():
    # for i in range(2):
    #     user_input = input(">: ")
    #     print("User's input was", user_input)
    #     print()
    #     chat(user_input)
    #     print()
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        with gr.Row():
            txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
        txt.submit(predict, txt, chatbot)
        txt.submit(None, None, txt, _js="() => {''}")
    demo.launch() 


if __name__ == "__main__":
    main()