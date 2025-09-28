from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm, EmailPostForm, PostForm
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)


def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = "posts"
	ordering = ['-date_posted']
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = "user_posts"
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


# class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'

	def get_content(self, **kwargs):
		content = super().get_content(**kwargs)
		post = self.get_object()
		content['comments'] = post.comments.filter(active=True)
		content['form'] = CommentForm()
		return context

	def post(request, post_id):
		post = get_object_or_404(Post,
							id=post_id)
		form = CommentForm(request.POST)

		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.save()
		
		comments = post.comments.filter(active=True)
		return render(request, 'blog/include/comment_form.html',
							{'post': post,
							'form': form,
							'comment': comments})


def post_detail(request, id, post):
	post = get_object_or_404(Post, id=id, slug=post,)
							# status = Post.Status.PUBLISHED)
	comments = post.comments.filter(active=True)
	form = CommentForm()
	return render(request,
					'blog/post_detail.html',
					{"post":post,
					"comment":comments,
					"form":form})

@require_POST
def post_comment(request, post_id):
	post = get_object_or_404(Post, 
							id=post_id)
							# status = Post.Status.PUBLISHED,)
	comment = None
	form = CommentForm(request.POST)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.post = post
		comment.author = request.user
		comment = form.save()
	return render(request, 'blog/comment.html',
							{'post': post,
							'form': form,
							'comment': comment})

def post_share(request, id):
	post = get_object_or_404(Post, id=id)
								# status = Post.Status.PUBLISHED)

	sent=False
	if request.method == "POST":
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(
				post.get_absolute_url())
			subject = f"{cd['name']} recommends you read " \
				f"{post.title}"
			message = f"Read {post.title} at {post_url}\n\n" \
				f"{cd['name']}\'s comments: {cd['comment']}"
			send_mail(subject, message, cd['email'],
				[cd['to']])
			sent = True

	else:
		form = EmailPostForm()
	return render(request, "blog/post_share.html",
							{'post':post,
							'form': form,
							"sent": sent})


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'blog/about.html', {'title':'About'})