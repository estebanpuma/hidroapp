from flask import render_template, redirect, url_for, request

from . import common_bp
from .models import Activity

@common_bp.route("/<module>/activity/<int:activity_id>")
def activity(module, activity_id):
    title = "Actividad"
    module = module
    activity = Activity.query.get(activity_id)
    previous_url = request.referrer
    if previous_url is None:
        previous_url = url_for("public.index")
        
    print(f"This is the pppp {previous_url}")
    return render_template("common/activity.html", 
                           title = title,
                           activity = activity,
                           module = module,
                           previous_url = previous_url)