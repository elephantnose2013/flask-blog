from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskwebapp import db
from flaskwebapp.models import Post
from flaskwebapp.post.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'post created!', 'success')
        # app.logger.info('passed')
        return redirect(url_for('main.home'))
    return render_template('create_and_update_post.html', title='New Post', form=form, legend='create post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('post updated', 'success')
        return redirect(url_for('posts.get_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_and_update_post.html', title='update post', form=form, legend='update post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('post deleted', 'success')
    return redirect(url_for('main.home'))
