from datetime import datetime
from app import db

from exceptions.exceptions import NotFoundError

friends = db.Table('friends',
                   db.Column('user1_id', db.Integer,
                             db.ForeignKey('users.id')),
                   db.Column('user2_id', db.Integer, db.ForeignKey('users.id'))
                   )

requests = db.Table('requests',
                    db.Column('sender_id', db.Integer,
                              db.ForeignKey('users.id')),
                    db.Column('recver_id', db.Integer,
                              db.ForeignKey('users.id'))
                    )

# modelo


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    friends = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.user1_id == id),
        secondaryjoin=(friends.c.user2_id == id), lazy='dynamic')

    sent_requests = db.relationship(
        'User', secondary=requests,
        primaryjoin=(requests.c.sender_id == id),
        secondaryjoin=(requests.c.recver_id == id),
        backref=db.backref('pending_requests', lazy='dynamic'), lazy='dynamic')

    push_token = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def serialize(self):
        return {
            'user_id': self.id
        }

    def serializeFriends(self):
        return {
            'friends': [f.serialize() for f in self.friends],
        }

    def serializeReceivedReqs(self):
        return {
            'pending_reqs': [p.serialize() for p in self.pending_requests]
        }

    def serializeSentReqs(self):
        return {
            'sent_reqs': [p.serialize() for p in self.sent_requests]
        }

    def is_friend_with(self, user2):
        return self.friends.filter(friends.c.user2_id == user2.id).count() > 0

    def received_request_from(self, user2):
        return self.pending_requests.filter(requests.c.sender_id == user2.id).count() > 0

    def accept_request_from(self, sender):
        if self.received_request_from(sender):
            self.pending_requests.remove(sender)

            self.friends.append(sender)
            sender.friends.append(self)

            db.session.commit()

        else:
            raise NotFoundError(
                f"Friendship request from {sender.id} to {self.id} not found!")

    def delete_friendship(self, other_user):
        self.friends.remove(other_user)
        other_user.friends.remove(self)

        db.session.commit()


    def reject_request_from(self, sender):
        if self.received_request_from(sender):
            self.pending_requests.remove(sender)

            db.session.commit()

        else:
            raise NotFoundError(
                f"Friendship request from {sender.id} to {self.id} not found!")

    def count_friends(self):
        return len(self.friends.all())