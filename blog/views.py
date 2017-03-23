from flask import render_template
from flask import request, redirect, url_for

from . import app
from .database import session, Entry

    

@app.route("/")
# @app.route("/entries/<int:limit>")
@app.route("/page/<int:page>")
def entries(page=1):
   
    count = session.query(Entry).count()
    
    try:
        limit = int(request.args.get('limit'))
        
    except (ValueError, TypeError):
        limit = 10
        
    if limit:
        if limit > count:
            limit = 10 
        PAGINATE_BY= limit
    else:
        PAGINATE_BY= 10
    # import pdb; pdb.set_trace()
    
    page_index = page - 1

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    ) 
    
    
@app.route("/entry/add", methods=["GET"])    
def add_entry_get():
    return render_template("add_entry.html")
    
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<int:id>")
def entry_view(id):
    #return "reading entry %d" % id
    entry = session.query(Entry)
    entry = entry.filter(Entry.id==id)[0]
    return render_template("entry_view.html", entry=entry)

@app.route("/entry/<int:id>/edit", methods=["GET"])
def entry_edit_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id==id)[0]
    return render_template("entry_edit.html", entry=entry)

@app.route("/entry/<int:id>/edit", methods=["POST"])   
def entry_edit_post(id):
    
    entry = session.query(Entry)
    entry = entry.filter(Entry.id==id)[0]
    entry.title = request.form['title']
    entry.content = request.form['content']
    session.add(entry)
    session.commit()
    return render_template("entry_view.html", entry=entry)
    
@app.route("/entry/<int:id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry)
    entry = entry.filter(Entry.id==id)[0]
    return render_template("delete_entry.html", entry=entry)

 
@app.route("/entry/<int:id>/delete_action")
def delete_entry_post(id):

    entry = session.query(Entry)
    entry = entry.filter(Entry.id==id)[0]
    # entry = entry
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))
    
