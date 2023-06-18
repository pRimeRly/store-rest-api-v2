from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operation on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Returns all tags in a store."""
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        """Creates a new tag in a store."""
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route('/items/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItem(MethodView):

    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        """Links a tag to an item the store."""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if not (item.store_id == tag.store_id):
            abort(400, message="Tags must belong to the same store")

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag")

        return tag

    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        """Unlink a tag to an item the store."""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if not (item.store_id == tag.store_id):
            abort(400, message="Tags must belong to the same store")

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the tag")

        return {"message": "Item removed from the tag", "item": item, "tag": tag}


@blp.route("/tags/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """Returns a tag."""
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it",
        example={"message": "Tag deleted successfully."}
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag cannot be deleted."
    )
    def delete(self, tag_id):
        """Deletes a tag only if not linked."""
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not be deleted. Tag is associated with one or more items."
        )
