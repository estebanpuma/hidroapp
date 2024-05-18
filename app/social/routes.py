from flask import render_template, redirect, url_for, request

from .models import Community
from . import social_bp


@social_bp.route("/")
def social():
    title = "Social"
    
    return render_template("social/index.html",
                           title = title)


@social_bp.route("/communities")
def communities():
    title = "Comunidades"
    communities = Community.query.all()
    return render_template("social/communities.html",
                           title=title,
                           communities = communities)
    

@social_bp.route("/add_community/<int:community_id>/", methods=["GET", "POST"])
@social_bp.route("/add_community", methods=["GET", "POST"])
def add_community(community_id=None):
    title = "Añadir comunidad"
    community = Community.get_by_id(community_id)
    name_error = None
    name_error_msg = None
    
    if request.method == "POST":
        print("reuqest")
        name = request.form["name"]
        description = request.form["description"]
        
        n_community = Community.query.filter_by(name=name).first()
        
        if n_community:
            name_error_msg = "Ya existe una comunidad registrada con este nombre"
            print(n_community)
        else:
            n_community = Community(name=name,
                                    description=description)
            print(n_community)
            n_community.save()

        return redirect(url_for('social.communities'))
    
    return render_template("social/add_community.html",
                           title=title,
                           community = community,
                           name_error = name_error,
                           name_error_msg = name_error_msg)
    

@social_bp.route("/delete_community/<int:community_id>/", methods=["GET", "POST"])
def delete_community(community_id):
    community = Community.get_by_id(community_id)
    if community:
        community.delete()
        return redirect(url_for('social.communities'))