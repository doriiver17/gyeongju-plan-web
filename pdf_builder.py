from pathlib import Path
import fitz

BASE = Path(__file__).resolve().parent
CONCEPTS = ['활기찬 일자리·경제', '소통배려 지역공동체', '글로벌 교육문화', '미래지향 도시유일성', '희망나눔 행복동행']
ACTIVITY_LIMIT = 60

class LayoutError(ValueError):
    pass

def build_pdf(data):
    with fitz.open(BASE / 'assets/plan_template.pdf') as doc:
        page = doc[0]
        width, height = page.rect.width, page.rect.height
        sx, sy = width / 1273, height / 1800
        fonts = {key: fitz.Font(fontfile=str(BASE / 'assets/fonts' / name)) for key, name in [('medium', 'Pretendard-Medium.otf'), ('extra', 'Pretendard-ExtraBold.otf')]}
        for key, font in fonts.items():
            page.insert_font(fontname=key, fontbuffer=font.buffer)
        color = (69/255, 68/255, 62/255)

        def place(text, box, size=11, align='center'):
            if not text:
                return
            x1,y1,x2,y2 = box
            x1,x2,y1,y2 = x1*sx,x2*sx,y1*sy,y2*sy
            font = fonts['medium']
            while size >= 7:
                lines, line = [], ''
                for char in text:
                    if char == '\n':
                        lines.append(line); line = ''; continue
                    if line and font.text_length(line+char,fontsize=size) > x2-x1-10:
                        lines.append(line); line = char
                    else:
                        line += char
                lines.append(line)
                if len(lines)*size*1.35 <= y2-y1-4:
                    break
                size -= .25
            else:
                raise LayoutError('입력 내용이 PDF 칸에 들어가지 않습니다. 내용을 줄여주세요.')
            leading = size*1.35
            baseline = (y1+y2)/2 - (len(lines)-1)*leading/2 + (font.ascender+font.descender)*size/2
            for i, line in enumerate(lines):
                x = x1+5 if align == 'left' else (x1+x2-font.text_length(line,fontsize=size))/2
                page.insert_text((x,baseline+i*leading),line,fontname='medium',fontsize=size,color=color)

        number = str(data['group_no'])
        font = fonts['extra']
        size = 40
        page.insert_text((744*sx-font.text_length(number,fontsize=size)/2,214.5*sy+(font.ascender+font.descender)*size/2),number,fontname='extra',fontsize=size,color=color)
        place(data['team_name'],(168,458,366,510),12)
        place(data['members'],(490,458,1193,510),10.5,'left')
        roles = [('leader',(360,614,637,660)),('budget',(360,660,637,702)),('insight_1',(360,702,637,744)),('insight_2',(360,744,637,787)),('schedule',(916,614,1193,660)),('photo',(916,660,1193,702)),('report_1',(916,702,1193,744)),('report_2',(916,744,1193,787))]
        for name, box in roles:
            place(data.get(name,''),box)
        for value in data['concepts']:
            x = [176,406,636,865,1096][int(value)]
            page.draw_line(((x-9)*sx,1117*sy),(x*sx,1126*sy),color=color,width=1.8)
            page.draw_line((x*sx,1126*sy),((x+12)*sx,1108*sy),color=color,width=1.8)
        for i,(y1,y2) in enumerate([(1400,1479),(1479,1558),(1558,1638)]):
            place(data[f'place_{i}'],(223,y1,489,y2))
            place(data[f'activity_{i}'],(489,y1,1207,y2),10.5,'left')
        return doc.tobytes(garbage=4,deflate=True)
