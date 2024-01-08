# To load and create a inference function for QnA when given a context
from transformers import pipeline

model_checkpoint = "consciousAI/question-answering-roberta-base-s-v2"
question_answerer = pipeline("question-answering", model=model_checkpoint)


def inference_model_qna(question, context):
    answer = question_answerer(question=question, context=context)
    return answer


    