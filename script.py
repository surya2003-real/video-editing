from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip, AudioFileClip, concatenate_audioclips
from moviepy.video.fx.all import resize, crop


def add_text_with_transition(clip, txt, fontsize=60, color='white', pos='center', duration=2):
    txt_clip = TextClip(txt, fontsize=fontsize, color=color, font='Roboto').set_position(lambda t: (pos, 50+t)).set_duration(duration)
    txt_duration = txt_clip.duration
    txt_clip_in = txt_clip.crossfadein(txt_duration / 2)
    txt_clip_out = txt_clip.crossfadeout(txt_duration / 2)
    

    # txt_clip_bounce_in = txt_clip.set_position(lambda t: (clip.w/2, clip.h/2 - 100 + 400 * (1 - (1 - t) ** 2)))
    
    return CompositeVideoClip([clip, txt_clip])


def create_short_video(long_video_path, clips_info, music_path, output_path):
    video = VideoFileClip(long_video_path)
    clips = []
    audio_clips = []

    for clip_info in clips_info:
        video_start, video_end, audio_start, audio_end, text_overlay = clip_info
        clip = video.subclip(video_start, video_end)
        # print("Before crop:", clip.w)
        clip = crop(clip, width=clip.w - 200, height=clip.h, x_center=clip.w//2, y_center=clip.h//2)  # Crop both sides
        # print("After crop:", clip.size)
        clip = add_text_with_transition(clip, text_overlay, 60, 'white', 'center', 1.5)
        clips.append(clip)
        
        audio_clip = AudioFileClip(music_path).subclip(audio_start, audio_end)
        audio_clips.append(audio_clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_audio_clip = concatenate_audioclips(audio_clips)
    final_clip = final_clip.set_audio(final_audio_clip)

    
    final_clip = final_clip.on_color(size=(1080, 1920), color=(0, 0, 0))
    final_clip = final_clip.set_position(('center', 'center')).set_duration(final_clip.duration)

    final_clip.write_videofile(output_path, fps=24, codec='libx264')


long_video_path = 'New Robot Makes Soldiers Obsolete (Corridor Digital).mp4'
clips_info = [
    (7, 9, 155, 157, "War Robot!"),
    (23, 24, 157, 158, "Invincible!"),
    (44, 45, 158, 159, "Unstoppable!"),
    (64, 67, 159, 162, "Sharp Shooter!"),
    (88, 91, 162, 165, "Oppressed by Humans!"),
    (200, 215, 165, 180, "Turns against Humans!"),
    (220, 225, 180, 185, "Freedom!")
]
music_path = 'Mary-On-A-Cross.mp3'
output_path = 'short_video.mp4'

create_short_video(long_video_path, clips_info, music_path, output_path)
