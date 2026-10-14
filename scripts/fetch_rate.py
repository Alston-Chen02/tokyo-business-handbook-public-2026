"""Fetch only BOT's official JPY spot selling quote; fail closed on challenge/invalid HTML."""
import json,re,sys
from datetime import datetime,timezone
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from pathlib import Path
SOURCE='https://rate.bot.com.tw/xrt?Lang=zh-TW'
class Table(HTMLParser):
 def __init__(self):
  super().__init__();self.rows=[];self.row=None;self.cell=None;self.text=[]
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.row=[]
  if tag=='td' and self.row is not None:self.cell=[]
 def handle_data(self,data):
  self.text.append(data)
  if self.cell is not None:self.cell.append(data)
 def handle_endtag(self,tag):
  if tag=='td' and self.cell is not None:self.row.append(' '.join(self.cell).strip());self.cell=None
  if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
def parse(html):
 p=Table();p.feed(html);text=' '.join(p.text)
 match=re.search(r'牌價最新掛牌時間[：:]?\s*(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2})',text)
 if not match:raise ValueError('Official quote timestamp missing; no data published')
 row=next((r for r in p.rows if r and '(JPY)' in r[0]),None)
 if not row or len(row)<6:raise ValueError('JPY row missing')
 rate=float(row[5])
 if not 0<rate<5:raise ValueError('Invalid spot sell rate')
 return {'currency':'JPY','kind':'spotSell','rate':rate,'quotedAt':datetime.strptime(match[1],'%Y/%m/%d %H:%M').isoformat()+'+08:00','fetchedAt':datetime.now(timezone.utc).isoformat(),'source':SOURCE}
if __name__=='__main__':
 with urlopen(Request(SOURCE,headers={'User-Agent':'TokyoHandbook/1.0 (public BOT quotation sync)'}),timeout=30) as response:html=response.read().decode('utf-8-sig')
 q=parse(html);Path(sys.argv[1] if len(sys.argv)>1 else 'jpy.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(q,ensure_ascii=False))
