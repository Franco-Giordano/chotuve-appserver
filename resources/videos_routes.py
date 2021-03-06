from flask_restful import reqparse, Resource

from services.mediasender import MediaSender
from services.authsender import AuthSender

from daos.videos_dao import VideoDAO
from daos.reactions_dao import ReactionDAO

from utils.decorators import token_required

import logging

post_parser = reqparse.RequestParser()
post_parser.add_argument("x-access-token", location='headers')
post_parser.add_argument('description', type = str, default = "", location = 'json')
post_parser.add_argument('location', type = str, default = "", location = 'json')
post_parser.add_argument('title', type = str, default = "", location = 'json')
post_parser.add_argument('thumbnail_url', type = str, required = True, location = 'json')
post_parser.add_argument('is_private', type = bool, default = False, location = 'json')
post_parser.add_argument('firebase_url', type = str, required = True, help="No firebase URL provided", location = 'json')



class UniqueVideoRoute(Resource):
    def __init__(self):
       self.logger = logging.getLogger(self.__class__.__name__)
       super(UniqueVideoRoute, self).__init__()

    @token_required
    def get(self, vid_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        self.logger.debug("getting uuid from token, via authsv")
        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        self.logger.debug("getting single vid from videoDAO")
        vid = VideoDAO.get(vid_id, uuid)

        vid["author"] = AuthSender.get_author_name(vid["uuid"], args["x-access-token"])

        self.logger.info(f"Retrieved single video, id {vid_id}, info: {vid}. RESPONSECODE:200")
        return vid, 200

    @token_required
    def patch(self, vid_id):
        edit_parser = reqparse.RequestParser()
        edit_parser.add_argument("x-access-token", location='headers')
        edit_parser.add_argument('description', type = str, location = 'json')
        edit_parser.add_argument('location', type = str, location = 'json')
        edit_parser.add_argument('title', type = str, location = 'json')
        edit_parser.add_argument('is_private', type = bool, location = 'json')
        args = edit_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        self.logger.debug("editing single vid from videoDAO")
        vid = VideoDAO.edit(vid_id, args, uuid)

        self.logger.info(f"Edited video info, id {vid_id}, info: {vid}. RESPONSECODE:200")
        return vid, 200
        
    @token_required
    def delete(self, vid_id):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        args = parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        self.logger.debug(f"Deleting video {vid_id}")
        VideoDAO.delete(vid_id, uuid)

        self.logger.info(f"Deleted video with id {vid_id}. RESPONSECODE:200")
        return {"message":"OK"}, 200


class VideoRoute(Resource):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(VideoRoute, self).__init__()
        
    @token_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers')
        parser.add_argument("search", type=str, required=False, location='args', default=None)
        parser.add_argument("page", type=int, required=False, location='args', default=1)
        parser.add_argument("per_page", type=int, required=False, location='args', default=50)
        args = parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        if args["search"]:
            videos = VideoDAO.get_from_search(uuid, args["x-access-token"], args["search"], page=args["page"], per_page=args["per_page"])
        else:
            videos = VideoDAO.get_recommendations(uuid, args["x-access-token"], page=args["page"], per_page=args["per_page"])

        # videos = VideoDAO.get_all(uuid, args["x-access-token"])

        self.logger.info(f"Executed /videos search, found {len(videos['videos'])} videos. RESPONSECODE:200")
        return videos, 200

    @token_required
    def post(self):
        args = post_parser.parse_args()

        uuid = AuthSender.get_uuid_from_token(args["x-access-token"])

        # add to local db
        new_vid_with_url = VideoDAO.add_vid(title=args['title'], description=args['description'], uuid=uuid, 
                        location=args['location'], is_private=args['is_private'], thumbnail_url=args['thumbnail_url'])

        # upload to mediasv
        new_vid_with_url['firebase_url'], new_vid_with_url['timestamp'] = MediaSender.send_url(new_vid_with_url['video_id'],args['firebase_url'])

        self.logger.info(f"New video uploaded, video info: {new_vid_with_url}. RESPONSECODE:201")
        return new_vid_with_url, 201


