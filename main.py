from helpers.db_helper import db, db_raw, all, special, sort_by
from helpers.markdown_to_html import markdown_to_html
from helpers.deso_helper import upload_to_deso
from helpers.uuid_helper import gen_uuid
from helpers.cors import fix_cors
from flask import *
import tempfile
import json

app = Flask(__name__)
"""
db["users"] = {}
db["jobs"] = {}
db["competitions"] = {}
"""

@app.route("/user/signup", methods=["POST"])
@fix_cors
def createUserIfNotExists():
  if request.form["uid"] not in db_raw["users"].keys():
    db["users"][request.form["uid"]] = {"uid": request.form["uid"], "profile": upload_to_deso(request.files["profile"])}
  return ""

@app.route("/jobs/all", methods=["GET"])
@fix_cors
def allJobs():
  retdata = []
  for job in all("jobs"):
    del job["applications"]
    del job["applicants"]
    del job["interested"]
    retdata.append(job)
  return jsonify(retdata)

@app.route("/jobs/one/<jid>", methods=["GET"])
@fix_cors
def oneJob(jid):
  retdata = special("jobs", jid)
  del retdata["applications"]
  del retdata["applicants"]
  del retdata["interested"]
  return jsonify(retdata)

@app.route("/jobs/create", methods=["POST"])
@fix_cors
def createJob():
  data = request.form.to_dict()
  data["jid"] = gen_uuid()
  data["questions"] = json.loads(data["questions"])
  data["applications"] = {}
  data["applicants"] = []
  data["interested"] = []
  data["description"] = markdown_to_html(data["description"])
  data["image"] = upload_to_deso(request.files["image"])
  db["jobs"][data["jid"]] = data
  return ""

@app.route("/jobs/<jid>", methods=["POST"])
@fix_cors
def interestJob(jid):
  db["jobs"][jid]["interested"].append(request.json["uid"])
  return ""

@app.route("/competitions/all", methods=["GET"])
@fix_cors
def allCompetitions():
  retdata = []
  for competition in all("competitions"):
    del competition["applications"]
    del competition["applicants"]
    del competition["interested"]
    retdata.append(competition)
  return jsonify(retdata)

@app.route("/competitions/one/<cid>", methods=["GET"])
@fix_cors
def oneCompetition(cid):
  retdata = special("competitions", cid)
  del retdata["applications"]
  del retdata["applicants"]
  del retdata["interested"]
  return jsonify(retdata)

@app.route("/competitions/create", methods=["POST"])
@fix_cors
def createCompetition():
  data = request.form.to_dict()
  data["cid"] = gen_uuid()
  data["questions"] = json.loads(data["questions"])
  data["applications"] = {}
  data["applicants"] = []
  data["interested"] = []
  data["description"] = markdown_to_html(data["description"])
  data["image"] = upload_to_deso(request.files["image"])
  db["competitions"][data["cid"]] = data
  return ""

@app.route("/competitions/<cid>", methods=["POST"])
@fix_cors
def interestCompetition(cid):
  db["jobs"][cid]["interested"].append(request.json["uid"])
  return ""

@app.route("/jobs/registered/<jid>", methods=["GET"])
@fix_cors
def getApplicantsJobs(jid):
  return jsonify(list(db_raw["jobs"][jid]["applications"].values()))

@app.route("/competitions/registered/<cid>", methods=["GET"])
@fix_cors
def getApplicantsCompetitions(cid):
  return jsonify(list(db_raw["competitions"][jid]["applications"].values()))

@app.route("/interview/<uid>", methods=["POST"])
@fix_cors
def interviewApplicant(uid):
  db["jobs"][request.json["jid"]]["applications"][uid]["interviewed"] = request.json["interviewed"]
  return ""

@app.route("/users/one/<uid>", methods=["POST"])
@fix_cors
def oneUser(uid):
  return jsnofiy(special("users", uid))

app.run(host="0.0.0.0")
