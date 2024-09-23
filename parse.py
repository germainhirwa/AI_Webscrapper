from langchain_ollama import OllamaLLM  # If I want in the future, I will switch to Open AI or Gemini
from langchain_core.prompts import ChatPromptTemplate

# This prompt helps us get a very decent response from the llm
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "knowing that these are thethings that we are getting from scragppin from a certain website that the persouing this service choses, Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** extract the information that matches the provided description: {parse_description}. "
    "3. **Empty Response:** If no information matches the description, try to give a response that kinda makes sense but mention that you didn't find a specific answer."
    "4. **Direct Data Only:** Try to make your output contain the data that is explicitly requested."
)

model =OllamaLLM(model="llama3.1")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model # Means first go to the prompt and then go to the model

    parsed_result = [] # contains all the outputs from all the chunks passed in the llm

    for i, chunk in enumerate(dom_chunks, start=1): # i don't want to start from 0 but 1
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        ) # I am calling the model and passing in each chunk
        
        print(f"parsed batch {i} of {len(dom_chunks)}") # So that I know how many chunks the model is parsing since it will be taking some time and I wanna know if something is going on
        parsed_result.append(response)

    return "\n".join(parsed_result) # separate the joined responses with a linespace

