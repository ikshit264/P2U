import re
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import subprocess

GEMINI_API_KEY = ''  # Key dal bhadve

prompt = ChatPromptTemplate.from_messages(

    [

    ("system", """generate plantuml code for given statement it must be detailed and self explinatory use only class diagrams make the full database as well as the backend connections for the given statement but all the code must be correct according the plantuml syntax. Also make proper packages and connect them if required"""),

 ("human", "{input}"),

 ]

)

output_parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=GEMINI_API_KEY)
chain = prompt | llm | output_parser

# def run_cli_command(command, capture_output=True, text=True):
#     try:
#         result = subprocess.run(command, capture_output=capture_output, text=text, check=True)  # check=True raises an exception for non-zero return codes
#         return result
#     except subprocess.CalledProcessError as e:
#         print(f"Command failed with return code {e.returncode}:")
#         if capture_output:
#             print(f"Stdout: {e.stdout}")
#             print(f"Stderr: {e.stderr}")
#         raise  # Re-raise the exception if you want the calling code to handle it.
#     except FileNotFoundError:
#         print(f"Command not found: {command}")
#         return None  # Or raise an exception, as appropriate.
#     except Exception as e: # Catch any other potential errors
#         print(f"An unexpected error occurred: {e}")
#         return None

def generate_and_save_plantuml(input_text, filename="diagram.txt"):
    llm_output = chain.invoke({"input": input_text})

    match = re.search(r"(@startuml.*?@enduml)", llm_output, re.DOTALL)
    if match:
        plantuml_code = match.group(1)
        if True:
            try:
                with open(filename, "w") as f:
                    f.write(plantuml_code)
                f.close()
                print(f"PlantUML code saved to {filename}")
                # command = ["python", "-m", "plantuml", f"{filename}"]
                # run_cli_command(command=command)
                return f"PlantUML code saved to {filename}"
            except Exception as e:
                return f"Error saving file: {e}"
        else:
            return "Error: Generated PlantUML is invalid." #Added this part
    else:
        return "Error: Could not extract PlantUML code from LLM response."


# Example usage (same as before):
filename = "diagram.txt"
user_input = "Design the database schema (tables and relationships) for a Bank Management system. Use PlantUML class diagrams"
result_message = generate_and_save_plantuml(user_input, filename=filename)
print(result_message)
