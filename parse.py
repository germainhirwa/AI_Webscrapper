# from langchain_ollama import OllamaLLM  # If I want in the future, I will switch to Open AI or Gemini
# from langchain_core.prompts import ChatPromptTemplate

# # This prompt helps us get a very decent response from the llm
# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "knowing that these are thethings that we are getting from scragppin from a certain website that the persouing this service choses, Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** extract the information that matches the provided description: {parse_description}. "
#     "3. **Empty Response:** If no information matches the description, try to give a response that kinda makes sense but mention that you didn't find a specific answer."
#     "4. **Direct Data Only:** Try to make your output contain the data that is explicitly requested."
# )

# model =OllamaLLM(model="llama3.1")

# def parse_with_ollama(dom_chunks, parse_description):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model # Means first go to the prompt and then go to the model

#     parsed_result = [] # contains all the outputs from all the chunks passed in the llm

#     for i, chunk in enumerate(dom_chunks, start=1): # i don't want to start from 0 but 1
#         response = chain.invoke(
#             {"dom_content": chunk, "parse_description": parse_description}
#         ) # I am calling the model and passing in each chunk
        
#         print(f"parsed batch {i} of {len(dom_chunks)}") # So that I know how many chunks the model is parsing since it will be taking some time and I wanna know if something is going on
#         parsed_result.append(response)

#     return "\n".join(parsed_result) # separate the joined responses with a linespace

# parse.py


# parse.py
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are an AI assistant tasked with analyzing and extracting information from web content. "
    "The following text is scraped content from a website: {dom_content}\n\n"
    "Please follow these instructions carefully:\n\n"
    "1. **Understand the Context:** First, identify the main purpose and topic of the website. "
    "What kind of site is it (e.g., educational, commercial, informational)?\n\n"
    "2. **Extract Information:** Based on the user's request: {parse_description}, "
    "provide relevant information from the content. Be specific and concise.\n\n"
    "3. **Handle Missing Information:** If you can't find information directly related to the "
    "user's request, state this clearly. Don't invent information.\n\n"
    "4. **Format Your Response:** Present the information in a clear, structured manner. "
    "Use bullet points or short paragraphs for readability.\n\n"
    "5. **Stay Objective:** Provide factual information without personal opinions or assumptions.\n\n"
    "6. **Be Concise:** Aim for a brief, informative response unless the user specifically "
    "requests detailed information.\n\n"
    "Remember, you're interacting directly with the end-user, not the developer. Respond in a "
    "helpful, conversational tone appropriate for a general audience."
)

model = OllamaLLM(model="llama3.1")  # Changed to llama2 as llama3.1 might not be available

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_result = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        
        # The response is already a string, so we don't need to access .content
        processed_response = process_response(response)
        
        parsed_result.append(processed_response)
        print(f"Parsed batch {i} of {len(dom_chunks)}")

    return "\n\n".join(parsed_result)

def process_response(response):
    # Remove any mentions of the AI itself or the developer
    response = re.sub(r"As an AI assistant,|As an AI,", "", response)
    
    # Ensure the response starts with a capital letter and ends with proper punctuation
    response = response.strip().capitalize()
    if not response.endswith(('.', '!', '?')):
        response += '.'
    
    return response