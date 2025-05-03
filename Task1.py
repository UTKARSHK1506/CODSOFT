from transformers import BertForQuestionAnswering, BertTokenizer
from transformers.utils import logging
import torch

# Suppress unnecessary warnings
logging.set_verbosity_error()

# Model name
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

# Load the model and tokenizer
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Context: Development of Artificial Intelligence
ai_development_history = """
Artificial Intelligence (AI) is a branch of computer science focused on creating machines capable of performing tasks that typically require human intelligence.
The field began in the 1950s with pioneers like Alan Turing and John McCarthy, the latter coining the term "Artificial Intelligence" in 1956.
Over the decades, AI has evolved through symbolic reasoning, expert systems in the 1980s, and machine learning techniques in the 1990s.
A major leap occurred in the 2010s with the rise of deep learning, enabled by powerful GPUs and large datasets.
Breakthroughs like AlphaGo, GPT models, and BERT have demonstrated the practical power of AI in areas like language, vision, and decision-making.
Today, AI is applied across industries, from healthcare and finance to autonomous vehicles and creative arts.
"""

# FAQ Bot Function
def faq_bot(question):
    context = ai_development_history
     
    # Encode the question and context
    input_ids = tokenizer.encode(question, context)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    
    # Segment IDs for BERT
    sep_idx = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_idx + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    
    # Get model outputs
    output = model(input_ids=torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))
    ans_start = torch.argmax(output.start_logits)
    ans_end = torch.argmax(output.end_logits)
    
    # Handle case where no valid answer is found
    if ans_end >= ans_start:
        answer = ' '.join(tokens[ans_start:ans_end + 1])
    else:
        return "I don't know the answer to this question."

    # Clean up token formatting
    corrected_ans = ''
    for word in answer.split():
        if word.startswith("##"):
            corrected_ans += word[2:]
        else:
            corrected_ans += ' ' + word
    
    return corrected_ans.strip()


# Example questions
questions = [
    "Who coined the term Artificial Intelligence?",
    "When did AI begin?",
    "What breakthrough occurred in the 2010s?",
    "Name some applications of AI.",
    "Who were the pioneers of AI?"
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {faq_bot(q)}\n")
