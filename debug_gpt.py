import traceback
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print('start')
model_name = 'distilgpt2'
print('loading tokenizer')
tokenizer = AutoTokenizer.from_pretrained(model_name)
print('loading model')
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32, device_map=None)
model.to('cpu')
print('model loaded')
prompt = 'Привет'
prompt_text = f'Сделай короткий ответ на русском: {prompt}'
print('tokenizing')
model_inputs = tokenizer([prompt_text], return_tensors='pt')
model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}
print('generating')
try:
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=20,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    print('generated')
    output_ids = generated_ids[0][len(model_inputs['input_ids'][0]):].tolist()
    content = tokenizer.decode(output_ids, skip_special_tokens=True).strip('\n')
    print('content:', content)
except Exception as e:
    print('ERROR', repr(e))
    traceback.print_exc()
