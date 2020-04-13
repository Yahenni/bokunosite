from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import Section, Article, CaptchaStore, User
from app.forms import ArticlePostForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        "index.html",
        title="Index Page",
        sections=Section.query.all(),
    )


@app.route('/kirill')
def kirill():
    if "Firefox" not in request.headers.get('User-Agent'):
        browser = "chrome"
    else:
        browser = "firefox"
    links_on_addon = {
        "firefox": "https://addons.mozilla.org/en-US/firefox/"
                   "addon/live-editor-for-css-less-sass/?src=search",
        "chrome": "https://chrome.google.com/webstore/detail/lil"
                  "ve-editor-for-css-less/ifhikkcafabcgolfjegfcgloomalapol"
    }
    return render_template(
        "specialpersons/kirill.html",
        title="Главный пидорас",
        browser=browser,
        addon=links_on_addon,
        favicon='specialpersons/kirill/favicon'
    )


@app.route('/yahenni')
def yahenni():
    return render_template(
        "specialpersons/yahenni.html",
        title="Якхенни",
    )


@app.route('/aboutme')
def aboutme():
    useragent = request.headers.get('User-Agent')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return render_template(
        "aboutme.html",
        title="Большой брат",
        useragent=useragent,
        ip=ip,
    )


@app.route('/trash')
def trash():
    return redirect("https://2ch.hk/ga/")


@app.route('/section/<shortname>/')
def section(shortname):
    page = request.args.get('page', 1, type=int)
    section = Section.query.filter_by(shortname=shortname).first_or_404()
    articles = section.articles.order_by(Article.timestamp.desc()).paginate(
        page, app.config['ARTICLES_PER_PAGE'], False)
    return render_template(
        'section.html',
        title="/{}/".format(shortname),
        section=section,
        articles=articles.items,
        pagination=articles,
    )


@app.route('/section/<shortname>/<article_id>')
def article(shortname, article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        flash("Такая страница не найдена")
        return redirect(url_for('section', shortname=shortname))
    return render_template(
        'article.html',
        article=article,
    )


@app.route('/section/post', methods=['POST', 'GET'])
def article_post():
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
            return redirect(url_for('article_post'))
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
        article.format_timestamp()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template(
        'article_post.html',
        form=form,
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль или имя пользователя', "error")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Успешно вошли')
        return redirect(url_for('index'))
    return render_template(
        "login.html",
        title="Login",
        navbar_off=True,
        message_off=True,
        form=form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
