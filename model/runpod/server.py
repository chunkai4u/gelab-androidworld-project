import base64, io, os, threading, time
import torch
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

MODEL_PATH = os.environ.get('GELAB_MODEL_PATH', '/workspace/gelab/model')
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = Qwen3VLForConditionalGeneration.from_pretrained(MODEL_PATH, torch_dtype=torch.bfloat16, device_map='auto', attn_implementation='sdpa')
model.eval()
lock = threading.Lock()
app = FastAPI()
class StepRequest(BaseModel):
    task: str
    image_base64: str
    history: str = ''
    max_new_tokens: int = Field(default=512, ge=1, le=1024)
@app.get('/health')
def health():
    return {'model':'GELab-Zero-4B-preview','device':str(model.device),'ready':True}
@app.post('/step')
def step(req: StepRequest):
    image = Image.open(io.BytesIO(base64.b64decode(req.image_base64))).convert('RGB')
    prompt = open('/workspace/gelab/prompt.txt').read()
    messages = [{'role':'user','content':[{'type':'text','text':prompt+'\nTask: '+req.task+'\nHistory: '+req.history},{'type':'image','image':image},{'type':'text','text':'Return your next action in the specified tab-separated format, including action and point or value as appropriate.'}]}]
    with lock:
        started=time.time()
        inputs=processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors='pt').to(model.device)
        with torch.inference_mode():
            generated=model.generate(**inputs, max_new_tokens=req.max_new_tokens, do_sample=False)
        output=processor.batch_decode(generated[:, inputs['input_ids'].shape[-1]:], skip_special_tokens=True)[0]
    return {'output':output,'seconds':round(time.time()-started,2),'model':'GELab-Zero-4B-preview'}
if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=11435)
