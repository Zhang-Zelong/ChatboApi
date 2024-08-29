# coding:utf-8
import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.routes.completion import router as completion_router
from src.routes.deprecated import router as deprecated_router
from src.routes.models import router as models_router
from src.routes.vector import router as vec_router

# 日志配置
logger = logging.getLogger("chatbot")
logger.info("backend starts...")

doc_dir = Path(__file__).parent.parent / "docs"
api_doc = doc_dir / "api_docs.md"

app = FastAPI(
    title="大模型调用平台",
    summary="大模型调用平台",
    version="1.0.0",
    description=api_doc.read_text(),
    docs_url=None,
)

app.include_router(models_router)
app.include_router(completion_router)
app.include_router(vec_router)
app.include_router(deprecated_router)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=doc_dir / "static"), name="static")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"reply": "", "status": "error", "error": str(exc)},
    )


@app.get("/docs")
def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title,
        swagger_favicon_url="https://fenxiplus.mktindex.com/favicon.ico",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=14883, log_config="uvicorn_log.json")
