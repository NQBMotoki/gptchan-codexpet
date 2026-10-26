"""Render motion proof from an encoded atlas; does not modify sprite artwork."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

SPECS = [('idle',6),('running-right',8),('running-left',8),('waving',4),('jumping',5),('failed',8),('waiting',6),('running',6),('review',6)]

def frame(atlas, row, col, caption=''):
    sprite = atlas.crop((192*col,208*row,192*(col+1),208*(row+1)))
    board = Image.new('RGBA',(256,256),'#eeeaf2')
    board.alpha_composite(sprite,(32,30))
    ImageDraw.Draw(board).text((8,8),caption,fill='#241e30')
    return board.convert('RGB')

def gif(images,path,durations):
    images[0].save(path,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('atlas',type=Path)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--ffmpeg',type=Path)
    ap.add_argument('--video-codec',default='libx264',help='Use h264_mf for Windows FFmpeg builds without libx264')
    a=ap.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=True)
    atlas=Image.open(a.atlas).convert('RGBA')
    all_frames=[]
    records=[]
    for row,(name,count) in enumerate(SPECS):
        frames=[frame(atlas,row,c,f'{name} {c+1}/{count}') for c in range(count)]
        gif(frames,a.output_dir/f'{name}.gif',[140]*(count-1)+[280])
        all_frames.extend(frames)
        records.append({'state':name,'row':row,'frames':count})
    gif(all_frames,a.output_dir/'all-states.gif',[180]*len(all_frames))
    jump=[frame(atlas,0,0,'idle before jump')]*3+[frame(atlas,4,c,f'jump {c+1}/5') for c in range(5)]+[frame(atlas,0,0,'idle after landing')]*3
    gif(jump,a.output_dir/'idle-jump-idle.gif',[180]*len(jump))
    stills=Image.new('RGB',(256*4,256),'#eeeaf2')
    for i,k in enumerate([2,4,5,8]):
        stills.paste(jump[k],(256*i,0))
    stills.save(a.output_dir/'jump-transition-stills.png')
    if atlas.height==2288:
        labels=['000','022.5','045','067.5','090','112.5','135','157.5','180','202.5','225','247.5','270','292.5','315','337.5']
        looks=[frame(atlas,9+i//8,i%8,f'look {label} deg') for i,label in enumerate(labels)]
        gif(looks,a.output_dir/'look-loop.gif',[200]*16)
    video_frames=a.output_dir/'video-frames'
    video_frames.mkdir(exist_ok=True)
    for i,im in enumerate(all_frames):
        im.save(video_frames/f'{i:03}.png')
    if a.ffmpeg:
        pixel_format = 'nv12' if a.video_codec == 'h264_mf' else 'yuv420p'
        result = subprocess.run([str(a.ffmpeg),'-y','-framerate','6','-i',str(video_frames/'%03d.png'),'-c:v',a.video_codec,'-pix_fmt',pixel_format,'-movflags','+faststart',str(a.output_dir/'all-states.mp4')],capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr.decode('utf-8',errors='replace'))
    (a.output_dir/'preview-manifest.json').write_text(json.dumps({'atlas':str(a.atlas.resolve()),'sha256':hashlib.sha256(a.atlas.read_bytes()).hexdigest(),'rows':records,'mp4':bool(a.ffmpeg),'video_codec':a.video_codec if a.ffmpeg else None},indent=2),encoding='utf-8')
    print(json.dumps({'ok':True,'output_dir':str(a.output_dir),'mp4':bool(a.ffmpeg)}))

if __name__=='__main__':
    main()
