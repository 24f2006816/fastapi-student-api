import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load CSV
try:
    students_df = pd.read_csv("q-fastapi.csv")
except FileNotFoundError:
    students_df = pd.DataFrame(columns=["studentId", "class"])

@app.get("/api")
def get_students(class_filter: Optional[List[str]] = Query(None, alias="class")):
    """
    Return all students or filtered by class.
    """
    if class_filter:
        filtered_df = students_df[students_df["class"].isin(class_filter)]
    else:
        filtered_df = students_df

    return {"students": filtered_df.to_dict(orient="records")}
