# To load and create a inference function for QnA when given a context
from transformers import pipeline

inference_model_qna = pipeline("question-answering", model="deepset/roberta-base-squad2")

