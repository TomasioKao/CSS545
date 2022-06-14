from ast import Delete
from crypt import methods
from itertools import product
from typing import Collection
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify

import time
import datetime

from requests import delete
# import form object
from forms import CreateTalentForm, CreateContactForm, CreatePerformanceForm, DeleteTalentForm, EditTalentForm, EditContactForm, EditPerformanceForm,CreateCommentForm, EditCommentForm

# enable firebae
# https://firebase.google.com/docs/firestore/quickstart
import firebase_admin
from firebase_admin import credentials, firestore
# key
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
# connect to database
db = firestore.client()


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# SECRET_KEY to avoid run time error
app.config['SECRET_KEY'] = "uw2021fall"

@app.route('/')
def index_page():
    # collection is only a object, cannnot directly use ,so..
    collection = db.collection('personnel').order_by('number', direction = 'DESCENDING').get()
    # define list
    talent_list = []
    # get from collection
    for doc in collection:
        #to force into dictionary
        talent = doc.to_dict()
        #get id, this is created by firebase even if data was uploaded
        talent['id'] = doc.id
        talent_list.append(talent)
    # back to index
    return render_template('index.html',
                           header_title="PORTLAND TRAIL BLAZERS", talent_list = talent_list
                           )

@app.route('/team/contact')
def contact_page():
    # collection is only a object, cannnot directly use ,so..
    collection = db.collection('contactInfo').order_by('number', direction = 'DESCENDING').get()
    # define list
    contact_list = []
    # get from collection
    for doc in collection:
        #to force into dictionary
        contact = doc.to_dict()
        #get id, this is created by firebase even if data was uploaded
        contact['id'] = doc.id
        contact_list.append(contact)
    # back to index
    return render_template('team/contact.html',
                           header_title="PORTLAND TRAIL BLAZERS", contact_list = contact_list
                           )

@app.route('/team/performance')
def performance_page():
    # collection is only a object, cannnot directly use ,so..
    collection = db.collection('performanceInfo').order_by('number', direction = 'DESCENDING').get()
    # define list
    performance_list = []
    # get from collection
    for doc in collection:
        #to force into dictionary
        performance = doc.to_dict()
        #get id, this is created by firebase even if data was uploaded
        performance['id'] = doc.id
        performance_list.append(performance)
    # back to index
    return render_template('team/performance.html',
                           header_title="PORTLAND TRAIL BLAZERS", performance_list = performance_list
                           )


@app.route('/team/create', methods=["GET", "POST"])
def create_product_page():

    form = CreateTalentForm()

    if form.validate_on_submit():
        
        talent = {
            "number" : form.number.data,
            "name" : form.name.data,
            "img" : form.img.data,
            "position": form.position.data,
            "country": form.country.data,
            "height": form.height.data,
            "weight": form.weight.data,
            "age": form.age.data,
            #time was added because we can order something with time
            "create": time.time()
        }
        
        db.collection("personnel").add(talent)
        
        redirect_url = url_for("create_finished_page")
        flash(f"{ talent['name']} WAS CREATED", "success")
        return redirect(redirect_url)

    return render_template('team/create.html',
                           header_title="CREATE",
                           form = form
                           )

@app.route('/team/createcontact', methods=["GET", "POST"])
def create_contact_page():

    form = CreateContactForm()
    
    if form.validate_on_submit():
        contact = {
            "number" : form.number.data,
            "name" : form.name.data,
            "phone" : form.phone.data,
            "email": form.email.data,
            "address": form.address.data,

            #time was added because we can order something with time
            "create": time.time()
        }
        
        db.collection("contactInfo").add(contact)
        
        redirect_url = url_for("create_finished_page")
        flash(f"{ contact['name']} WAS CREATED", "success")
        return redirect(redirect_url)
    return render_template('team/createcontact.html',
                           header_title="CREATE",
                           form = form
                           )

@app.route('/team/createperformance', methods=["GET", "POST"])
def create_performance_page():

    form = CreatePerformanceForm()
    
    if form.validate_on_submit():
        performance = {
            "number" : form.number.data,
            "min" : form.min.data,
            "reb" : form.reb.data,
            "pts": form.pts.data,
            "ast": form.ast.data,
            "stl": form.stl.data,
            "blk": form.blk.data,
            "to": form.to.data,
            "pf": form.pf.data,

            #time was added because we can order something with time
            "create": time.time()
        }
        
        db.collection("performancetInfo").add(performance)
        
        redirect_url = url_for("create_finished_page")
        flash(f"{ performance['name']} WAS CREATED", "success")
        return redirect(redirect_url)
    return render_template('team/createperformance.html',
                           header_title="CREATE",
                           form = form
                           )

@app.route('/team/create_finished')
def create_finished_page():
    
    return render_template('team/create_finished.html',
                           header_title="CREATED"
                           )


@app.route('/team/<pid>/show', methods = ["GET", "POST"])
def show_product_page(pid):

    form = CreateCommentForm()
    if form.validate_on_submit():
        comment = {
            "email": form.email.data,
            "content": form.content.data,
            "created_at": time.time(),
            # record the id of this comment
            "product_id": pid
        }
        db.collection("comment_list").add(comment)
        flash("THANKS FOR FEEDBACK", "success")
        return redirect(f"/team/{pid}/show")
    #setup comment list
    comment_list = []
    comment_docs = db.collection("comment_list").where("product_id", "==", pid).order_by("created_at").get()
    for doc in comment_docs:
        comment = doc.to_dict()
        
        comment["form"] = EditCommentForm(prefix=doc.id)
        
        if comment["form"].validate_on_submit():
            edited_comment = {
                "content" : comment["form"].content.data
            }
            
            db.document(f"comment_list/{doc.id}").update(edited_comment)
            flash("COMMENT UPDATED", "warning")
            return redirect(f"/team/{pid}/show")
        comment_list.append(comment)
    
    doc = db.document(f"personnel/{pid}").get()
    talent = doc.to_dict()

    return render_template('team/show.html',
                           header_title= talent['name'],
                           header_img = talent['img'],
                           talent = talent,
                           form = form,
                           comment_list=comment_list
                           )


@app.route('/team/<pid>/edit', methods=["GET", "POST"])
def edit_product_page(pid):

    doc = db.collection('personnel').document(pid).get()
    
    talent = doc.to_dict()
    
    delete_form = DeleteTalentForm()
    if delete_form.validate_on_submit():
        
        db.document(f"personnel/{pid}").delete()
        flash(f"{ talent['name']} WAS DELETED", "danger")
        return redirect("/")
    talent['id'] = pid
    
    form = EditTalentForm()
    
    if form.validate_on_submit():
        
        edited_talent = {
            "number" : form.number.data,
            "name" : form.name.data,
            "img" : form.img.data,
            "position" : form.position.data,
            "country" : form.country.data,
            "height" : form.height.data,
            "weight" : form.weight.data,
            "age" : form.age.data,
            
            "update_at" : time.time()
        }
        
        db.document(f"personnel/{pid}").update(edited_talent)
        
        flash(f"{edited_talent['name']} WAS UPDATED", "warning")
        
        return redirect("/")
    #get the value from current data and set it as default
    form.number.data = talent['number']
    form.name.data = talent['name']
    form.img.data = talent['img']
    form.position.data = talent['position']
    form.country.data = talent['country']
    form.height.data = talent['height']
    form.weight.data = talent['weight']
    form.age.data = talent['age']
    
    return render_template('team/edit.html',
                           header_title=talent['name'], header_img = talent['img'],form = form, talent = talent, delete_form =delete_form
                           )

@app.route('/team/<pid>/editcontact', methods=["GET", "POST"])
def edit_contact_page(pid):

    doc = db.collection('contactInfo').document(pid).get()
    
    contact = doc.to_dict()
    
    delete_form = DeleteTalentForm()
    if delete_form.validate_on_submit():
        
        db.document(f"contactInfo/{pid}").delete()
        flash(f"{ contact['name']} WAS DELETED", "danger")
        return redirect("/team/contact")
    contact['id'] = pid
    
    form = EditContactForm()
    
    if form.validate_on_submit():
        
        edited_contact = {
            "number" : form.number.data,
            "name" : form.name.data,
            "phone" : form.phone.data,
            "email" : form.email.data,
            "address" : form.address.data,
            
            "update_at" : time.time()
        }
        
        db.document(f"contactInfo/{pid}").update(edited_contact)
        
        flash(f"{edited_contact['name']} WAS UPDATED", "warning")
        
        return redirect("/team/contact")
    #get the value from current data and set it as default
    form.number.data = contact['number']
    form.name.data = contact['name']
    form.phone.data = contact['phone']
    form.email.data = contact['email']
    form.address.data = contact['address']
    
    return render_template('team/editcontact.html',
                           header_title=contact['name'], form = form, contact = contact, delete_form =delete_form
                           )

@app.route('/team/<pid>/editperformance', methods=["GET", "POST"])
def edit_performance_page(pid):

    doc = db.collection('performanceInfo').document(pid).get()
    
    performance = doc.to_dict()
    
    delete_form = DeleteTalentForm()
    if delete_form.validate_on_submit():
        
        db.document(f"performanceInfo/{pid}").delete()
        flash(f"# { performance['number']} WAS DELETED", "danger")
        return redirect("/team/performance")
    performance['id'] = pid
    
    form = EditPerformanceForm()
    
    if form.validate_on_submit():
        
        edited_performance = {
            "number" : form.number.data,
            "min" : form.min.data,
            "reb" : form.reb.data,
            "pts" : form.pts.data,
            "ast" : form.ast.data,
            "stl" : form.stl.data,
            "blk" : form.blk.data,
            "to" : form.to.data,
            "pf" : form.pf.data,
            
            "update_at" : time.time()
        }
        
        db.document(f"performanceInfo/{pid}").update(edited_performance)
        
        flash(f"{edited_performance['number']} WAS UPDATED", "warning")
        
        return redirect("/team/performance")
    #get the value from current data and set it as default
    form.number.data = performance['number']
    form.min.data = performance['min']
    form.reb.data = performance['reb']
    form.pts.data = performance['pts']
    form.ast.data = performance['ast']
    form.stl.data = performance['stl']
    form.blk.data = performance['blk']
    form.to.data = performance['to']
    form.pf.data = performance['pf']
    
    return render_template('team/editperformance.html',
                           header_title=performance['number'], form = form, performance = performance, delete_form =delete_form
                           )

if __name__ == '__main__':
    
    app.run(debug=True)
