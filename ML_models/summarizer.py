# To load summarizer model that summarizes text given a context
from transformers import pipeline

inference_model_summarize = pipeline("summarization", model="t5-base", tokenizer="t5-base")