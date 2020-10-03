from starlette.applications import Starlette
from starlette.responses import UJSONResponse
import uvicorn
import os
import gc
from aitextgen import aitextgen

def start_model():
    #ai = aitextgen(tf_gpt2="124M", to_gpu=False)
    ai = aitextgen(model="trained_model/pytorch_model.bin", config="trained_model/config.json", to_gpu=False)
    return ai

def kw2lyrics(keywords,temperature=0.7,repetition_penalty=1):
  song = ai.generate_one(prompt=f"KW: {keywords}\\n", temperature=temperature,top_k=40,repetition_penalty=repetition_penalty)
  return song.replace("\\n","\n")

app = Starlette(debug=False)
ai = start_model()

# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*'
}

@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def homepage(request):
    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()
    elif request.method == 'HEAD':
        return UJSONResponse({'text': ''},
                             headers=response_header)

    text = kw2lyrics(params.get('prefix', '')[:500],temperature=float(params.get('temperature', 0.7)),repetition_penalty=float(params.get('repetition', 1.0)))

    '''
    length=int(params.get('length', 1023))
    top_k=int(params.get('top_k', 0))
    top_p=float(params.get('top_p', 0))
    '''

    gc.collect()
    return UJSONResponse({'text': text},
                         headers=response_header)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
