#!/usr/bin/env python3
"""Regenerate the downloadable CV and social image. Requires reportlab and Pillow."""
import html
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import DATA, PROJECTS, EXPERIENCE, EARLIER
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'src/static';TARGET.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('CVSans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('CVSansBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('CVSans',normal='CVSans',bold='CVSansBold',italic='CVSans',boldItalic='CVSansBold')
INK=colors.HexColor('#142b38');TEAL=colors.HexColor('#147968');MUTED=colors.HexColor('#526773')
styles={
 'name':ParagraphStyle('name',fontName='CVSansBold',fontSize=27,leading=34,textColor=INK,spaceAfter=6),
 'tag':ParagraphStyle('tag',fontName='CVSans',fontSize=10.3,leading=16,textColor=TEAL,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='CVSans',fontSize=9.2,leading=14,textColor=MUTED,spaceAfter=8),
 'section':ParagraphStyle('section',fontName='CVSansBold',fontSize=12,leading=17,textColor=INK,spaceBefore=16,spaceAfter=9,keepWithNext=True),
 'sub':ParagraphStyle('sub',fontName='CVSansBold',fontSize=10,leading=15,textColor=INK,spaceBefore=8,spaceAfter=4,keepWithNext=True),
 'meta':ParagraphStyle('meta',fontName='CVSans',fontSize=8.4,leading=13,textColor=TEAL,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='CVSans',fontSize=8.2,leading=12,textColor=MUTED,spaceAfter=8),
}
def clean(text):return str(text).replace('–','-').replace('—','-').replace('‑','-').replace('’',"'")
def p(text,style='body'):return Paragraph(clean(text),styles[style])
def esc(text):return html.escape(clean(text))
def link(url,label):return f'<link href="{html.escape(url,quote=True)}" color="#147968">{esc(label)}</link>'
class NumberedCanvas(canvas.Canvas):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.states=[]
 def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
 def save(self):
  count=len(self.states)
  for state in self.states:
   self.__dict__.update(state);self.setStrokeColor(colors.HexColor('#dce5e9'));self.line(46,40,A4[0]-46,40);self.setFont('CVSans',7.3);self.setFillColor(MUTED);self.drawString(46,26,'Ming Chen | Selected academic CV | November 2026');self.drawRightString(A4[0]-46,26,f'{self._pageNumber} / {count}');super().showPage()
  super().save()

story=[]
story += [p('Ming Chen','name'),p('Researcher &amp; engineer in cloud and AI systems','tag'),p('Melbourne, Australia | '+link('mailto:'+DATA['email'],DATA['email'])+'<br/>'+link(DATA['github'],'GitHub')+' | '+link(DATA['linkedin'],'LinkedIn')+' | '+link(DATA['scholar'],'Google Scholar')+' | '+link(DATA['orcid'],'ORCID'),'small')]
story += [p('Research profile','section'),p(esc(DATA['research_profile']))]
story += [p('Education','section'),p('PhD, Engineering and IT (Computer Science) | University of Melbourne','sub'),p('March 2022-April 2026. School of Computing and Information Systems. Thesis: <i>Demand Prediction and Service Scaling Methods for Microservices in Dynamic Computing Environments.</i><br/>Supervisor: Rajkumar Buyya. Co-supervisors: Maria Rodriguez Read and Muhammed Tawfiqul Islam.'),p('BEng (Hons), Intelligence Science and Technology | Hunan University','sub'),p('September 2012-June 2016. Outstanding Undergraduate Thesis.')]
story += [p('Research &amp; professional experience','section')]
short={
 'wearables':'Part-time. Develop reproducible Python analysis and verification tools for wearable sensor algorithms, including numerical checks, data-quality audits, capture-timing analysis, and evaluation design.',
 'supervision':'Supervised 10 industry-partner projects involving approximately 50 postgraduate students. Guided scope, method selection, implementation review, evaluation, partner demonstrations, and handover.',
 'phd':'Designed and implemented resource-forecasting, scheduling, and emulation methods for dynamic microservices, with Kubernetes experiments and first-author IEEE research outputs.',
 'telecom':'Led telecommunications and smart-finance R&D teams. Coordinated partner requirements, milestones, and reporting; contributed predictive models and co-authored operational-analytics research.',
 'robotics':'Built Linux/Docker/ROS robot-server infrastructure and real-time multi-robot map fusion. Integrated sensor streams and diagnosed networking and runtime-integration problems.'
}
for item in DATA['experience']:
 story += [p(esc(item['role']),'sub'),p(esc(item['organization'])+' | '+esc(item['date']),'meta'),p(esc(short[item['id']]))]
story.append(PageBreak())
story += [p('Selected publications &amp; preprints','section')]
for item in PROJECTS+DATA['additional_preprints']:
 venue={'idynamics':'IEEE Transactions on Services Computing, Early Access, 2026.','trade':'IEEE Transactions on Parallel and Distributed Systems, 37(1), 76-89, 2026.','agentfair':'Preprint, arXiv:2607.15781, 2026. Ming Chen: co-first and corresponding author.','enbeats':'IEEE International Conference on Cloud Computing (CLOUD), 144-154, 2023.'}.get(item['id'],'Preprint, arXiv:'+item.get('arxiv','')+', 2026.')
 authors=esc(item['authors']).replace('Ming Chen','<b>Ming Chen</b>')
 resources=link(item['paper'],'Paper / preprint')+(' | '+link(item['code'],'Public code') if item.get('code') else '')
 story.append(KeepTogether([p(esc(item['paper_title']),'sub'),p(authors+'<br/>'+esc(venue)),p(resources,'small')]))
story += [p('Earlier research','section'),p('Additional peer-reviewed work covers telecommunications alarm prediction (DCSA, ICPADS 2019), network-state prediction (LBNN, ICPADS 2020), financial-behavior modeling (AIMS 2019), anti-fraud methods (ICPS 2019), and NAO robot speech interaction (ICAR 2017). Full entries are available on the website Publications page and Google Scholar.')]
story.append(PageBreak())
story += [p('Industry collaboration &amp; supervision','section'),p('University of Melbourne Master of Data Science | 2023-present. Guided student teams through partner requirements, methods, implementation reviews, evaluation, demonstrations, and handover. Selected supervised projects:')]
for item in DATA['collaborations']:
 story.append(p('<b>'+esc(item['partner'])+':</b> '+esc(item['summary'])))
story += [p('Teaching','section')]
for item in DATA['teaching']:
 story.append(p('<b>'+esc(item['role'])+' | '+esc(item['institution'])+'</b><br/>'+esc(item['date'])+' | '+esc(item['course'])+'. '+esc(item['summary'])))
story += [p('Technical skills','section'),p('<b>Programming:</b> Python, Java, C/C++, MATLAB.<br/><b>Systems:</b> Kubernetes, Docker, Linux, Istio, Prometheus, Grafana, microservices, networking, ROS.<br/><b>AI &amp; data:</b> PyTorch, time-series forecasting, ensemble learning, anomaly prediction, RAG, LangGraph, FastAPI, SQLite, and LLM agents.<br/><b>Research practice:</b> experimental design, reproducible benchmarking, numerical verification, technical writing, teaching, mentoring, and stakeholder communication.')]
story += [p('Selected recognition','section')]
for item in DATA['recognition']:
 story.append(p('- '+esc(item['title'])+' | '+esc(item['context'])+' | '+item['year'], 'small'))
path=TARGET/'ming-chen-cv.pdf'
SimpleDocTemplate(str(path),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=40,bottomMargin=54,title='Ming Chen - Selected Academic CV',author='Ming Chen').build(story,canvasmaker=NumberedCanvas)

image=Image.new('RGB',(1200,630),'#142b38');draw=ImageDraw.Draw(image)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'
draw.text((85,90),'MING CHEN  /  CLOUD & AI SYSTEMS',font=ImageFont.truetype(bold,23),fill='#bdd9ce')
draw.text((80,205),'Research ideas.',font=ImageFont.truetype(bold,77),fill='#ffffff')
draw.text((80,315),'Working systems.',font=ImageFont.truetype(serif,80),fill='#a5d7c2')
draw.line((85,480,1115,480),fill='#49626d',width=1)
draw.text((85,520),'PhD, University of Melbourne  |  Researcher & Engineer',font=ImageFont.truetype(font_path,24),fill='#c4d5dc')
image.save(TARGET/'social-preview.png',optimize=True)
print(json.dumps({'cv':str(path),'social_image':str(TARGET/'social-preview.png')}))
