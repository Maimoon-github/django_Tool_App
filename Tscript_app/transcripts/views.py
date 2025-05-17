from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from .models import Category, Post
from .forms import AgeCalculatorForm
import os
from datetime import date

def home(request):
    latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    context = {
        'latest_posts': latest_posts,
        **sidebar_context()
    }
    return render(request, 'transcripts/home.html', context)

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

def calculate_age_view(request):
    age_result = None
    if request.method == 'POST':
        form = AgeCalculatorForm(request.POST)
        if form.is_valid():
            birth_date = form.cleaned_data['birth_date']
            today = date.today()
            # Calculate years
            years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            # Calculate months
            months = today.month - birth_date.month
            if today.day < birth_date.day:
                months -= 1
            if months < 0:
                months += 12
            # Calculate days
            if today.day >= birth_date.day:
                days = today.day - birth_date.day
            else:
                prev_month = today.month - 1 or 12
                prev_year = today.year if today.month != 1 else today.year - 1
                from calendar import monthrange
                days_in_prev_month = monthrange(prev_year, prev_month)[1]
                days = today.day + days_in_prev_month - birth_date.day
            # Total months and days
            total_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
            if today.day < birth_date.day:
                total_months -= 1
            total_days = (today - birth_date).days
            age_result = {
                'years': years,
                'months': months,
                'days': days,
                'totalMonths': total_months,
                'totalDays': total_days,
            }
    else:
        form = AgeCalculatorForm()
    return render(request, 'transcripts/age_calculator.html', {'form': form, 'age_result': age_result})

def sidebar_context():
    return {
        'recent_posts': Post.objects.filter(status='published').order_by('-published_at')[:5],
        'categories': Category.objects.all()
    }

def blog_home(request):
    category = request.GET.get('category')
    if category:
        post_list = Post.objects.filter(
            status='published',
            category__slug=category
        ).order_by('-published_at')
    else:
        post_list = Post.objects.filter(status='published').order_by('-published_at')
    
    paginator = Paginator(post_list, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'current_category': category,
        **sidebar_context()
    }
    return render(request, 'transcripts/blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    context = {
        'post': post,
        'related_posts': post.related_posts,
        **sidebar_context()
    }
    return render(request, 'transcripts/blog/post_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'posts': posts,
        **sidebar_context()
    }
    return render(request, 'transcripts/blog/category_detail.html', context)
