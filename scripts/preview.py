"""Generate a local-file-friendly preview without network requests or fetch()."""
import json
from pathlib import Path

def html(catalog):
    data = json.dumps(catalog, ensure_ascii=False).replace('<', '\\u003c')
    return TEMPLATE.replace('__CATALOG__', data)

TEMPLATE = '''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GPT酱 · 动作与换装预览</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f4f1f8;color:#302b3e;font:16px/1.6 system-ui,sans-serif}
main{max-width:940px;margin:40px auto;padding:24px}h1{font-size:28px;margin-bottom:4px}p{color:#635c73}
.controls{display:flex;gap:14px;flex-wrap:wrap;margin:24px 0}label{display:grid;gap:4px;font-size:14px}
select,button{font:inherit;border:1px solid #c7bed6;border-radius:8px;padding:8px;background:white;color:#302b3e}
button{align-self:end;cursor:pointer}.stage{height:390px;display:grid;place-items:center;border:1px solid #cec5dc;border-radius:18px;background:#fff}
#pet{width:192px;height:208px;background-repeat:no-repeat;transform-origin:center;image-rendering:auto}
.note{font-size:14px}output{font-variant-numeric:tabular-nums}a{color:#684e9c}
</style><main><h1>GPT酱 · 动作与换装预览</h1>
<p>逐帧检查、深浅背景与缩放。这里的播放速度用于素材检查，实际触发与速度由宿主决定。</p>
<div class="controls">
<label>服装<select id="outfit"></select></label><label>动作<select id="state"></select></label>
<label>背景<select id="background"><option value="#fff">浅色</option><option value="#252232">深色</option></select></label>
<label>尺寸<select id="scale"><option value="1">100%</option><option value="0.5">50%</option><option value="1.5">150%</option></select></label>
<button id="play" type="button">暂停</button><button id="step" type="button">下一帧</button></div>
<div class="stage" id="stage"><div id="pet" role="img" aria-label="GPT酱当前动作"></div></div>
<p><output id="counter" aria-live="off"></output></p>
<p class="note">16 个视线格按图集编号展示，方向顺序仍需实机验收。当前只有完成的服装会列出；高分辨率形象样稿不属于可安装服装。</p>
<p><a href="docs/OUTFITS.md">换装说明</a> · <a href="docs/ART-DIRECTION.md">形象与动作规范</a></p></main>
<script>
const catalog=__CATALOG__;
const states=[['待机',0,6],['向右移动',1,8],['向左移动',2,8],['挥手',3,4],['跳跃',4,5],['失败',5,8],['等待',6,6],['工作',7,6],['检查',8,6],['视线格 0–7',9,8],['视线格 8–15',10,8]];
const byId=id=>document.getElementById(id);let frame=0,playing=true;
for(const [id,value] of Object.entries(catalog.outfits)){const option=document.createElement('option');option.value=id;option.textContent=value.name;byId('outfit').append(option)}
states.forEach((s,i)=>{const option=document.createElement('option');option.value=i;option.textContent=s[0];byId('state').append(option)});
byId('outfit').value=catalog.defaultOutfit;
function draw(){const s=states[Number(byId('state').value)];frame%=s[2];byId('pet').style.backgroundPosition=(-192*frame)+'px '+(-208*s[1])+'px';byId('counter').textContent=s[0]+' · 帧 '+(frame+1)+' / '+s[2]}
function outfit(){const path=catalog.outfits[byId('outfit').value].path;byId('pet').style.backgroundImage='url('+JSON.stringify(path+'/spritesheet.webp')+')';frame=0;draw()}
byId('outfit').onchange=outfit;byId('state').onchange=()=>{frame=0;draw()};
byId('background').onchange=()=>byId('stage').style.background=byId('background').value;
byId('scale').onchange=()=>byId('pet').style.transform='scale('+byId('scale').value+')';
function pause(){playing=false;byId('play').textContent='播放'}
byId('play').onclick=()=>{playing=!playing;byId('play').textContent=playing?'暂停':'播放'};
byId('step').onclick=()=>{pause();frame++;draw()};
if(matchMedia('(prefers-reduced-motion: reduce)').matches)pause();
setInterval(()=>{if(playing){frame++;draw()}},150);outfit();
</script></html>'''

if __name__ == '__main__':
    from petctl import ROOT, catalog
    (ROOT / 'preview.html').write_text(html(catalog()), encoding='utf-8')
