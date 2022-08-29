# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-29 07:33:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 07:45:35

from orb.web.app import serve as web_serve
import typer

app = typer.Typer()


@app.command()
def serve():
    """
    Serve the Orb web app.
    """
    web_serve()
