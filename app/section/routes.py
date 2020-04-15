from flask import redirect, request, \
                  render_template, url_for, \
                  flash
from flask_login import current_user, login_required

from app import db, codemirror, config
from app.models import Section, Article, CaptchaStore
from app.section import section
from .forms import ArticlePostForm


@section.route('/<shortname>/')
def feed(shortname):
    page = request.args.get('page', 1, type=int)
    section = Section.query.filter_by(shortname=shortname).first_or_404()
    articles = section.articles.order_by(Article.timestamp.desc()).paginate(
        page, config['ARTICLES_PER_PAGE'], False)
    return render_template(
        'feed.html',
        title="/{}/".format(shortname),
        section=section,
        articles=articles.items,
        pagination=articles,
    )


@section.route('/<shortname>/<article_id>')
def article(shortname, article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        flash("Такая страница не найдена")
        return redirect(url_for('section', shortname=shortname))
    return render_template(
        'article.html',
        title=article.title,
        article=article,
    )


@section.route('/post', methods=['POST', 'GET'])
def post():
    form = ArticlePostForm()
    form.section.choices = [
        (s.id, s.longname) for s in Section.query.all()
    ]
    if form.validate_on_submit():
        captcha = CaptchaStore.query.filter_by(
            hash=form.hash.data).first()
        if captcha is None:
            flash(
                "Капча неверна. Пожалуйста, решите ее перед отправкой",
                'error'
            )
            return redirect(url_for('.post'))
        captcha.remove_picture()
        db.session.delete(captcha)
        db.session.commit()
        article = Article(
            markdown_body=form.data.data,
            title=form.title.data,
            section_id=form.section.data,
            poster_name=form.username.data,
            description=form.description.data,
        )
        article.create_tripcode(form.password.data)
        article.create_html()
        db.session.add(article)
        db.session.commit()
        return redirect(url_for(
            '.article',
            shortname=Section.query.get(article.section_id).shortname,
            article_id=article.id
        ))
    return render_template(
        'post.html',
        title="Запостить",
        form=form,
    )
