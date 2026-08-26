from flask import jsonify, request
from flask_login import login_required

from services.feed_service import FeedService


class FeedController:
    @staticmethod
    @login_required
    def listar():
        busca = request.args.get("busca")
        return jsonify(FeedService.montar_feed(busca))
