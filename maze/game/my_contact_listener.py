from Box2D import *


class MyContactListener(b2ContactListener):
    def BeginContact(self, contact):
        user_data_a = contact.fixtureA.body.userData
        user_data_b = contact.fixtureB.body.userData
        if user_data_a is not None:
            user_data_a.contact(contact.fixtureA, contact.fixtureB, contact)
        if user_data_b is not None:
            user_data_b.contact(contact.fixtureB, contact.fixtureA, contact)

    def EndContact(self, contact):
        pass

    def PostSolve(self, contact, impulse):
        pass

    def PreSolve(self, contact, old_manifold):
        pass
