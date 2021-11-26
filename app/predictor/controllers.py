from flask import Blueprint, render_template, request,redirect,flash
# from utils.utils import finalList, pvr
# from utils import finalList, pvr
# from minor.utils.utils import *
from utils.utils import finalList, pvr

predict = Blueprint("predictor", "__name__", url_prefix="/")

@predict.route("/test", methods=["GET"])
def render_form():
    return render_template("predictor/index.html")

@predict.route("/test", methods=["POST"])
def predict_output():
    req = request.form
    percentile = req["percentile"]
    rank = req["rank"]
    state = req["state"]
    pwd = req["pwd"]
    gender = req["gender"]
    category = req["category"]
    sortby = str(req["sortby"])

    if(percentile == "" and rank == ""):
        flash("Please enter either your Rank or your Percentile",'error')
        return redirect(request.url)

    if(rank == ""):
        ranks = pvr(float(percentile),pwd,category)
        ranks = int(ranks)

        if(ranks <= 0):
            ranks = 2
        result = finalList(ranks,float(percentile),category,state,gender,pwd,sortby)

    if(rank):
        result = finalList(int(rank),percentile,category,state,gender,pwd,sortby)
        ranks = rank
    return render_template("predictor/output.html",ranks=ranks,category=category,tables=[result.to_html(classes='data')], titles=result.columns.values)