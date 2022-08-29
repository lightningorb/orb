# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-29 07:43:15
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 14:01:34

import uvicorn
from fastapi import FastAPI

from pathlib import Path
from threading import Lock
from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.app import App
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

webapp = FastAPI()

path = Path(__file__).parent
pub = (path / "orb_frontend/public").as_posix()
build = (path / "orb_frontend/public/build").as_posix()

webapp.mount("/front", StaticFiles(directory=pub, html=True), name="front")
webapp.mount("/build", StaticFiles(directory=build), name="build")


webapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


orbapp = None
app_build_lock = Lock()


def app_dependency():
    global orbapp
    with app_build_lock:
        if not orbapp:
            pubkey = get_default_id()
            App().run(pubkey=pubkey)
            ln = factory(pubkey)
            App().build(ln)
            orbapp = App.get_running_app()
        return orbapp


@webapp.get("/channels")
def channels(orbapp=Depends(app_dependency)):
    return [
        dict(
            capacity=x.channel.capacity,
            profit=x.channel.profit,
            alias=x.channel.alias,
            local_balance=x.channel.local_balance,
            remote_balance=x.channel.remote_balance,
        )
        for x in orbapp.channels
    ]


@webapp.get("/info")
def channels(orbapp=Depends(app_dependency)):
    return orbapp.ln.get_info().todict()


@webapp.get("/")
async def front():
    return RedirectResponse(url="front")


def serve(
    host: str = "0.0.0.0",
    port: int = 8080,
    reload: bool = True,
    debug: bool = True,
    workers: int = 3,
):
    uvicorn.run(
        "orb.web.app:webapp",
        host=host,
        port=port,
        reload=reload,
        debug=debug,
        workers=workers,
    )
