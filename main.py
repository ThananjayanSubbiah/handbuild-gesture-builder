"""HandBuild: gesture-controlled 2D blocks with optional lightweight physics."""
import argparse
from dataclasses import dataclass
import cv2
import mediapipe as mp
import numpy as np

@dataclass
class Block:
    x:float;y:float;size:int=58;angle:float=0;vy:float=0;color:tuple=(80,200,255)

def draw_block(frame,b):
    s=b.size/2;corners=np.array([[-s,-s],[s,-s],[s,s],[-s,s]])
    t=np.deg2rad(b.angle);rot=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
    pts=np.int32(corners@rot.T+[b.x,b.y]);cv2.fillConvexPoly(frame,pts,b.color)
    cv2.polylines(frame,[pts],True,(245,245,245),2,cv2.LINE_AA)
    cv2.circle(frame,(int(b.x),int(b.y)),3,(15,25,40),-1)

def physics_step(blocks,width,height):
    # Simple axis-aligned vertical stack solver. Rotation is visual only.
    for b in sorted(blocks,key=lambda b:b.y,reverse=True):
        b.vy=min(b.vy+.7,13)
        bottom=height-34-b.size/2
        for other in blocks:
            if other is b:continue
            if abs(b.x-other.x)<(b.size+other.size)*.44 and b.y<other.y:
                bottom=min(bottom,other.y-(other.size+b.size)/2)
        if b.y+b.vy>=bottom: b.y=bottom;b.vy=0
        else:b.y+=b.vy
        b.x=max(b.size/2,min(width-b.size/2,b.x))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--camera',type=int,default=0);args=parser.parse_args()
    cap=cv2.VideoCapture(args.camera)
    if not cap.isOpened():raise SystemExit('Camera unavailable. Try --camera 1.')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280);cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    hands=mp.solutions.hands.Hands(max_num_hands=1,min_detection_confidence=.6,min_tracking_confidence=.55)
    blocks=[];selected=None;pinched_last=False;physics=False;kind=0
    palette=[(235,170,65),(110,220,135),(200,120,240)]
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            frame=cv2.flip(frame,1);h,w=frame.shape[:2]
            result=hands.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            pinched=False;point=None;open_hand=False
            if result.multi_hand_landmarks:
                lm=result.multi_hand_landmarks[0].landmark
                point=(int(lm[8].x*w),int(lm[8].y*h))
                thumb=(int(lm[4].x*w),int(lm[4].y*h))
                pinched=np.hypot(point[0]-thumb[0],point[1]-thumb[1])<min(w,h)*.05
                open_hand=sum(lm[t].y<lm[p].y for t,p in [(8,6),(12,10),(16,14),(20,18)])>=4
                cv2.circle(frame,point,10,(30,255,90) if pinched else (255,255,80),2)
                if pinched and not pinched_last and point[1]<h-70:
                    # Select topmost nearby block; otherwise spawn a new one.
                    selected=next((b for b in reversed(blocks) if np.hypot(b.x-point[0],b.y-point[1])<b.size*.75),None)
                    if selected is None:
                        selected=Block(float(point[0]),float(point[1]),color=palette[kind]);blocks.append(selected)
                if pinched and selected:
                    selected.x=float(point[0]);selected.y=float(point[1]);selected.vy=0
                if open_hand and selected and not pinched:
                    selected.angle=(selected.angle+2.5)%360
            if not pinched:selected=None
            pinched_last=pinched
            if physics:
                held=selected
                physics_step([b for b in blocks if b is not held],w,h)
            overlay=np.zeros_like(frame);overlay[:]=(20,25,36)
            frame=cv2.addWeighted(frame,.30,overlay,.70,0)
            cv2.line(frame,(0,h-34),(w,h-34),(100,180,240),2)
            for b in blocks:draw_block(frame,b)
            cv2.putText(frame,'H A N D B U I L D',(25,40),cv2.FONT_HERSHEY_SIMPLEX,.85,(250,230,140),2)
            cv2.putText(frame,f'Blocks: {len(blocks)}   Physics: {"ON" if physics else "OFF"}   Color: {kind+1}',(25,76),cv2.FONT_HERSHEY_SIMPLEX,.6,(245,245,245),2)
            cv2.putText(frame,'Pinch: spawn / drag | 1-3: color | E: rotate last | P: physics | R: reset | Q: quit',(15,h-12),cv2.FONT_HERSHEY_SIMPLEX,.53,(240,240,240),1)
            cv2.imshow('HandBuild Gesture Builder',frame)
            key=cv2.waitKey(1)&255
            if key in (ord('q'),27):break
            if key in (ord('1'),ord('2'),ord('3')):kind=key-ord('1')
            if key==ord('p'):physics=not physics
            if key==ord('e') and blocks:blocks[-1].angle=(blocks[-1].angle+15)%360
            if key==ord('r'):blocks.clear();selected=None
    finally:
        hands.close();cap.release();cv2.destroyAllWindows()
if __name__=='__main__':main()
