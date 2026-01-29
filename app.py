from pytubefix import YouTube
import ffmpeg
import os
import re
import streamlit as st

# Simple video downloader using streamlit and pytubefix

# page configuration
st.set_page_config(page_title="Youtube 1080p Video Downloader", page_icon=":video_camera:")
st.title("Youtube High Quality Video Downloader")
st.markdown("This app allows you to download 1080p YouTube videos!")

# helper function to clean filenames
def clean_filename(title):
    #delete illegal characters from filename
    return re.sub(r'[\\/*?:"<>|]', "", title)

# input URL
url = st.text_input("Enter Youtube Video URL: ",  placeholder="https://www.youtube.com/watch?v=example")

if url:
    try:
        #load youtube
        yt = YouTube(url)


        # show video information
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(yt.thumbnail_url, use_container_width=True)
        with col2:
            st.subheader(yt.title)
            st.write(f"Views: {yt.views:,} views")
            st.write(f"Channel: {yt.author}")

        # Set download folder
        path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Download button
        if st.button("Download Video (1080p)"):
            with st.status("Processing...", expanded=True) as status:
                # Download video and audio separately
                st.write("Looking for best video & audio")
                video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                # temp file location
                video_temp = os.path.join(path, "temp_video.mp4")
                audio_temp = os.path.join(path, "temp_audio.mp4")

                # Download process
                st.write(f"Downloading video at quality: ({video_stream.resolution})")
                video_stream.download(output_path=path, filename="temp_video.mp4")
                st.write("Downloading audio...")
                audio_stream.download(output_path=path, filename="temp_audio.mp4")
                
                #merge with ffmpeg
                st.write("Merging audio and video...")
                cleaned_title = clean_filename(yt.title)
                output_file = os.path.join(path, f"{cleaned_title}.mp4")

                try:
                    v_input = ffmpeg.input(video_temp)
                    a_input = ffmpeg.input(audio_temp)
                    # Merge setting idk
                    ffmpeg.output(v_input, a_input, output_file, vcodec='copy', acodec='aac').run(overwrite_output=True, quiet=True)
                    
                    # Clear temp files
                    os.remove(video_temp)
                    os.remove(audio_temp)
                    
                    status.update(label="Selesai!", state="complete", expanded=False)
                    st.success(f"Berhasil! File disimpan di: {output_file}")
                    st.balloons() # Celebration effect lol
                
                except Exception as e:
                    st.error(f"Error during merging: {e}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.divider()
st.caption("Developed by sbsm")