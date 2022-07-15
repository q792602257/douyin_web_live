from flask import Blueprint, request, jsonify

from core import CoreManager

blueprint = Blueprint("api_manager", __name__, url_prefix="/api/manager")

c = CoreManager()


@blueprint.post("/on_broadcast")
def on_broadcast():
    form = request.form
    if "room_id" in form:
        c.on_broadcast(room_id=form['room_id'])
        return jsonify(
            message="OK",
            code=0,
            success=True,
            data=None
        )
    else:
        return jsonify(
            message="Missing Param [room_id]",
            code=403,
            success=False,
            data=None
        )


@blueprint.post("/open_url")
def open_url():
    form = request.form
    if "url" in form:
        c.open_tab(form['url'])
        return jsonify(
            message="OK",
            code=0,
            success=True,
            data=None
        )
    else:
        return jsonify(
            message="Missing Param [room_id]",
            code=403,
            success=False,
            data=None
        )


@blueprint.get("/config")
def get_config():
    return jsonify(
        message="OK",
        code=0,
        success=True,
        data=c.config_manager.config,
    )


@blueprint.post("/config")
def write_config():
    c.config_manager.save_config()
    return jsonify(
        message="OK",
        code=0,
        success=True,
        data=None
    )
