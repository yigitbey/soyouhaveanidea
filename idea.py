from random import choice, randrange


class Idea(object):

    def __init__(self):
        self.pitch = self.random_idea_generator()
        self.features = randrange(900, 1500) * 10
        self.design_need = randrange(10, 20) * 10

    def random_idea_generator(self):
        starters = ["Like", "We're"]
        products = ["Facebook", "Google", "Tinder", "Instagram", "Gmail", "Uber", "Airbnb",
                    "Dropbox", "Snapchat", "Pinterest", "Spotify", "SoundHound", "Medium",
                    "EventBrite", "Quora", "Slack", "Github", "Twitter", "Craigslist",
                    "an online Community", "a social marketing automation platform",
                    "a reminder app"
                    ]
        combiners = ["with", "without", "but without", "for", "but for"]
        nouns = ["pictures", "children", "animals", "pets", "videos", "moms", "dads",
                 "ugly people", 'videos', "space", "planets", "government", "mathematicians",
                 "surgeons", "youtubers", "redditors", "events", "ex-girlfriends",
                 "disappearing messages"]

        return "{} {} {} {}.".format(
            choice(starters),
            choice(products),
            choice(combiners),
            choice(nouns)
        )

    def __repr__(self):
        return self.pitch