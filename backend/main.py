from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from plot_azel import generate_azel_plot
import base64
import os
import matplotlib
matplotlib.use('Agg')


app = FastAPI()

origins = list(filter(None, {
    os.getenv("FRONTEND_ORIGIN"),
    "http://localhost:3000",
}))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://e-azel-plot.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Target(BaseModel):
    name: str
    color: str


class PlotRequest(BaseModel):
    date: str
    timezone: str
    site: str
    targets: List[Target]


@app.post("/generate")
async def generate_plot(req: PlotRequest):
    targets_for_plot = [
        {"label": t.name, "color": t.color} for t in req.targets
    ]
    plot_result = generate_azel_plot(
        obsdate=req.date,
        timezone=req.timezone,
        site=req.site,
        targets_input=targets_for_plot
    )
    
    image_data_base64 = None
    image_buffer = plot_result.get("image_data")
    if image_buffer and hasattr(image_buffer, 'getvalue'): 
        image_data_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode('utf-8')

    return JSONResponse(content={
        "imageData": image_data_base64,
        "errors": plot_result.get("errors", [])
    })
