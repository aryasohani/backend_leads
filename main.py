from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models import OfferIn
from storage import init_db, save_offer, save_leads_bulk, fetch_all_leads_unscored, update_lead_score, fetch_latest_offer, fetch_all_results
from utils import parse_csv_file
from scoring import compute_rule_score
from ai_client import classify_with_ai
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all origins
    allow_credentials=True,
    allow_methods=["*"],       # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],       # allow all headers
)
init_db()

@app.get("/")
async def root():
    return {"message": "Lead Scoring API is running. Visit /docs for Swagger UI."}

@app.post("/offer")
async def post_offer(offer: OfferIn):
    save_offer(offer.dict())
    return {"status":"ok"}

@app.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    tmp = "leads.csv"
    with open(tmp, "wb") as f:
        f.write(await file.read())
    leads = parse_csv_file(tmp)
    save_leads_bulk(leads)
    return {"status":"ok", "imported": len(leads)}

@app.post("/score")
async def run_scoring():
    offer = fetch_latest_offer()
    leads = fetch_all_leads_unscored()
    results = []
    for row in leads:
        lead = dict(row)
        rule_score, reasons = compute_rule_score(lead, offer)
        intent, ai_reason = classify_with_ai(offer, lead)
        ai_points = {"High":50,"Medium":30,"Low":10}.get(intent, 10)
        final = min(100, rule_score + ai_points)
        update_lead_score(lead['id'], final, intent, "; ".join(reasons) + " | AI: " + ai_reason)
        results.append({"name": lead['name'], "intent": intent, "score": final})
    return {"processed": len(results), "results": results}

@app.get("/results")
async def get_results():
    return fetch_all_results()
