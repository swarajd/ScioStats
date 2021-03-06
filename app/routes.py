from flask import render_template, request, redirect, url_for, flash
from app import app, limiter
from werkzeug.utils import secure_filename
from app import stats

ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

# this function checks if the files are excel files
def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# this template is to shorten the decimals
@app.template_filter("roundNum")
def roundNum(n):
    return format(n, ".2f")

@app.route('/', methods=["GET", "POST"])
@limiter.limit("10/minute")
def index():
    if (request.method == "POST"):
        # we'll be processing the ranks and potentially the roster
        rankFile = None
        rosterFile = None

        uploadedFiles = request.files.keys()

        # 'validate' both files
        if 'schoolRanks' in uploadedFiles:
            rankFile = request.files['schoolRanks']
            if not allowedFile(rankFile.filename):
                flash("the rank file must be an excel file")
                return redirect(request.url)
            rankFile.stream.seek(0)
        
        if 'schoolRoster' in uploadedFiles:
            rosterFile = request.files['schoolRoster']
            if not allowedFile(rosterFile.filename):
                flash("the roster file must be an excel file")
                return redirect(request.url)
            rosterFile.stream.seek(0)


        # go ahead and run the statistics
        if (rankFile is None):
            flash("you need a rank file!")
            return redirect(request.url)
        else:
            dataMap = {}
            stats.getStats(rankFile, rosterFile, dataMap)
        
        return render_template('results.html', title="ScioStats", dataMap=dataMap)
    else:
        return render_template('index.html', title="ScioStats")
