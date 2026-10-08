from io import BytesIO
import re
from flask import Flask, render_template, request, send_file
from pdf_builder import build_pdf, CONCEPTS, ACTIVITY_LIMIT, LayoutError

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

@app.get('/')
def index():
    return render_template('index.html', concepts=CONCEPTS, activity_limit=ACTIVITY_LIMIT)

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/generate')
def generate():
    data = {k: v.strip() for k,v in request.form.items()}
    data['concepts'] = request.form.getlist('concepts')
    def error(message):
        return {'error':message}, 400
    if not re.fullmatch(r'[0-9]{1,2}',data.get('group_no','')) or not 1 <= int(data['group_no']) <= 99:
        return error('조 번호는 1~99 사이의 숫자를 입력해주세요.')
    data['group_no'] = int(data['group_no'])
    limits = {'team_name':20,'members':100, **{r:20 for r in ['leader','budget','insight_1','insight_2','schedule','photo','report_1','report_2']}, **{f'place_{i}':40 for i in range(3)}, **{f'activity_{i}':ACTIVITY_LIMIT for i in range(3)}}
    required = ['team_name','members','leader','budget','insight_1','schedule','photo','report_1'] + [f'{prefix}_{i}' for i in range(3) for prefix in ['place','activity']]
    for key in required:
        if not data.get(key): return error('필수 입력 항목을 모두 작성해주세요.')
    for key, limit in limits.items():
        if len(data.get(key,'')) > limit: return error(f'{key} 항목은 공백 포함 {limit}자 이내로 작성해주세요.')
    members = [n.strip() for n in data['members'].split(',') if n.strip()]
    if not 1 <= len(members) <= 8: return error('조원 이름은 최대 8명을 쉼표로 구분해주세요.')
    if not data['concepts'] or any(v not in ['0','1','2','3','4'] for v in data['concepts']):
        return error('탐방 컨셉을 한 개 이상 선택해주세요.')
    if any(ord(c)<32 and c!='\n' for k,v in data.items() if isinstance(v,str) for c in v):
        return error('지원하지 않는 제어문자가 있습니다.')
    try:
        pdf = build_pdf(data)
    except LayoutError as exc:
        return error(str(exc))
    safe_name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', '_', data['team_name']).strip(' .') or '조이름'
    filename = f"현장체험계획서_{data['group_no']}조_{safe_name}.pdf"
    response = send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name=filename)
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
