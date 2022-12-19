from flask import render_template, redirect, url_for, session
from jardiquest.model.database.entity.quete import Quete
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db
from datetime import date




def getUser(user_id: int):
    """Get the user with the id user_id or redirect to login page if not connected"""
    if user_id is None:
        return redirect(url_for("controller.login"))
    else:
        return User.query.get(user_id)

# ------------------------------------------ Garden quests ------------------------------------------

def list_garden_id_quest_model(gardenId : int):
    garden = Jardin.query.get(gardenId)
    quests = Quete.query.filter_by(id_jardin=gardenId).all()
    return render_template("quests_list_garden.html", quests=quests, today = date.today(), garden = garden)


def list_garden_quest_model(user_id: str):
    user = getUser(user_id)
    if not user.idJardin :
        # TODO : redirect to a page to create a garden or to join one
        return "test"
        pass
    else:
        id_garden = user.idJardin
        garden = Jardin.query.get(id_garden)
        quests = Quete.query.filter_by(id_jardin=id_garden, id_user = None).all()
        return render_template("quests_list_garden.html", quests=quests, today = date.today(), garden = garden)


# ------------------------------------------ User quests ------------------------------------------
def list_user_quests_model(user_id: str):
    user = getUser(user_id)
    garden = Jardin.query.get(user.idJardin)
    quests = user.quetes
    return render_template("quests_list_user.html", quests=quests, today = date.today(), user = user, garden=garden)


def accept_quest_model(user_id: str, quest_id: int):
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == user.idJardin:
        quest.id_user = user_id
        db.session.commit()
    else :
        return "probleme"
    return redirect(url_for("controller.list_garden_quests"))


def cancel_quest_model(user_id: str, quest_id: int):
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == user.idJardin:
        quest.id_user = None
        db.session.commit()
    else :
        return "probleme"
        pass
    return redirect(url_for("controller.list_user_quests"))



def complete_quest_model(user_id: str, quest_id: int):
    user = getUser(user_id)
    quest = Quete.query.get(quest_id)
    if quest.id_jardin == user.idJardin:
        quest.accomplished = True
        db.session.commit()
    else :
        return "probleme"
    return redirect(url_for("controller.list_user_quests"))



# ------------------------------------------ Quests Details ------------------------------------------
def display_quest_model(quest_id: int):
    """Display a quest with a specific id"""
    user_id = session.get("_user_id")
    quest = Quete.query.get(quest_id)
    garden = Jardin.query.get(quest.id_jardin)
    return render_template("quest_details.html", quest=quest, today = date.today(), garden = garden, user = user_id)

