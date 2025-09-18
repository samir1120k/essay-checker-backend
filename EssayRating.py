from langgraph.graph import StateGraph, START ,END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from pydantic import BaseModel ,Field
import operator

load_dotenv()

model=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

class EvaluationSchema(BaseModel):
    feedback: str=Field(description='Detailed Feedback for the essay')
    score:int=Field(description='Score out of 10',ge=0,le=10)



structure_model=model.with_structured_output(EvaluationSchema)

class feedbackState(TypedDict):

    essay:str
    language_feedback:str
    analysis_feedback:str
    clarity_feedback:str
    overall_feedback:str

    individual_score:Annotated[list[int],operator.add]
    avg_score:float


def evaluate_language(state:feedbackState):
    prompt=f'Evaluate the language Quality of following essay and Provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output =structure_model.invoke(prompt)
    return {'language_feedback':output.feedback,'individual_score':[output.score]}

def evaluate_analysis(state:feedbackState):
    prompt=f'Evaluate the Depth of analysis of following essay and Provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output =structure_model.invoke(prompt)
    return {'analysis_feedback':output.feedback,'individual_score':[output.score]}

def evaluate_thought(state:feedbackState):
    prompt=f'Evaluate the clarity of thought of following essay and Provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output =structure_model.invoke(prompt)
    return {'clarity_feedback':output.feedback,'individual_score':[output.score]}

def final_evaluation(state:feedbackState):
    # Geneting the overall feedback
    prompt=f'Based on the following feedbacks create a summrize feedback \n language feedback -{state['language_feedback']} \n depth of analysis feedback -{state["analysis_feedback"]} \n clarity of thought feedback -{state["clarity_feedback"]}'
    overall_feedback=model.invoke(prompt)

    #average the overall score
    avg_score=sum(state["individual_score"])/len(state["individual_score"])
    return {'overall_feedback':overall_feedback, 'avg_score':avg_score}


graph=StateGraph(feedbackState)

graph.add_node('evaluate_language',evaluate_language)
graph.add_node('evaluate_thought',evaluate_thought)
graph.add_node('evaluate_analysis',evaluate_analysis)
graph.add_node('final_evaluation',final_evaluation)

graph.add_edge(START,'evaluate_language')
graph.add_edge(START,'evaluate_thought')
graph.add_edge(START,'evaluate_analysis')

graph.add_edge('evaluate_language','final_evaluation')
graph.add_edge('evaluate_thought','final_evaluation')
graph.add_edge('evaluate_analysis','final_evaluation')

graph.add_edge('final_evaluation',END)

workflow=graph.compile()

# essay="""Artificial Intelligence (AI) has become one of the most influential technologies of the 21st century, shaping the way people live, work, and interact with the world. At its core, AI refers to computer systems designed to perform tasks that normally require human intelligence, such as recognizing speech, analyzing data, making decisions, and even understanding natural language.

# One of AI’s greatest strengths lies in its ability to process vast amounts of information quickly and accurately. In medicine, for example, AI helps doctors detect diseases earlier by analyzing medical images and patient records. In business, AI-driven tools predict market trends, optimize supply chains, and enhance customer service. Even in everyday life, AI powers virtual assistants, recommendation systems, and smart devices that simplify routine tasks.

# However, the rise of AI also brings important challenges. Concerns about privacy, job displacement, and ethical decision-making must be addressed to ensure the technology benefits society as a whole. Governments, companies, and researchers are now working together to create guidelines that balance innovation with responsibility.

# In conclusion, AI is not just a technological trend but a transformative force. If developed and used wisely, it has the potential to solve complex global problems and improve human life in countless ways. Yet, its success will depend on how humanity chooses to guide its growth, ensuring that AI remains a tool that supports human progress rather than replaces it."""

#Testing of out model
# initial_state={
#     'essay': essay
# }

# print(workflow.invoke(initial_state))