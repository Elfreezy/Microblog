from app.main import bp
from app import db
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from flask import g, current_app

from datetime import datetime


@bp.before_request
def before_request():
    g.locale = str(get_locale())
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config.get('POST_PER_PAGE'), False)
    next_url = None
    if posts.has_next:
        next_url = url_for('main.explore', page=posts.next_num)
    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.explore', page=posts.prev_num)

    return render_template('index.html', posts=posts.items, prev_url=prev_url, next_url=next_url)


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))

    posts = current_user.followed_posts().paginate(page, current_app.config.get('POST_PER_PAGE'), False)
    next_url = None
    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    return render_template('index.html', form=form, posts=posts.items, prev_url=prev_url, next_url=next_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config.get('POST_PER_PAGE'), False)
    next_url = None
    if posts.has_next:
        next_url = url_for('main.user', username=user.username, page=posts.next_num)
    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.user', username=user.username, page=posts.prev_num)
    return render_template('user.html', user=user, posts=posts.items, prev_url=prev_url, next_url=next_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are unfollowing %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)
