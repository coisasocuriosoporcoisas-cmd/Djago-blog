from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Comment, Post


class CommentTests(TestCase):
	def setUp(self):
		self.author = get_user_model().objects.create_user(
			username='author',
			password='test-password',
		)
		self.post = Post.objects.create(
			title='A published post',
			slug='published-post',
			author=self.author,
			body='Post body',
			status=Post.Status.PUBLISHED,
		)
		self.comment_url = reverse('blog:post_comment', args=[self.post.id])

	def test_site_root_redirects_to_blog_list(self):
		response = self.client.get('/')

		self.assertRedirects(response, reverse('blog:post_list'))

	def test_valid_comment_is_saved(self):
		response = self.client.post(
			self.comment_url,
			{'name': 'Reader', 'email': 'reader@example.com', 'body': 'Nice post.'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Comment.objects.count(), 1)
		self.assertEqual(Comment.objects.get().post, self.post)
		self.assertContains(response, 'Your comment has been added.')

	def test_invalid_comment_is_not_saved(self):
		response = self.client.post(
			self.comment_url,
			{'name': '', 'email': 'not-an-email', 'body': ''},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Comment.objects.count(), 0)
		self.assertTrue(response.context['form'].errors)

	def test_get_is_not_allowed(self):
		response = self.client.get(self.comment_url)

		self.assertEqual(response.status_code, 405)

	def test_inactive_comments_are_hidden_and_not_counted(self):
		Comment.objects.create(
			post=self.post,
			name='Hidden reader',
			email='hidden@example.com',
			body='Hidden comment.',
			active=False,
		)
		Comment.objects.create(
			post=self.post,
			name='Visible reader',
			email='visible@example.com',
			body='Visible comment.',
			active=True,
		)
		detail_url = reverse(
			'blog:post_detail',
			args=[
				self.post.publish.year,
				self.post.publish.month,
				self.post.publish.day,
				self.post.slug,
			],
		)

		response = self.client.get(detail_url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['total_comments'], 1)
		self.assertContains(response, 'Visible reader')
		self.assertNotContains(response, 'Hidden reader')

	def test_similar_posts_are_shown_without_comments(self):
		similar_post = Post.objects.create(
			title='A related post',
			slug='related-post',
			author=self.author,
			body='Related post body',
			status=Post.Status.PUBLISHED,
		)
		self.post.tags.add('django')
		similar_post.tags.add('django')
		detail_url = reverse(
			'blog:post_detail',
			args=[
				self.post.publish.year,
				self.post.publish.month,
				self.post.publish.day,
				self.post.slug,
			],
		)

		response = self.client.get(detail_url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['similar_posts']), [similar_post])
		self.assertContains(response, 'Similar posts')
		self.assertContains(response, 'A related post')

	def test_posts_link_to_their_detail_page(self):
		response = self.client.get(reverse('blog:post_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.post.get_absolute_url())

	def test_tag_page_filters_posts(self):
		self.post.tags.add('django')
		other_post = Post.objects.create(
			title='An unrelated post',
			slug='unrelated-post',
			author=self.author,
			body='Unrelated post body',
			status=Post.Status.PUBLISHED,
		)

		response = self.client.get(
			reverse('blog:post_list_by_tag', args=['django'])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			[post.pk for post in response.context['posts']],
			[self.post.pk],
		)
