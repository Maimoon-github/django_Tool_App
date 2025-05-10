from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os

@csrf_exempt
def fetch_transcript(request):
    result = ""
    if request.method == "POST":
        url = request.POST.get("url", "")
        filename = request.POST.get("filename", "output.txt")
        dest_folder = request.POST.get("dest_folder", "")
        if not filename.endswith(".txt"):
            filename += ".txt"
        # If user provided a destination folder, join it with the filename
        if dest_folder:
            output_file = os.path.join(dest_folder, filename)
        else:
            # Use the user's home directory as the default destination folder
            home_dir = os.path.expanduser('~')
            output_file = os.path.join(home_dir, filename)

        def get_transcript_with_translation(video_id):
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except:
                    for transcript_item in transcript_list:
                        if transcript_item.is_generated:
                            transcript = transcript_item.translate('en')
                            break
                    else:
                        raise ValueError("No suitable transcript found")
                formatter = TextFormatter()
                return formatter.format_transcript(transcript.fetch())
            except Exception as e:
                return f"Error fetching transcript for video ID {video_id}: {e}"

        try:
            title = "User Provided URL"
            video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
            transcript = get_transcript_with_translation(video_id)
            # Ensure the output directory exists
            folder_to_create = os.path.dirname(output_file)
            if folder_to_create and not os.path.exists(folder_to_create):
                os.makedirs(folder_to_create)
            with open(output_file, "w", encoding="utf-8") as f_out:
                if transcript:
                    f_out.write(f"Title: {title}\n")
                    f_out.write(f"URL: {url}\n")
                    f_out.write("Transcript:\n")
                    f_out.write(transcript)
                    f_out.write("\n" + "="*80 + "\n\n")
                    result += f"Transcript for '{title}' saved.\n"
                else:
                    result += f"No transcript available for: {title}\n"
            result += f"Transcripts saved in {output_file}"
        except Exception as e:
            result += f"Error processing {url}: {e}\n"
    return render(request, "transcripts/fetch_transcript.html", {"result": result})
