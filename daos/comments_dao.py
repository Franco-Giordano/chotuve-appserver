from app import db
from run import app
from models.video_elements import Video

from daos.videos_dao import VideoDAO

from models.video_elements import Comment

class CommentDAO():

    @classmethod
    def add_cmnt(cls, vid_id, uuid,text):
        with app.app_context():
            new_cmnt = Comment(uuid=uuid, text=text)
            new_cmnt.video = VideoDAO.get_raw(vid_id)
            
            db.session.add(new_cmnt)
            db.session.commit()

            return new_cmnt.serialize()


    @classmethod
    def get_all_from(cls, vid_id):
        with app.app_context():
            vid =  VideoDAO.get_raw(vid_id)

            return [c.serialize() for c in vid.comments]