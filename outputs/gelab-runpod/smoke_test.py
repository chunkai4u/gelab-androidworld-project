"""Synthetic screen test only; this is not an AndroidWorld evaluation."""
import base64, io, json, urllib.request
from PIL import Image, ImageDraw, ImageFont
img=Image.new('RGB',(540,960),'white')
d=ImageDraw.Draw(img)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
d.text((25,50),'Settings',font=f,fill='black')
d.text((25,150),'Wi-Fi',font=f,fill='black')
d.text((25,200),'Off',font=f,fill='black')
d.rounded_rectangle((405,150,505,205),radius=25,fill='#aaaaaa')
d.ellipse((410,155,455,200),fill='white')
img.save('/workspace/gelab/synthetic_wifi.png')
b=io.BytesIO(); img.save(b,format='PNG')
payload={'task':'Turn Wi-Fi on.','image_base64':base64.b64encode(b.getvalue()).decode(),'max_new_tokens':384}
request=urllib.request.Request('http://127.0.0.1:11435/step',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(request,timeout=180) as r: result=json.load(r)
open('/workspace/gelab/smoke_result.json','w').write(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
