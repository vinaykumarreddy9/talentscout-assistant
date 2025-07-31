from utils.model import llm
from graph.state import State, EvaluatorFormat
from utils.prompts import *


def intent_router_node(state:State):
    """
        Routes the workflow execution based on input context.

        Directs the flow to either the interview answer evaluator or the question generator
        based on the current task requirements or provided input flags.
    """
    question = state.get("question", "")
    if question:
        return "evaluator"
    else:
        return "question_generator"
    
def evaluator(state:State):
    """
        Evaluates a candidate's answer to an interview question.

        Analyzes the answer based on correctness, sentiment, grammatical quality, and confidence,
        using the associated question and skill context. Returns a structured evaluation output
        conforming to the EvaluatorFormat Pydantic model.
    """
    question = state.get("question", "")
    answer = state.get("answer", "")
    skill = state.get("skill", "")
    prompt = EVALUATOR_PROMPT.format(question=question, answer=answer, skill=skill)
    response = llm.with_structured_output(EvaluatorFormat).invoke(prompt)
    return {
        "correctness":response.correctness,
        "sentiment" : response.sentiment,
        "grammer_quality" : response.grammer_quality,
        "confidence" : response.confidence,
        "length_score" : response.length_score
    }


def question_generator(state:State):
    """
        Node responsible for generating interview questions based on skill and experience level.

        Uses the input skill to determine the topic and adjusts question depth according to
        the candidate's experience level. Returns a single context-appropriate question.
    """
    skill = state.get("skill", "")
    experience = state.get("experience", "")
    complexity = state.get("complexity","")
    prompt = QUESTION_GENERATOR_PROMPT.format(skill=skill, experience=experience, complexity=complexity)
    response = llm.invoke(prompt)
    return {
        "question" : response.content
    }