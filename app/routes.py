from flask import render_template, flash, redirect, url_for, request

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Index Page")


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
        addon=links_on_addon
    )


@app.route('/yahenni')
def yahenni():
    return render_template("specialpersons/yahenni.html", title="Якхенни")


@app.route('/aboutme')
def aboutme():
    useragent = request.headers.get('User-Agent')
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return render_template(
        "aboutme.html",
        title="Большой брат",
        useragent=useragent,
        ip=ip
    )
