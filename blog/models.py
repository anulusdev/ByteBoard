from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class Post(models.Model):

	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'
	
	title = models.CharField(max_length=100)
	content = RichTextUploadingField()
	date_posted = models.DateTimeField(default=timezone.now)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	status = models.CharField(max_length=2,
							choices=Status.choices,
							default=Status.DRAFT)

	class Meta:
		ordering = ['-date_posted']
		indexes = [
			models.Index(fields=['-date_posted']),
		]
	
	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.title)
			slug = base_slug
			num = 1
			while Post.objects.filter(slug=slug).exists():
				slug = f"{base_slug}-{num}"
				num += 1
			self.slug = slug
			super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post_detail',
						args=[self.id,
							self.slug])

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post,
			on_delete=models.CASCADE, 
			related_name='comments')
	author = models.ForeignKey(User, 
				on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ["-created"]
		indexes = [
			models.Index(fields=['-created']),
		]

	def __str__(self):
		return f'commented by {self.author} on {self.post}'