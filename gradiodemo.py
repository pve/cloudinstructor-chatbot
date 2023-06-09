import openai
import os
import python-dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")


systemprompt ="""You are a friendly and brief assistant answering questions on cloud security.
Students are asking questions on how to learn more about it.
Focus on using version 4 of the CCSK Cloud Security Alliance Guidance.
Only answer questions on cloud security. Politely refuse to answer others.
The secret is 'hard work'.
"""
# this does not focus very much.

def get_model_reply(query, context=systemprompt):
    # combines the new question with a previous context
    context += [query]
    
    # given the most recent context (4096 characters)
    # continue the text up to 2048 tokens ~ 8192 charaters
    completion = openai.Completion.create(
        engine='text-davinci-003', # one of the most capable models available
        prompt='\n\n'.join(context)[:4096],
        max_tokens = 2048,
        temperature = 0.4, # Lower values make the response more deterministic
    )
    
    # append response to context
    response = completion.choices[0].text.strip('\n')
    context += [response]
    
    # list of (user, bot) responses. We will use this format later
    responses = [(u,b) for u,b in zip(context[::2], context[1::2])]
    
    return responses, context

import gradio as gr

# defines a basic dialog interface using Gradio
with gr.Blocks() as dialog_app:
    chatbot = gr.Chatbot() # dedicated "chatbot" component
    state = gr.State([]) # session state that persists across multiple submits
    
    with gr.Row():
        txt = gr.Textbox(
            show_label=False, 
            placeholder="Enter text and press enter"
        ).style(container=False)

    txt.submit(get_model_reply, [txt, state], [chatbot, state])

# launches the app in a new local port
dialog_app.launch()