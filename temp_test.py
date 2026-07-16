import traceback
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = 'Qwen/Qwen3-0.6B'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype='auto', device_map='auto')
prompt = 'Привет как дела'
messages = [
    {'role': 'system', 'content': 'Ты — ИИ-агроном.'},
    {'role': 'user', 'content': prompt}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
model_inputs = tokenizer([text], return_tensors='pt').to(model.device)
print('device:', model.device)
print('input ids len:', model_inputs.input_ids.shape[1])
try:
    with __import__('torch').no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=40,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    content = tokenizer.decode(output_ids, skip_special_tokens=True).strip('\n')
    print('content:', content)
except Exception as e:
    print('ERROR', repr(e))
    traceback.print_exc()
